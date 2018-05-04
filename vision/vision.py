import io
import os
import requests
from PIL import Image, ImageDraw
from enum import Enum

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

class FeatureType(Enum):
    PAGE = 1
    BLOCK = 2
    PARA = 3
    WORD = 4
    SYMBOL = 5

def draw_boxes(image, bounds, color):
    """Draw a border around the image using the hints in the vector list."""
    # [START draw_blocks]
    draw = ImageDraw.Draw(image)

    for bound in bounds:
        draw.polygon([
            bound.vertices[0].x, bound.vertices[0].y,
            bound.vertices[1].x, bound.vertices[1].y,
            bound.vertices[2].x, bound.vertices[2].y,
            bound.vertices[3].x, bound.vertices[3].y], None, color)
    return image

def get_document_bounds(document, feature):
    # [START detect_bounds]
    """Returns document bounds given an image."""
    bounds = []

    # Collect specified feature bounds by enumerating all document features
    for page in document.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    for symbol in word.symbols:
                        if (feature == FeatureType.SYMBOL):
                            bounds.append(symbol.bounding_box)

                    if (feature == FeatureType.WORD):
                        bounds.append(word.bounding_box)

                if (feature == FeatureType.PARA):
                    bounds.append(paragraph.bounding_box)

            if (feature == FeatureType.BLOCK):
                bounds.append(block.bounding_box)

        if (feature == FeatureType.PAGE):
            bounds.append(block.bounding_box)
    return bounds

# Instantiates a client
image_uri = 'http://www.researchpaperspot.com/wp-content/uploads/2017/09/home-depot-receipt-template-professional-templates-for-home-depot-receipt-template.jpg'
client = vision.ImageAnnotatorClient()
google_response = client.annotate_image({
    'image': {
        'source': {
            'image_uri': image_uri
        },
    },
    'features': [
        {'type': vision.enums.Feature.Type.LOGO_DETECTION},
        {'type': vision.enums.Feature.Type.DOCUMENT_TEXT_DETECTION}
    ],
})
document = google_response.full_text_annotation

downloaded_image = requests.get(image_uri)
image = Image.open(io.BytesIO(downloaded_image.content))

bounds = get_document_bounds(document, FeatureType.PAGE)
draw_boxes(image, bounds, 'blue')
bounds = get_document_bounds(document, FeatureType.PARA)
draw_boxes(image, bounds, 'red')
bounds = get_document_bounds(document, FeatureType.WORD)
draw_boxes(image, bounds, 'yellow')
image.show()

print(google_response.logo_annotations)
print(google_response.full_text_annotation.text)
