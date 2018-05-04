import io
import os

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

# Instantiates a client
client = vision.ImageAnnotatorClient()

response = client.annotate_image({
    'image': {
        'source': {
            'image_uri': 'http://www.researchpaperspot.com/wp-content/uploads/2017/09/home-depot-receipt-template-professional-templates-for-home-depot-receipt-template.jpg'
        },
    },
    'features': [
        {'type': vision.enums.Feature.Type.LOGO_DETECTION},
        {'type': vision.enums.Feature.Type.DOCUMENT_TEXT_DETECTION}
    ],
})

print(response.logo_annotations)
print(response.full_text_annotation.text)
