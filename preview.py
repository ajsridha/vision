import sys
import yaml
import numpy
import math
from shapely.geometry import Polygon
from PIL import Image, ImageDraw, ExifTags
from io import BytesIO
import json
from enum import Enum


def get_vertices(bound):
    return [
        (bound['vertices'][0]['x'], bound['vertices'][0]['y']),
        (bound['vertices'][1]['x'], bound['vertices'][1]['y']),
        (bound['vertices'][2]['x'], bound['vertices'][2]['y']),
        (bound['vertices'][3]['x'], bound['vertices'][3]['y'])
    ]


def draw_boxes(image, words, color):
    draw = ImageDraw.Draw(image)
    for word in words:
        bound = word['bounds']
        draw.polygon([
            bound['vertices'][0]['x'], bound['vertices'][0]['y'],
            bound['vertices'][1]['x'], bound['vertices'][1]['y'],
            bound['vertices'][2]['x'], bound['vertices'][2]['y'],
            bound['vertices'][3]['x'], bound['vertices'][3]['y']], None, color)
    return image

def get_raw_wordsymbols(document, rotation, center_x, center_y, offset_x, offset_y):
    # [START detect_bounds]
    words = []
    count = 0
    highest_x = None

    # Collect specified feature words by enumerating all document features
    for page in document['fullTextAnnotation']['pages']:
        for block in page['blocks']:
            for paragraph in block['paragraphs']:
                for word in paragraph['words']:
                    detected_word = ""
                    for symbol in word['symbols']:
                        detected_word += symbol['text']

                    bounds = rotate_word(word['boundingBox'], rotation, center_x, center_y, offset_x, offset_y)
                    highest_x = find_highest_x(bounds, highest_x)
                    words.append({
                        "id": count,
                        "text": detected_word,
                        "bounds": bounds
                    })
                    count = count + 1

    return words, highest_x

def find_highest_x(bounds, highest_x):
    for bound in bounds['vertices']:
        new_x = bound['x']

        if highest_x is None or new_x > highest_x:
            highest_x = new_x

        return highest_x

def main():
    if len(sys.argv) != 2:
        raise Exception("No testcase specified")

    testcase = sys.argv[1]
    stream = open('fixtures/vcr_cassettes/{}.yaml'.format(testcase), 'r')
    docs = yaml.load_all(stream)
    image = None
    image_uri = ''
    for doc in docs:
        for key, value in doc.items():
            if key != 'interactions':
                continue
            image_download = value[0]
            image = image_download['response']['body']['string']
            image_uri = image_download['request']['uri'].replace(
                'http://afn85.webfactional.com/receipts/',
                '/Users/anton/projects/vision/fixtures/vision/')
            break

    if image and image_uri:
        with open(image_uri, 'r') as fb:
            document = json.loads(fb.read())['responses'][0]
        fb.close()

        preview = Image.open(BytesIO(image))
        width, height = preview.size
        center_x = width / 2
        center_y = height / 2

        for orientation in ExifTags.TAGS.keys() :
            if ExifTags.TAGS[orientation]=='Orientation' : break
        exif = dict(preview._getexif().items())
        rotation = None
        if exif[orientation] == 3 :
            rotation = 180
        elif exif[orientation] == 6 :
            rotation = 270
        elif exif[orientation] == 8 :
            rotation = 90

        new_w = width
        new_h = height
        if rotation:
            preview = preview.rotate(rotation, expand=True)
            new_w, new_h = preview.size

        offset_x = (new_w - width) / 2
        offset_y = (new_h - height) / 2
        print(offset_x, offset_y)
        # m = (new_h - height) / (new_w - width)
        words, highest_x = get_raw_wordsymbols(document, rotation, center_x, center_y, offset_x, offset_y)
        # words = get_real_words(words, highest_x)

        # Once we have these words, we can look for check if 'total-like' words exist and see if it collides with amounts
        draw_boxes(preview, words, 'yellow')
        preview.show()

def rotate_word(bounds, rotation, center_x, center_y, offset_x, offset_y):
    if not rotation:
        return bounds

    new_vertices = []
    for bound in bounds['vertices']:
        new_x, new_y = rotate(center_x, center_y, bound["x"], bound["y"], offset_x, offset_y, rotation)
        new_vertices.append({
            "x": new_x,
            "y": new_y
        })

    return {
        "vertices": new_vertices
    }

