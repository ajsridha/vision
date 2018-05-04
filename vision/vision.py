import io
import os

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

# Instantiates a client
client = vision.ImageAnnotatorClient()

response = client.annotate_image({
    'image': {'source': {'image_uri': 'gs://my-test-bucket/image.jpg'}},
    'features': [{'type': vision.enums.Feature.Type.FACE_DETECTION}],
})
