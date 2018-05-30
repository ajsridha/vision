import sys
import yaml
from PIL import Image, ImageDraw

from io import BytesIO
import json
from enum import Enum


class FeatureType(Enum):
    PAGE = 1
    BLOCK = 2
    PARA = 3
    WORD = 4
    SYMBOL = 5

def draw_boxes(image, words, color):
    """Draw a border around the image using the hints in the vector list."""
    # [START draw_blocks]
    draw = ImageDraw.Draw(image)
    for word in words:
        bound = word['bounds']
        draw.polygon([
            bound['vertices'][0]['x'], bound['vertices'][0]['y'],
            bound['vertices'][1]['x'], bound['vertices'][1]['y'],
            bound['vertices'][2]['x'], bound['vertices'][2]['y'],
            bound['vertices'][3]['x'], bound['vertices'][3]['y']], None, color)
    return image

def get_words(document):
    # [START detect_bounds]
    """Returns document bounds given an image."""
    words = []

    # Collect specified feature words by enumerating all document features
    for page in document['fullTextAnnotation']['pages']:
        for block in page['blocks']:
            for paragraph in block['paragraphs']:
                for word in paragraph['words']:
                    detected_word = ""
                    for symbol in word['symbols']:
                        detected_word += symbol['text']

                    words.append({
                        "text": detected_word,
                        "bounds": word['boundingBox']
                    })

    return words

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

        words = get_words(document)
        import pdb; pdb.set_trace()
        draw_boxes(preview, words, 'yellow')
        preview.show()


if __name__ == "__main__":
    main()
