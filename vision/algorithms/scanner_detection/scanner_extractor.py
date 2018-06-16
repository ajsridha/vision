import imageio
import re
import copy

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
        self.document = document
        self.receipt = receipt
        words, average_word_height = self.extract_words()

        self.algorithm_frames = []
        self.words = words

        # Fatten it up
        self.scan_height = average_word_height * 1.10

        self.lines = self.extract_lines()
        for line in self.lines:
            print(line)
        # imageio.mimsave('/Users/anton/movie.gif', self.algorithm_frames)

    def extract_words(self):
        words = []
        count = 0
        sum_height = 0
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
                            sum_height += word.height
                            count += 1
                        except KeyError:
                            continue

        return words, sum_height/count

    def extract_lines(self):
        words = list(self.words)
        collisions = []
        words_in_line = []
        lines = []

        total_height = 0

        while total_height < self.receipt.height:
            if words_in_line:
                lines.append(self.create_line(words_in_line))
                words_in_line = []

            big_line = self.get_big_line(total_height)
            total_height = total_height + self.scan_height

            for word in words:
                if word.id in collisions:
                    continue

                if self.collides(big_line, word):
                    collisions.append(word.id)
                    words_in_line.append(word)

            self.algorithm_frames.append(
                self.receipt.preview_scanner(
                    big_line,
                    self.uncombined_words(words, collisions),
                    thumbnail=600))

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
                if re.search('[a-zA-Z0-9&$]', curr_char):
                    line += " "
                elif  re.search('[:]', curr_char):
                    pass
            elif re.search('[0-9]', last_char):
                if re.search('[a-zA-Z]', curr_char):
                    line += " "
                elif re.search('[.]', curr_char):
                    pass
            elif re.search('[&]', last_char) and re.search('[a-zA-Z]', curr_char):
                line += " "
            elif re.search('[#]', last_char) and re.search('[a-zA-Z]', curr_char):
                line += " "
            elif re.search('[:]', last_char) and re.search('[a-zA-Z]', curr_char):
                line += " "
            elif re.search('[:]', last_char) and re.search('[0-9]', curr_char):
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
        collision_percentage = (polygon.intersection(big_line).area / polygon.area) * 100
        if collision_percentage > 10:
            return True

        return False

    def uncombined_words(self, words, collisions):
        polygons = []
        for word in words:
            if word.id not in collisions:
                polygons.append(word.polygon)
        return polygons


    def get_big_line(self, position):
        return Polygon([
            (0, position),
            (self.receipt.width, position),
            (self.receipt.width, position + self.scan_height),
            (0, position + self.scan_height)
        ])

    def print_polygon(self, polygon):
        x_list, y_list = polygon.exterior.xy
        print("Polygon({}, {}, {}, {})".format(
            (x_list[0], y_list[0]),
            (x_list[1], y_list[1]),
            (x_list[2], y_list[2]),
            (x_list[3], y_list[3]),
        ))
