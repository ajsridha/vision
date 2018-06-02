import os
import urllib
import json
import requests
import base64
import re
from datetime import datetime
from decimal import Decimal
from google.cloud import vision
from date_detector import Parser
from vision.word import Word
from vision.lines_extractor import LinesExtractor
from vision.receipt import Receipt
from vision.constants import GRAND_TOTAL_FIELDS, SUBTOTAL_FIELDS, TAX_FIELDS, CASH_FIELDS
from commonregex import CommonRegex


def scan_file(file_path):
    # Instantiates a client
    with open(file_path, 'rb') as fp:
        content = fp.read()
        image = Receipt(content)
        content = encode_file(content)
        return scan_content(content, image)


def scan_content(content, image):
    google_api_key = os.environ.get('GOOGLE_API_KEY')
    if not google_api_key:
        raise Exception("Unable to find Google API Key")

    response = requests.post(
        'https://vision.googleapis.com/v1/images:annotate?key={}'.format(google_api_key),
        json={
                "requests": [{
                    "image": {
                        "content": content
                    },
                    "features": [
                        {'type': vision.enums.Feature.Type.LOGO_DETECTION},
                        {'type': vision.enums.Feature.Type.DOCUMENT_TEXT_DETECTION}
                    ]
                }]
            })

    if response.status_code != 200:
        raise Exception("Google Error")

    data = response.json()['responses'][0]
    return build(data, image)


def scan(image_uri):
    response = requests.get(image_uri)
    image = Receipt(response.content)
    content = encode_file(response.content)
    return scan_content(content, image)


def encode_file(bytes):
    content = base64.b64encode(bytes)
    return content.decode('ascii')

def build(data, image):
    receipt = {
        'vendor': '',
        'date': '',
        'sub_total': '',
        'tax1_amount': '',
        'tax2_amount': '',
        'tax3_amount': '',
        'grand_total': ''
    }
    if not data.get('textAnnotations'):
        return receipt

    extractor = LinesExtractor(data, image)
    lines = extractor.text()
    sub_total, taxes, grand_total = build_amounts(lines)
    # extractor.preview_original()
    # extractor.preview()
    # receipt['address'] = determine_address(lines)
    # receipt['vendor'] = determine_vendor(lines)
    # receipt['date'] = determine_date(lines)
    receipt['sub_total'] = sub_total
    receipt['grand_total'] = grand_total
    receipt['lines'] = lines
    receipt['extractor'] = extractor


    # if grand_total == Decimal('0.00'):
        # extractor.preview()
    # for i, tax in enumerate(taxes):
    #     receipt['tax{}_amount'.format(i + 1)] = tax

    return receipt

def build_amounts(lines):
    grand_total = Word('0.00')
    sub_total = Word('')
    taxes = []
    grand_total_line = None
    sub_total_line = None

    lines_with_amounts = list(filter(has_price, lines))
    for line_number, line in enumerate(lines_with_amounts):
        for field in SUBTOTAL_FIELDS:
            if field.upper() in line.upper():
                sub_total_line = line_number
                results = money_regex().findall(line)
                sub_total = Word(results[0].strip())
                break
        if sub_total.numeric_money_amount():
            break

    if sub_total_line:
        lines_with_amounts = lines_with_amounts[sub_total_line + 1:]
    for line_number, line in enumerate(lines_with_amounts):
        for field in GRAND_TOTAL_FIELDS:
            if field.upper() in line.upper():
                grand_total_line = line_number
                results = money_regex().findall(line)
                grand_total = Word(results[0].strip())
                break
        if grand_total.numeric_money_amount():
            break

    if sub_total_line and grand_total_line:
        lines_with_amounts = lines_with_amounts[:grand_total_line]

    taxes = []
    for line_number, line in enumerate(lines_with_amounts):
        for field in TAX_FIELDS:
            if field.upper() in line.upper():
                results = money_regex().findall(line)
                taxes.append(Word(results[0].strip()))
                break

    return sub_total.numeric_money_amount(), taxes, grand_total.numeric_money_amount()

def money_regex():
    return re.compile(u'\s?[+-]?[0-9]{1,3}(?:(?:,?[0-9]{3}))*(?:\.[0-9]{1,2})')

def has_price(text):
    results = money_regex().findall(text)
    if results:
        return True
    return False
