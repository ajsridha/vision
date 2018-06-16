from shapely.geometry import Polygon
from vision.models.line import Line
import re
from math import (
    fabs,
    cos,
    sin,
    radians,
    sqrt,
    pow
)
import math
import logging

MAX_X = 4000

logging.basicConfig()
shapely_log = logging.getLogger("shapely")
shapely_log.setLevel(logging.ERROR)

class Paragraph(object):
    def __ini__(self, words, bounds):
        self.words = words
        self.bounds = bounds

class HybridExtractor(object):

    # Go through each "paragraph"
    # Extend and see what it collides with
    # New Idea: Fat paragraphs? Get height, increase padding, then see
    # Grab text and smash together into new lines
    # Maybe compare number of lines?
    # Maybe even try to see the differnce in paragraph Y values to see if it's top-heavy or bottom-heavy
    def __init__(self, document, receipt):
        self.document = document
        self.receipt = receipt
        self.paragraphs = self.extract_paragraphs()
        self.lines = [Line(line) for line in self.find_collisions()]

    def build_amounts(self):
        return 0, [], 0

    def extract_paragraphs(self):
        paragraphs = []
        count = 0
        for page in self.document['fullTextAnnotation']['pages']:
            for block in page['blocks']:
                for paragraph in block['paragraphs']:

                    words = ''
                    for word in paragraph['words']:
                        detected_word = ""
                        for symbol in word['symbols']:
                            detected_word += symbol['text']

                        words += detected_word.strip()
                        last_symbol = word['symbols'][-1]
                        if 'detectedBreak' in last_symbol['property']:
                            detectedBreak = last_symbol['property']['detectedBreak']['type']
                            # print(symbol['text'], detectedBreak)
                            if detectedBreak == 'LINE_BREAK':
                                words += '\n'
                            elif detectedBreak == 'SPACE':
                                words += ' '
                            elif detectedBreak == 'EOL_SURE_SPACE':
                                words += '\n'

                    if re.search('[a-zA-Z0-9]', words):
                        try:
                            paragraphs.append({
                                'id': count + 1,
                                'text': words.strip().split('\n'),
                                'vertices': self.get_vertices(paragraph['boundingBox'])
                            })
                            count += 1
                        except KeyError:
                            continue

        paragraphs = self.sort_paragraphs(paragraphs)
        return paragraphs

    def get_vertices(self, bound):
        # print("Polygon({}, {}, {}, {})".format(
        #     (bound['vertices'][0]['x'], bound['vertices'][0]['y']),
        #     (bound['vertices'][1]['x'], bound['vertices'][1]['y']),
        #     (bound['vertices'][2]['x'], bound['vertices'][2]['y']),
        #     (bound['vertices'][3]['x'], bound['vertices'][3]['y'])
        # ))
        return self.reorientate_vertices([
            (bound['vertices'][0]['x'], bound['vertices'][0]['y']),
            (bound['vertices'][1]['x'], bound['vertices'][1]['y']),
            (bound['vertices'][2]['x'], bound['vertices'][2]['y']),
            (bound['vertices'][3]['x'], bound['vertices'][3]['y'])
        ])

    def reorientate_vertices(self, vertices):
        center_x = 0
        center_y = 0
        for vertice in vertices:
            center_x += vertice[0]
            center_y += vertice[1]

        center_x = center_x/4
        center_y = center_y/4

        point_x = vertices[0][0]
        point_y = vertices[0][1]
        if point_x < center_x:
            # 0 --- 1
            # |     |
            # 3 --- 2
            if point_y < center_y:
                return vertices

            # 1 --- 2
            # |     |
            # 0 --- 3
            return [
                vertices[1],
                vertices[2],
                vertices[3],
                vertices[0]
            ]

        # 3 --- 0
        # |     |
        # 2 --- 1
        if point_y < center_y:
            return [
                vertices[3],
                vertices[0],
                vertices[1],
                vertices[2]
            ]

        # 2 --- 3
        # |     |
        # 1 --- 0
        return [
            vertices[2],
            vertices[3],
            vertices[0],
            vertices[1]
        ]

    def find_collisions(self):
        extended_paragraphs = list(self.paragraphs)
        collision_paragraphs = list(self.paragraphs)

        used_extended_paragraphs = []
        collided_paragraphs = []
        current_collisions = []

        results = []

        for paragraph in extended_paragraphs:
            # Skip paragraphs that already belong to something
            if paragraph['id'] in collided_paragraphs:
                continue

            if len(current_collisions):
                results.append(self.combine_paragraphs(current_collisions))
                current_collisions = []

            # Take the left-most word and extend its box all the way to the right
            extended_paragraph = self.extend_polygon(paragraph)
            print("\nBig Paragraph: {}\n--{}".format(paragraph['text'], self.debug_polygon(extended_paragraph)))

            used_extended_paragraphs.append(extended_paragraph)
            for collision_paragraph in collision_paragraphs:
                if collision_paragraph['id'] in collided_paragraphs:
                    continue
                if self.collides(extended_paragraph, collision_paragraph):
                    collided_paragraphs.append(collision_paragraph['id'])
                    current_collisions.append(collision_paragraph)
        self.receipt.preview_hybrid(used_extended_paragraphs, collision_paragraphs)
        lines = [text for result in results for text in result]
        # print(lines)
        return lines

        return ''

    def combine_paragraphs(self, paragraphs):
        # paragraphs = self.sort_paragraphs(paragraphs)

        # sort left to right
        # Try to determine how many columns we'll have

        # For each column, we sort top down

        # Now go through each column, and combine the words

        # When combining, we find the largest column, and 'pad' each one, until they're the same length
        # Then we combine each column together

        for paragraph in paragraphs:
            print("Collision: {}\n--{}".format(paragraph['text'], self.debug_polygon(Polygon(paragraph['vertices']))))
        first_paragraph_text = paragraphs[0]['text']
        found_text = []
        for paragraph in paragraphs[1:]:
            found_text += paragraph['text']

        if not found_text:
            return first_paragraph_text

        if len(first_paragraph_text) == len(found_text):
            assembled_text = []
            for index, text in enumerate(first_paragraph_text):
                assembled_text.append(u"{} {}".format(text, found_text[index]))
            return assembled_text

        return first_paragraph_text + found_text


    def collides(self, polygon_1, paragraph):
        polygon_2 = Polygon(paragraph['vertices'])
        if not polygon_1.is_valid:
            polygon_1 = polygon_1.buffer(0)

        if not polygon_2.is_valid:
            polygon_2 = polygon_2.buffer(0)

        if not polygon_1.intersects(polygon_2):
            return False
        try:
            # We dont' want to add fragments that only barely touch the big line
            collision_percentage = (polygon_2.intersection(polygon_1).area / polygon_2.area) * 100
            if collision_percentage > 10:
                return True
        except:
            return False
        return False

    def extend_polygon(self, paragraph):
        # 0 --- 1
        # |     |
        # 3 --- 2
        top_left_point = paragraph['vertices'][0]
        top_right_point = paragraph['vertices'][1]

        bottom_left_point = paragraph['vertices'][3]
        bottom_right_point = paragraph['vertices'][2]

        top_left_point, top_right_point = self.extend_line(top_left_point, top_right_point)
        bottom_left_point, bottom_right_point = self.extend_line(bottom_left_point, bottom_right_point)

        top_left_point, bottom_left_point = self.increase_height(top_left_point, bottom_left_point)
        top_right_point, bottom_right_point = self.increase_height(top_right_point, bottom_right_point)

        return Polygon([ top_left_point, top_right_point, bottom_right_point, bottom_left_point])

    def increase_height(self, top_point, bottom_point):
        X = 0
        Y = 1
        height_increase = 0.20
        height_delta = fabs(bottom_point[Y] - top_point[Y])  * height_increase
        new_top_y = top_point[Y] - height_delta
        new_bottom_y = bottom_point[Y] + height_delta

        try:
            slope = float(top_point[Y] - bottom_point[Y]) / float(top_point[X] - bottom_point[X])
            intercept = ((slope * bottom_point[X]) - bottom_point[Y]) * -1
        except ZeroDivisionError:
            return (top_point[X], new_top_y), (bottom_point[X], new_bottom_y)

        new_top_x = (new_top_y - intercept) / slope
        new_bottom_x = (new_bottom_y - intercept) / slope

        return (new_top_x, new_top_y), (new_bottom_x, new_bottom_y)

    def calculate_line_length(self, point_1, point_2):
        X = 0
        Y = 1
        return fabs(sqrt((
            pow(point_2[X] - point_1[X], 2) +
            pow(point_2[Y] - point_1[Y], 2)
        )))

    def extend_line(self, left_point, right_point):
        X = 0
        Y = 1

        slope = float(right_point[Y] - left_point[Y]) / float(right_point[X] - left_point[X])
        intercept = ((slope * left_point[X]) - left_point[Y]) * -1
        left = (0, self.calculate_y(0, slope, intercept))
        right = (MAX_X, self.calculate_y(MAX_X, slope, intercept))
        return left, right

    def calculate_y(self, x, slope, intercept):
        return (x * slope) + intercept

    # Sort by the top right vertice
    def sort_paragraphs(self, paragraphs):
        # Sort by x left to right
        paragraphs = sorted(paragraphs, key=lambda paragraph:paragraph['vertices'][1][0], reverse=True)

        # Sort by y top to bottom
        paragraphs = sorted(paragraphs, key=lambda paragraph:paragraph['vertices'][1][1])
        return paragraphs
        return list(reversed(paragraphs))

    def debug_polygon(self, polygon):
        vertices = polygon.exterior.xy
        return "Polygon({}, {}, {}, {})".format(
            (vertices[0][0], vertices[1][0]),
            (vertices[0][1], vertices[1][1]),
            (vertices[0][2], vertices[1][2]),
            (vertices[0][3], vertices[1][3])
        )
