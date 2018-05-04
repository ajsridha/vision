import io
import re
import os
import requests
from PIL import Image, ImageDraw
from enum import Enum

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

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
        {'type': vision.enums.Feature.Type.DOCUMENT_TEXT_DETECTION}
    ],
})



threshold = 10 # threshold for y coordinate (line) just in case image is skewed.
               # this is used for identifying each block of text are in the same line.
threshold_x_pct = 20 # threshold for x coordinate - just in case the result is a skewed box

print("Start Detection...")

line = -1
sentences = []
sentences_bound = []
text = ""
end_x = 0
end_x_min = None
end_x_max = None
start_x = 0
start_x_count = 0
start_x_max = None

print("Step 1 - Define farthest right x coordinate")
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

print("Step 2 - Construct sentence line by line")
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
            sentences_bound.append(bounds)

        text = text_annotation.description # create a new line
        start_x += bounds[0].x
        start_x_count = start_x_count + 1

    line = this_average
    last_bounds = bounds

start_x = start_x / start_x_count
start_x_max = start_x + ((threshold_x_pct * start_x)/100)

print("Step 3 - Getting the 'last price' - from the rightest part of sentence and traverse to the left.")
results = []
for index, sentence in enumerate(sentences):
    sentence_parts = sentence.split(" ")
    print("--> sentence is {}".format(sentence))
    print("----> sr is {}".format(sentence_parts))

    num_candidate = 0
    check_before = True

    # Going from right to left
    for sentence_part in reversed(sentence_parts):
        word = sentence_part.strip()

        # google vision 'cuts' word by space (?), so sometime we see the amount 2, 000 is cut into
        # 2 words, need to join this into a number
        if word.startswith(",") or word.startswith("."):
            word = re.sub(r"/,/g", "", word)
            if not is_number(word):
                print("------>stop at word: {}".format(word))
                break # End, not a number
            else:
                num_candidate = float(word) + num_candidate
                print("------> numCandidate is: {}".format(num_candidate))
                check_before = True
                continue
        elif word.endswith(",") or word.endswith("."):
            word = re.sub(r"/,/g", "", word)
            if not is_number(word):
                print("------>stop at word: {}".format(word))
                break # End, not a number
            else:
                num_candidate = float(word) + num_candidate
                print("------> numCandidate is: {}".format(num_candidate))
                check_before = False
                continue
        elif check_before:
            word = re.sub(r"/,/g", "", word)
            if not is_number(word):
                print("------>stop at word: {}".format(word))
                break # End, not a number
            else:
                num_candidate = float(word) + num_candidate
                print("------> numCandidate is: {}".format(num_candidate))
                check_before = False
                continue
        else:
            print("------>stop at word: {}".format(word))
            break
    print("------>candidate is {}".format(num_candidate))
    num = float(num_candidate)

    if num is None or num < 100:
        if len(results) == 0 or num < 100:
            continue
    else:
        results.append({
            "number": float(num_candidate),
            "bounds": sentences_bound[index]
        })

print({
    "textDetectionResult": results
})
