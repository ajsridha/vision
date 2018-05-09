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

def scan(annotated_image_response):
    description = annotated_image_response.text_annotations[0].description
    print(description)
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
    grand_total = Word('')
    sub_total = Word('')
    taxes = []

    for index, line in enumerate(lines):
        for field in SUBTOTAL_FIELDS:
            if any(word.text.upper() == field.upper() for word in line):
                sub_total = find_amount(lines, index)
                break

    for index, line in enumerate(lines):
        for field in GRAND_TOTAL_FIELDS:
            if any(word.text.upper() == field.upper() for word in line):
                grand_total = find_amount(lines, index)
                break

    for index, line in enumerate(lines):
        for field in TAX_FIELDS:
            if any(field.upper() in word.text.upper() for word in line):
                taxes.append(find_taxes(lines, index, field))
                break

    return {
        'sub_total': sub_total.numeric_money_amount(),
        'taxes': taxes,
        'grand_total': grand_total.numeric_money_amount()
    }

def find_amount(lines, index):
    word = search_for_amount(lines[index])
    if word:
        return word

    word = search_for_amount(lines[index + 1])
    if word:
        return word

    word = search_for_amount(lines[index - 1])
    if word:
        return word


def find_taxes(lines, index, field):
    word = search_for_amount(lines[index], ignore_percentage=True)
    if word:
        return { 'name': field, 'amount': word.numeric_money_amount() }

    word = search_for_amount(lines[index + 1], ignore_percentage=True)
    if word:
        return { 'name': field, 'amount': word.numeric_money_amount() }

    word = search_for_amount(lines[index  - 1], ignore_percentage=True)
    if word:
        return { 'name': field, 'amount': word.numeric_money_amount() }

    return {}

def search_for_amount(line, ignore_percentage=False):
    line.reverse()
    for word in line:
        if ignore_percentage and word.is_percentage():
            continue
        if word.is_money():
            return word


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
    scan(annotated_image_response)

analyze(
    "https://forum.smartcanucks.ca/attachments/canadian-deals-bragging-discussion/213580d1391211437-80-bars-dove-soap-4-57-loblaws-m_photo-3.jpg")