def rotate(center_x, center_y, x, y, offset_x, offset_y, degrees):
    # if degrees == 270:
    #     degrees = 90

    radians = math.radians(90)
    new_x = center_x + (
        ((x - center_x) * math.cos(radians))
        - ((y - center_y) * math.sin(radians))
    )
    new_y = center_y + (
        ((x - center_x) * math.sin(radians))
        + ((y - center_y) * math.cos(radians))
    )
    return new_x + offset_x, new_y + offset_y

def extend_to_the_right(word, highest_x):
    verticies = get_vertices(word['bounds'])
    try:
        top_right_coordinate = calculate_right_most_coordinate(verticies[0], verticies[1], highest_x)
        bottom_right_coordinate = calculate_right_most_coordinate(verticies[3], verticies[2], highest_x - (verticies[3][0] - verticies[0][0]))
        return Polygon([
            verticies[0],
            top_right_coordinate,
            bottom_right_coordinate,
            verticies[3]
        ])
    except ZeroDivisionError:
        return Polygon([
            verticies[0],
            verticies[1],
            verticies[2],
            verticies[3]
        ])

def get_polygon_from_word(word):
    verticies = get_vertices(word['bounds'])
    return Polygon(verticies)

def calculate_right_most_coordinate(point1, point2, new_x):
    Y = 1
    X = 0
    slope = (point2[Y] - point1[Y]) / (point2[X] - point1[X])
    intercept = ((slope * point1[X]) - point1[Y]) * -1

    new_y = (new_x * slope) + intercept
    return (new_x, new_y)

def combine_words(words):
    new_word = ""
    last_word = None

    if not words:
        return new_word
    for word in words:
        if last_word is None:
            new_word += word['meta']['text']
            last_word = word
            continue

        if word['polygon'].distance(last_word['polygon']) < 10:
            new_word += word['meta']['text']
            last_word = word
            continue
        # else word['polygon'].distance(last_word['polygon']) < 50:
        new_word += " " + word['meta']['text']
        # print(new_word, word['polygon'].distance(last_word['polygon']))
        last_word = word

    first_word = words[0]['meta']['bounds']['vertices']
    last_word = words[-1]['meta']['bounds']['vertices']

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


def get_real_words(words, highest_x):
    lines = []
    collisions = []
    original_words = words.copy()
    words_to_check_collisions = words.copy()

    new_word = []
    new_words = []
    for word in original_words:
        # Skip words that already belong to something
        if word['id'] in collisions:
            continue

        # By now, we will have a new word so let's form one and reset
        combined_word = combine_words(new_word)
        if combined_word:
            new_words.append(combined_word)
        new_word = []

        big_line = extend_to_the_right(word, highest_x)
        new_words.append(transform_polygon(big_line))
        for word_to_check in words_to_check_collisions:
            word_polygon = get_polygon_from_word(word_to_check)
            if big_line.intersects(word_polygon):
                try:
                    collision_percentage = (word_polygon.intersection(big_line).area/word_polygon.area)*100
                    if collision_percentage > 50:
                        collisions.append(word_to_check['id'])
                        new_word.append({
                            "meta": word_to_check,
                            "polygon": word_polygon
                        })
                except:
                    pass


    # for foo in new_words:
    #     print(foo['text'])
    return new_words
        # boundary = shapely.geometry.Polygon(vertices)
    # Given a list of boxes, pick the first one, and draw a line to the right
    # If there's a collision:
    #   check if it's within our word kerning tolerance
    #       if yes: add that to a new 'group' list
    # This will give us a list of words that belong together. ie. $19.95
    # We get new bounds now, that's equal to the top left and bottom left of the first object
    # And top right and bottom right of the last object
    # If a word is in our 'group' list: ignore it

def transform_polygon(polygon):
    vertices = []
    coordinates = polygon.exterior.coords.xy
    for i, x in enumerate(coordinates[0]):
        vertices.append({"x": x, "y": coordinates[1][i]})

    return {
        "bounds": {
            "vertices": vertices
        }
    }

if __name__ == "__main__":
    main()
