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


class LinesExtractor(object):
    def __init__(self, document, receipt):
        self.receipt = receipt
        if not receipt.orientation_known:
            degrees = self._calculate_orientation_from_fragments(document)
            self.receipt.rotate(degrees)
        self.word_fragments = self._get_fragments(document)
        self.words = self._extract_text(self.word_fragments, self.receipt.width)
        self.lines = [Line(word) for word in self.words]

    def text(self):
        return list(map(lambda x: x['text'], self.words))

    def boxes(self):
        return list(map(lambda x: x['bounds'], self.words))

    def fragment_boxes(self):
        return list(map(lambda x: x['bounds'], self.word_fragments))

    def preview_original(self):
        boxes = self.fragment_boxes()
        self.receipt.preview(boxes)

    def preview(self):
        boxes = self.boxes()
        self.receipt.preview(boxes)

    def preview_algorithm(self):
        boxes = self.fragment_boxes()
        big_lines = []
        for line in self.big_lines:
            vertices = []
            for index, x_coordinate in enumerate(line.exterior.xy[0]):
                vertices.append({
                    'x': x_coordinate,
                    'y': line.exterior.xy[1][index]
                })
            big_lines.append({
                'vertices': vertices
            })

        self.receipt.preview_algorithm(big_lines, boxes)

    def _calculate_orientation_from_fragments(self, document):
        count = 0
        width_sum = 0
        height_sum = 0
        vertices = []

        for page in document['fullTextAnnotation']['pages']:
            for block in page['blocks']:
                for paragraph in block['paragraphs']:
                    for word in paragraph['words']:
                        vertices = word['boundingBox']['vertices']
                        break

        center_x = 0
        center_y = 0
        for vertice in vertices:
            center_x += vertice["x"]
            center_y += vertice["y"]

        center_x = center_x/4
        center_y = center_y/4

        point_x = vertices[0]["x"]
        point_y = vertices[0]["y"]

        if point_x < center_x:
            # 0 --- 1
            # |     |
            # 3 --- 2
            if point_y < center_y:
                return 0

            # 1 --- 2
            # |     |
            # 0 --- 3
            return 270

        # 3 --- 0
        # |     |
        # 2 --- 1
        if point_y < center_y:
            return 90

        # 2 --- 3
        # |     |
        # 1 --- 0
        return 180

    def _measure_box(self, bounds):
        bottom_left_corner = bounds['vertices'][0]
        bottom_right_corner = bounds['vertices'][1]
        top_right_corner = bounds['vertices'][2]
        top_left_corner = bounds['vertices'][3]

        try:
            width = fabs(sqrt((
                pow(top_right_corner['x'] - top_left_corner['x'], 2) +
                pow(top_right_corner['y'] - top_left_corner['y'], 2)
            )))

            height = fabs(sqrt((
                pow(bottom_right_corner['x'] - top_right_corner['x'], 2) +
                pow(bottom_right_corner['y'] - top_right_corner['y'], 2)
            )))
            return width, height
        except:
            return 0, 0

    def _get_fragments(self, document):
        fragments = []
        count = 0
        highest_x = None

        for page in document['fullTextAnnotation']['pages']:
            for block in page['blocks']:
                for paragraph in block['paragraphs']:
                    for word in paragraph['words']:
                        detected_word = ""
                        for symbol in word['symbols']:
                            detected_word += symbol['text']
                        try:
                            bounds = self._rotate_word(word['boundingBox'])

                            # sorted_bounds = self._sort_bounds(bounds)
                            fragments.append({
                                "id": count,
                                "text": detected_word,
                                "polygon": self._get_polygon(bounds),
                                "bounds": bounds
                            })
                            count = count + 1
                        except:
                            continue

        return fragments

    def _get_polygon(self, boundings):
        vertices = self._get_vertices(boundings)
        return Polygon(vertices)

    def _get_vertices(self, bound):
        return [
            (bound['vertices'][0]['x'], bound['vertices'][0]['y']),
            (bound['vertices'][1]['x'], bound['vertices'][1]['y']),
            (bound['vertices'][2]['x'], bound['vertices'][2]['y']),
            (bound['vertices'][3]['x'], bound['vertices'][3]['y'])
        ]

    def _find_highest_x(self, bounds, highest_x):
        for bound in bounds['vertices']:
            new_x = bound['x']

            if highest_x is None or new_x > highest_x:
                highest_x = new_x

            return highest_x

    def compare_distance_to_left(self, word):
        # Sort by looking at the top left vertice, and figuring out how close it is to 0
        return word['bounds']['vertices'][3]['x']

    def _extract_text(self, fragments, highest_x):
        original_fragments = fragments.copy()
        fragments_for_collision_checks = fragments.copy()
        big_lines = []

        collisions = []

        average_slope = 0
        for fragment in original_fragments:
            slope = self._calculate_slope(fragment)
            if slope > 0:
                average_slope += self._calculate_slope(fragment)

        average_slope = average_slope/len(original_fragments)

        new_word_fragments = []
        extracted_text = []
        for fragment in original_fragments:
            # Skip words that already belong to something
            if fragment['id'] in collisions:
                continue

            # By now, we will have a new word so let's form one and reset
            combined_word = self._combine_words(new_word_fragments)
            if combined_word:
                extracted_text.append(combined_word)

            # Reset the new word fragments
            new_word_fragments = []

            # Take the left-most word and extend its box all the way to the right
            big_line = self._extend_to_the_right(fragment, average_slope, highest_x)
            big_lines.append(big_line)

            # print("Big Line: {}".format(fragment['text']))
            # Check what collides with this big line
            for collision_fragment in fragments_for_collision_checks:
                if collision_fragment['id'] in collisions:
                    continue
                if self._fragments_touch(big_line, collision_fragment):
                    # print("Collision: {}".format(collision_fragment['text']))

                    collisions.append(collision_fragment['id'])
                    new_word_fragments.append(collision_fragment)
        self.big_lines = big_lines
        return extracted_text

    def print_polygon(self, polygon):
        x_list, y_list = polygon.exterior.xy
        print("Polygon({}, {}, {}, {})".format(
            (x_list[0], y_list[0]),
            (x_list[1], y_list[1]),
            (x_list[2], y_list[2]),
            (x_list[3], y_list[3]),
        ))

    def _combine_words(self, words):
        new_word = ""
        mode = 0

        if not words:
            return new_word

        # Sort each word in the line left ro right
        words = sorted(words, key=self.compare_distance_to_left)

        last_word = None
        distances = []
        for word in words:
            if last_word is None:
                last_word = word
                continue

            distances.append(word['polygon'].distance(last_word['polygon']))
            last_word = word

        if len(distances) > 1:
            mode = max(set(distances), key=distances.count)

        last_word = None
        for word in words:
            if last_word is None:
                new_word += word['text']
                last_word = word
                continue

            # 36% - May 30  1:23pm
            # Back at 36% - June 2nd at 1:18 pm
            # 54% June 4 at 8:22 am
            # 66% June 7 at 8:22 am
            # Add no spaces if the last word was pretty close to each other

            if (word['polygon'].distance(last_word['polygon']) < mode) or \
                    (re.match(r'\d', new_word[-1]) and word['text'] in ['.', '/']) or \
                    (re.match(r'\d', word['text'][-1]) and new_word[-1] in ['.', '/']):
                new_word += word['text']
                last_word = word
                continue

            new_word += " " + word['text']
            last_word = word

        first_word = words[0]['bounds']['vertices']
        last_word = words[-1]['bounds']['vertices']

        return {
            "text": new_word,
            "bounds": {
                "vertices": [
                    {'x': first_word[0]["x"], 'y': first_word[0]["y"]},
                    {'x': first_word[3]["x"], 'y': first_word[3]["y"]},
                    {'x': last_word[2]["x"], 'y': last_word[2]["y"]},
                    {'x': last_word[1]["x"], 'y': last_word[1]["y"]},
                ]
            }
        }

    def _fragments_touch(self, big_line, collision_fragment):
        polygon = collision_fragment['polygon']

        if not big_line.intersects(polygon):
            return False
        try:
            # We dont' want to add fragments that only barely touch the big line
            collision_percentage = (polygon.intersection(big_line).area / polygon.area) * 100
            if collision_percentage > 41:
                return True

            return False
        except:
            return False

    def _extend_to_the_right(self, word, slope, highest_x):
        vertices = self._get_vertices(word['bounds'])
        try:
            top_right_coordinate = self._calculate_right_most_coordinate(
                vertices[0], vertices[1], slope, highest_x)

            # We want the right and left sides to be parallel with each other
            # So we offset the x coordinate
            bottom_right_coordinate = self._calculate_new_line(
                slope, vertices[3], highest_x - (vertices[3][0] - vertices[0][0]))

            top_left_coordinate = (0, vertices[0][1])
            bottom_left_coordinate = (0, vertices[3][1])

        except ZeroDivisionError:
            return Polygon([
                vertices[0],
                vertices[1],
                vertices[2],
                vertices[3]
            ])

        return Polygon([
            top_left_coordinate,
            top_right_coordinate,
            bottom_right_coordinate,
            bottom_left_coordinate
        ])

    def _calculate_slope(self, word):
        Y = 1
        X = 0
        vertices = self._get_vertices(word['bounds'])
        point1 = vertices[0]
        point2 = vertices[1]
        try:
            return (point2[Y] - point1[Y]) / (point2[X] - point1[X])
        except ZeroDivisionError:
            return 0


    def _calculate_right_most_coordinate(self, point1, point2, slope, new_x):
        Y = 1
        X = 0

        intercept = ((slope * point1[X]) - point1[Y]) * -1

        new_y = (new_x * slope) + intercept
        return (new_x, new_y)

    def _calculate_new_line(self, slope, point, new_x):
        Y = 1
        X = 0

        intercept = ((slope * point[X]) - point[Y]) * -1
        new_y = (new_x * slope) + intercept
        return (new_x, new_y)

    def _rotate_word(self, bounds):
        new_vertices = []
        for bound in bounds['vertices']:
            if "x" not in bound or "y" not in bound:
                raise Exception("Incomplete vertice")
            new_x, new_y = self._rotate_point(bound["x"], bound["y"])
            new_vertices.append({
                "x": new_x,
                "y": new_y
            })

        return {
            "vertices": new_vertices
        }

    def _rotate_point(self, x, y):

        new_x = self.receipt.center_x + (
            ((x - self.receipt.center_x) * cos(self.receipt.rotation_radians))
            - ((y - self.receipt.center_y) * sin(self.receipt.rotation_radians))
        )
        new_y = self.receipt.center_y + (
            ((x - self.receipt.center_x) * sin(self.receipt.rotation_radians))
            + ((y - self.receipt.center_y) * cos(self.receipt.rotation_radians))
        )
        return new_x + self.receipt.offset_x, new_y + self.receipt.offset_y
