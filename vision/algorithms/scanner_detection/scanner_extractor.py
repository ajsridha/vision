import imageio
import re
import copy
import numpy as np

from shapely.geometry import Polygon
from vision.models.line import Line
from vision.models.word import Word
from math import (
    fabs,
    cos,
    sin,
    radians,
    sqrt,
    pow
)

import logging
logging.basicConfig()
shapely_log = logging.getLogger("shapely")
shapely_log.setLevel(logging.ERROR)

class ScannerExtractor(object):
    # https://www.pyimagesearch.com/2017/02/20/text-skew-correction-opencv-python/

    # like a scanner, we create a huge line,
    # and traverse down the image,
    # Collecting all the collisions
    def __init__(self, document, receipt):
        self.debug = False
        self.thumbnail_size = 1000
        self.collision_sensitivity_percentage = 0.10
        self.fattened_big_line_percentage = 0.15

        self.document = document
        self.receipt = receipt
        self.words = self.extract_words()

        # Orientations
        #   0 - Upright: We can scan top to bottom
        #  90 - Sideways: We can scan right to left
        # 180 - Upsidedown: We can scan bottom to top
        # 270 - Sideways: We can scan left to right
        self.orientation = np.median([word.orientation for word in self.words])

        self.big_line_height = np.median([word.height for word in self.words]) * \
            (1 + self.fattened_big_line_percentage)
        self.big_line_slope = self.calculate_big_line_slope()

        self.algorithm_frames = []
        self.lines = self.extract_lines()

        if self.debug:
            for line in self.lines:
                print(line)
            imageio.mimsave('/Users/anton/movie.gif', self.algorithm_frames)

    def extract_words(self):
        words = []
        count = 0
        for page in self.document['fullTextAnnotation']['pages']:
            for block in page['blocks']:
                for paragraph in block['paragraphs']:
                    for word in paragraph['words']:
                        detected_word = ""
                        for symbol in word['symbols']:
                            detected_word += symbol['text']

                        try:
                            word = Word(
                                    count + 1,
                                    detected_word.split('\n'),
                                    word
                                )
                            words.append(word)
                            count += 1
                        except KeyError:
                            continue

        return words

    def calculate_big_line_slope(self):
        slopes = [self.calculate_slope(word) for word in self.words]
        num_undefined = slopes.count(None)
        # Too many vertical lines means they're probably mostly vertical lines
        if num_undefined > len(slopes) - num_undefined:
            return None

        # If the median is the vast majority, return that instead
        slopes = filter(lambda slope: slope is not None, slopes)
        median_slope = np.median(slopes)
        count_median = slopes.count(median_slope)
        median_percentage = count_median * 1.0 / len(slopes) * 100
        if median_percentage > 80:
            return median_slope

        # Figure out the average slope, minus outliers that can mess up the average
        data = np.array(slopes)
        m = 2
        d = np.abs(data - np.median(data))
        mdev = np.median(d)
        s = d/mdev if mdev else 0.
        return np.mean(data[s < m])

    def extract_lines(self):
        words = list(self.words)
        collisions = []
        words_in_line = []
        lines = []

        total_height = 0

        # for word in words:
        #     print("\n{}".format(word.text))
        #     self.print_polygon(word.polygon)
        #     import pdb; pdb.set_trace()

        while total_height < self.receipt_height:
            if words_in_line:
                lines.append(self.create_line(words_in_line))
                words_in_line = []

            big_line = self.get_big_line(total_height)
            total_height = total_height + self.big_line_height
            # if self.debug:
            #     print("\nBig Line:")
            #     self.print_polygon(big_line)

            for word in words:
                if word.id in collisions:
                    continue

                if self.collides(big_line, word):
                    # if self.debug:
                    #     print("Collision:")
                    #     self.print_polygon(word.polygon)
                    collisions.append(word.id)
                    words_in_line.append(word)

            if self.debug:
                self.algorithm_frames.append(
                    self.receipt.preview_scanner(
                        big_line,
                        self.uncombined_words(words, collisions),
                        thumbnail=self.thumbnail_size))

        return lines

    def create_line(self, words):
        non_decimal_numerical_chars = [".", "/", ",", "$"]
        line = u""
        last_word = u""

        for word in words:
            current_word = word.text[0].strip()
            last_char = line[-1] if line else ""
            curr_char = current_word[0] if current_word else ""

            if re.search('[a-zA-Z]', last_char):
                if re.search('[a-zA-Z0-9&$(]', curr_char):
                    line += " "
                elif  re.search('[:]', curr_char):
                    pass
            elif re.search('[0-9]', last_char):
                if re.search('[a-zA-Z0-9$]', curr_char):
                    line += " "
                elif re.search('[.]', curr_char):
                    pass
            elif re.search('[%&#%]', last_char) and re.search('[a-zA-Z]', curr_char):
                line += " "
            elif re.search('[:]', last_char) and re.search('[a-zA-Z]', curr_char):
                line += " "
            elif re.search('[%:]', last_char) and re.search('[0-9]', curr_char):
                line += " "
            elif re.search('[.]', last_char) and re.search('[0-9]', curr_char):
                pass
            elif re.search('[,]', last_char) and re.search('[a-zA-Z]', curr_char):
                pass

            line += current_word

        return Line(line)


    def collides(self, big_line, word):
        polygon = word.polygon
        if not polygon.is_valid:
            polygon = polygon.buffer(0)

        if not big_line.intersects(polygon):
            return False

        collision = big_line.intersection(polygon)
        # We dont' want to add fragments that only barely touch the big line
        collision_percentage = (polygon.intersection(big_line).area / polygon.area)
        if collision_percentage > self.collision_sensitivity_percentage:
            return True

        return False

    def uncombined_words(self, words, collisions):
        polygons = []
        for word in words:
            if word.id not in collisions:
                polygons.append(word.polygon)
        return polygons


    def get_big_line(self, position):

        if self.orientation in [0, 180]:
            top_left = (0, position)
            bottom_left = (0, position + self.big_line_height)
            top_right = (self.receipt.width, position)
            bottom_right = (self.receipt.width, position + self.big_line_height)

            if self.big_line_slope is not None:
                top_intercept = top_left[1] - (self.big_line_slope * top_left[0])
                top_right_y = (self.big_line_slope * self.receipt.width) + top_intercept
                top_right = (self.receipt.width, top_right_y)

                bottom_intercept = bottom_left[1] - (self.big_line_slope * bottom_left[0])
                bottom_right_y = (self.big_line_slope * self.receipt.width) + bottom_intercept
                bottom_right = (self.receipt.width, bottom_right_y)


        elif self.orientation in [90, 270]:
            top_left = (position, 0)
            bottom_left = (position + self.big_line_height, 0)
            top_right = (position, self.receipt.height)
            bottom_right = (position + self.big_line_height, self.receipt.height)

            if self.big_line_slope is not None:
                top_intercept = top_left[1] - (self.big_line_slope * top_left[0])
                top_right_x = (self.receipt.height - top_intercept) / self.big_line_slope
                top_right = (top_right_x, self.receipt.height)

                bottom_intercept = bottom_left[1] - (self.big_line_slope * bottom_left[0])
                bottom_right_x = (self.receipt.height - bottom_intercept) / self.big_line_slope
                bottom_right = (bottom_right_x, self.receipt.height)

        return Polygon([
            top_left,
            top_right,
            bottom_right,
            bottom_left
        ])

    def print_polygon(self, polygon):
        x_list, y_list = polygon.exterior.xy
        print("Polygon({}, {}, {}, {})".format(
            (x_list[0], y_list[0]),
            (x_list[1], y_list[1]),
            (x_list[2], y_list[2]),
            (x_list[3], y_list[3]),
        ))

    @property
    def receipt_height(self):
        # Upright
        if self.orientation in [0, 180]:
            return self.receipt.height
        elif self.orientation in [180, 270]:
            return self.receipt.width

        return self.receipt.height

    def calculate_slope(self, word):
        try:
            x, y = word.polygon.exterior.xy
            if self.orientation in [0, 180]:
                # 2 --- 3
                # |     |
                # 1 --- 0
                return float(y[2] - y[3]) / float(x[2] - x[3])

            elif self.orientation in [90, 270]:
                # 3 --- 2
                # |     |
                # 0 --- 1
                return float(y[3] - y[0]) / float(x[3] - x[0])

        except ZeroDivisionError:
            # Pesky vertical lines
            return None
