import re
from decimal import Decimal
from google.cloud import vision
from constants import GRAND_TOTAL_FIELDS, SUBTOTAL_FIELDS, TAX_FIELDS


class Word():
    def __init__(self, text):
        self.text = text

    def is_money(self):
        pattern = re.compile('^(-?\$?(\d)*.(\d))')
        return pattern.match(self.text) is not None

    def is_number(self):
        try:
            float(self.text)
            return True
        except ValueError:
            return False

    def is_percentage(self):
        return '%' in self.text

    def numeric_money_amount(self):
        if not self.is_money():
            return None

        number = ''
        pattern = re.compile('^\d')
        for char in self.text:
            if char == "." or pattern.match(char):
                number = number + char

        return Decimal(number)

def generate_receipt(annotated_image_response):
    description = annotated_image_response.text_annotations[0].description
    lines = build_lines(description)
    receipt = build_receipt(lines)

    print(receipt)

def build_lines(description):
    lines = []
    for words in description.split('\n'):
        line = []
        for word in words.split(' '):
            word = Word(word)
            line.append(word)
        lines.append(line)

    return lines

def build_receipt(lines):
    grand_total = 0
    sub_total = 0
    taxes = []

    for index, line in enumerate(lines):
        for field in SUBTOTAL_FIELDS:
            if any(word.text.upper() == field.upper() for word in line):
                sub_total = find_amount(lines, index, field)
                break

    for index, line in enumerate(lines):
        for field in GRAND_TOTAL_FIELDS:
            if any(word.text.upper() == field.upper() for word in line):
                grand_total = find_amount(lines, index, field)
                break

    for index, line in enumerate(lines):
        for field in TAX_FIELDS:
            if any(word.text.upper() == field.upper() for word in line):
                taxes.append(find_taxes(lines, index, field))
                break

    return {
        'sub_total': sub_total,
        'taxes': taxes,
        'grand_total': grand_total
    }

def find_amount(lines, index, field):
    for word in lines[index]:
        if word.is_money():
            return word.numeric_money_amount()

    # if couldn't find amout, search next row
    for word in lines[index+1]:
        if word.is_money():
            return word.numeric_money_amount()

def find_taxes(lines, index, field):
    possible_amounts = []
    for word in lines[index]:
        if not word.is_percentage() and word.is_money():
            possible_amounts.append(word.numeric_money_amount())

    # try looking at the next amount
    if not possible_amounts:
        for word in lines[index+1]:
            if not word.is_percentage() and word.is_money():
                possible_amounts.append(word.numeric_money_amount())

    if not possible_amounts:
        return {}
    # temp return smallest tax amount
    return { 'name': field, 'amount': sorted(possible_amounts)[0] }

def analyze(image_uri):
    # Instantiates a client
    client = vision.ImageAnnotatorClient()
    annotated_image_response = client.annotate_image({
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
    generate_receipt(annotated_image_response)

analyze(
    "https://cdn0.opinion-corp.com/review-media/pictures/c1/2d/3993/best-buy_best-buy-discontinued-service-of-my-8-month-old-item-20110416232667_c12d-gallery.jpeg")