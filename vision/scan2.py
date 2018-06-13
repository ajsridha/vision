import os
import urllib
import json
import requests
import base64
import re
from datetime import datetime
from decimal import Decimal
from date_detector import Parser
from vision.word import Word
from vision.lines_extractor import LinesExtractor
from vision.receipt import Receipt
from vision.constants import GRAND_TOTAL_FIELDS, SUBTOTAL_FIELDS, TAX_FIELDS, CASH_FIELDS
from vision.constants import LOGO_DETECTION, TEXT_DETECTION
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
                        {'type': LOGO_DETECTION},
                        {'type': TEXT_DETECTION}
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
    lines = extractor.lines
    sub_total, taxes, grand_total = build_amounts(lines)
    # receipt['address'] = determine_address(lines)
    # receipt['vendor'] = determine_vendor(lines)
    # receipt['date'] = determine_date(lines)
    receipt['sub_total'] = sub_total
    receipt['grand_total'] = grand_total
    receipt['lines'] = lines
    receipt['extractor'] = extractor

    # if grand_total == Decimal('0.00'):
        # extractor.preview()
    for i, tax in enumerate(taxes):
        receipt['tax{}_amount'.format(i + 1)] = tax.numeric_money_amount()

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
            if line.contains(field):
                sub_total_line = line_number
                sub_total = Word(line.amount)
                break
        if sub_total.numeric_money_amount():
            break

    if sub_total_line:
        del lines_with_amounts[sub_total_line]

    for line_number, line in enumerate(lines_with_amounts):
        for field in GRAND_TOTAL_FIELDS:
            if line.contains(field) and \
                    line.not_contains("sub") and \
                    line.not_contains("tax") and \
                    line.not_contains("beverage") and \
                    line.not_contains("excl"):
                grand_total_line = line_number
                grand_total = Word(line.amount)
                break
        if grand_total.numeric_money_amount():
            break

    if grand_total_line:
        del lines_with_amounts[grand_total_line]

    if (not grand_total or grand_total.numeric_money_amount() == 0):
        if sub_total and sub_total.numeric_money_amount():
            grand_total = sub_total
        else:
            _, grand_total = find_largest_amount(lines_with_amounts, index=0)

    if not sub_total or not sub_total.numeric_money_amount():
        if grand_total and grand_total.numeric_money_amount() > 0:
            sub_total = grand_total

    taxes = []
    for line_number, line in enumerate(lines_with_amounts):
        for field in TAX_FIELDS:
            if line.contains(field) and line.amount:
                taxes.append(Word(line.amount))
                break

    return sub_total.numeric_money_amount(), taxes, grand_total.numeric_money_amount()

def find_largest_amount(lines, index, ignore_amount=None):
    cash_used = False
    for line in lines:
        for field in CASH_FIELDS:
            if line.contains(field):
                cash_used = True
                break

    amounts = []
    for line_number, line in enumerate(lines[index:]):
        if ignore_amount and line.decimal_amount == ignore_amount.numeric_money_amount:
            continue

        amounts.append({
            'line_number': index + line_number,
            'line': line
        })

    if amounts:
        if ignore_amount:
            amounts = list(filter(lambda x: x["line"].decimal_amount != ignore_amount.numeric_money_amount(), amounts))
        amounts.sort(key=lambda x: x["line"].decimal_amount, reverse=True)

        if cash_used and len(amounts) > 1:
            return amounts[1]['line_number'], Word(amounts[1]['line'].amount)

        if amounts:
            return amounts[0]['line_number'], Word(amounts[0]['line'].amount)

        return 0, Word('0.00')

    return 0, Word('0.00')


def has_price(line):
    return True if line.amount is not None else False
