from shapely.geometry import Polygon
from math import (
    fabs,
    cos,
    sin,
    radians,
    sqrt,
    pow
)

class LinesExtractor(object):
    def __init__(self, document, receipt):
        self.receipt = receipt

        if not receipt.orientation_known:
            degrees = self._calculate_orientation_from_fragments(document)
            self.receipt.rotate(degrees)

        word_fragments, highest_x = self._get_fragments(document)
        self.word_fragments = word_fragments
        self.words = self._extract_text(word_fragments, highest_x)

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

    def _calculate_orientation_from_fragments(self, document):
        count = 0
        width_sum = 0
        height_sum = 0

        for page in document['fullTextAnnotation']['pages']:
            for block in page['blocks']:
                for paragraph in block['paragraphs']:
                    for word in paragraph['words']:
                        width, height = self._measure_box(word['boundingBox'])
                        width_sum += width
                        height_sum += height

                        count = count + 1
        average_width = width_sum / count
        average_height = height_sum / count

        if average_height > average_width:
            return 270
        return 0

    def _measure_box(self, bounds):
        top_left_corner = bounds['vertices'][0]
        top_right_corner = bounds['vertices'][1]
        bottom_right_corner = bounds['vertices'][2]
        try:
            width = fabs(sqrt((
                pow(top_right_corner['x'] - top_left_corner['x'], 2) +
                pow(top_right_corner['y'] - top_left_corner['y'], 2)
            )))

            height = fabs(sqrt((
                pow(bottom_right_corner['x'] - top_left_corner['x'], 2) +
                pow(bottom_right_corner['y'] - top_left_corner['y'], 2)
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
                            highest_x = self._find_highest_x(bounds, highest_x)

                            fragments.append({
                                "id": count,
                                "text": detected_word,
                                "polygon": self._get_polygon(bounds),
                                "bounds": bounds
                            })
                        except:
                            pass
                        count = count + 1

        return fragments, highest_x

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

    def _extract_text(self, fragments, highest_x):
        original_fragments = fragments.copy()
        fragments_for_collision_checks = fragments.copy()

        collisions = []

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
            big_line = self._extend_to_the_right(fragment, highest_x)

            # Check what collides with this big line
            for collision_fragment in fragments_for_collision_checks:
                if self._fragments_touch(big_line, collision_fragment):
                    collisions.append(collision_fragment['id'])
                    new_word_fragments.append(collision_fragment)

        return extracted_text

    def _combine_words(self, words):
        new_word = ""
        last_word = None

        if not words:
            return new_word
        for word in words:
            if last_word is None:
                new_word += word['text']
                last_word = word
                continue

            # 36% - 1:23pm
            # Add no spaces if the last word was pretty close to each other
            if word['polygon'].distance(last_word['polygon']) < 15:
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
            if collision_percentage > 50:
                return True

            return False
        except:
            return False

    def _extend_to_the_right(self, word, highest_x):
        vertices = self._get_vertices(word['bounds'])
        try:
            top_right_coordinate = self._calculate_right_most_coordinate(
                vertices[0], vertices[1], highest_x)

            # We want the right and left sides to be parallel with each other
            # So we offset the x coordinate
            bottom_right_coordinate = self._calculate_right_most_coordinate(
                vertices[3], vertices[2], highest_x - (vertices[3][0] - vertices[0][0]))
        except ZeroDivisionError:
            return Polygon([
                vertices[0],
                vertices[1],
                vertices[2],
                vertices[3]
            ])

        return Polygon([
            vertices[0],
            top_right_coordinate,
            bottom_right_coordinate,
            vertices[3]
        ])

    def _calculate_right_most_coordinate(self, point1, point2, new_x):
        Y = 1
        X = 0

        slope = (point2[Y] - point1[Y]) / (point2[X] - point1[X])
        intercept = ((slope * point1[X]) - point1[Y]) * -1

        new_y = (new_x * slope) + intercept
        return (new_x, new_y)

    def _rotate_word(self, bounds):
        new_vertices = []
        for bound in bounds['vertices']:
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
