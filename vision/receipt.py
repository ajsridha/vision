import io
import re
import os
import requests
import sys
from PIL import Image, ImageDraw
from babel.numbers import parse_decimal
from enum import Enum

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types


def extract_amount(sentence):
    # find index where number begins
    # get everything to the right
    match = re.search(r"\d", sentence)
    number_index = match.start()
    amount = sentence[number_index:]
    return re.sub(r"\s", "", amount)

def extract_tax(sentence):
    match = re.search(r"\d", sentence)
    number_index = match.start()
    tax = sentence[:number_index].strip()

    amount = extract_amount(sentence)
    if "%" in amount:
        percentage_index = amount.index("%")
        amount = amount[percentage_index + 1:]
    return {
        "tax": tax,
        "amount": amount
    }


if len(sys.argv) != 2:
    print("[Usage] receipt.py path-to-image")
    exit()

# Instantiates a client
image_uri = sys.argv[1]
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



threshold = 10 # threshold for y coordinate (line) just in case image is skewed.
               # this is used for identifying each block of text are in the same line.
threshold_x_pct = 20 # threshold for x coordinate - just in case the result is a skewed box

line = -1
sentences = []
text = ""
end_x = 0
end_x_min = None
end_x_max = None
start_x = 0
start_x_count = 0

# print("Step 1 - Define farthest right x coordinate")
text_annotations = google_response.text_annotations
word_count = 0
for index, text_annotation in enumerate(text_annotations):
    if index == 0:
        continue
    bounds = text_annotation.bounding_poly.vertices

    # Get the farthest right x coordinate
    end_x = max([
        end_x,
        max(bounds[1].x, bounds[3].x)
    ])

end_x_min = end_x - ((threshold_x_pct * end_x) / 100) # Calculate threshold for x

# print("Step 2 - Construct sentence line by line")
last_bounds = None
for index, text_annotation in enumerate(text_annotations):
    if index == 0:
        continue
    bounds = text_annotation.bounding_poly.vertices

    this_average = (bounds[2].y + bounds[3].y)/2
    if line < 0:
        line = this_average

    # Check if the middle of the word is within the line threshold
    if abs(this_average - line) <= threshold:
        text = "{} {}".format(text, text_annotation.description) # Within the threshold, add to line with space delimited
    else: # beyond threshold
        average_end_x = (last_bounds[1].x + last_bounds[3].x) / 2
        if average_end_x >= end_x_min:
            sentences.append(text)

        text = text_annotation.description # create a new line
        start_x += bounds[0].x
        start_x_count = start_x_count + 1

    line = this_average
    last_bounds = bounds


vendor = ""
logos = google_response.logo_annotations
for logo in logos:
    vendor = logo.description


total = 0
found_total = False

taxes = []
found_tax = False

for index, sentence in enumerate(sentences):
    if not len(vendor) and index == 0:
        vendor = sentence
    if "total" in sentence.lower() and "sub" not in sentence.lower():
        total = extract_amount(sentence)
    if "tax" in sentence.lower():
        taxes.append(extract_tax(sentence))


print("Vendor: {}".format(vendor))
for tax in taxes:
    print("{}: {}".format(tax["tax"], tax["amount"]))
print("Total: {}".format(total))

