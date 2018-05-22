from urllib import request
from google.cloud import vision
from vision.algorithms.text_analysis import find_total_on_line
from vision.algorithms.largest_amount import find_largest_amount
from vision.word import Word
from vision.constants import GRAND_TOTAL_FIELDS, SUBTOTAL_FIELDS, TAX_FIELDS


def scan_file(file_path):
    # Instantiates a client
    with open(file_path, 'rb') as fp:
        data = fp.read()
        return scan_content(data)


def scan(image_uri):
    content = request.urlopen(image_uri).read()
    return scan_content(content)


def scan_content(content):
    # Instantiates a client
    client = vision.ImageAnnotatorClient()
    annotated_image_response = client.annotate_image({
        'image': {
            'content': content
        },
        'features': [
            {'type': vision.enums.Feature.Type.LOGO_DETECTION},
            {'type': vision.enums.Feature.Type.DOCUMENT_TEXT_DETECTION}
        ],
    })
    return build(annotated_image_response)


def build(annotated_image_response):
    if not annotated_image_response.text_annotations:
        return {
            'vendor': None,
            'grand_total': '0.00',
            'taxes': []
        }

    vendor = determine_vendor(annotated_image_response)
    grand_total, taxes = build_amounts(annotated_image_response)

    return {
        'vendor': vendor,
        'grand_total': grand_total,
        'taxes': taxes
    }


def determine_vendor(annotated_image_response):
    if not annotated_image_response.logo_annotations:
        return None

    return annotated_image_response.logo_annotations[0].description

def build_lines(description):
    lines = []
    for words in description.split('\n'):
        line = []
        for word in words.split(' '):
            word = Word(word)
            line.append(word)
        # print(line)
        lines.append(line)

    return lines


def build_amounts(annotated_image_response):
    lines = build_lines(
        annotated_image_response.text_annotations[0].description)
    grand_total = Word('0.00')
    taxes = []

    for index, line in enumerate(lines):
        for field in GRAND_TOTAL_FIELDS:
            if any(word.text.upper() == field.upper() for word in line):
                grand_total = find_total(lines, index)
                break
        if grand_total.numeric_money_amount():
            break

    for index, line in enumerate(lines):
        for field in TAX_FIELDS:
            if any(field.upper() in word.text.upper() for word in line):
                taxes.append(find_taxes(lines, index, field, grand_total))
                break

    return grand_total.numeric_money_amount(), taxes


def find_total(lines, index):
    total = find_total_on_line(lines, index)
    if total:
        return total

    total = find_largest_amount(lines, index)
    if total:
        return total


    return Word('0.00')


def find_taxes(lines, index, field, grand_total):
    # A safe assumption to make is that the taxes will be lower than the
    # subtotal. Often receipts have "X% of SUBTOTAL" as a line item.
    # We want to ignore any amounts that are >= to the subtotal
    word = search_for_amount(lines[index], ignore_percentage=True)
    if word and eligible_tax_amount(word, grand_total):
        return { 'name': field, 'amount': word.numeric_money_amount() }

    word = search_for_amount(lines[index + 1], ignore_percentage=True)
    if word and eligible_tax_amount(word, grand_total):
        return { 'name': field, 'amount': word.numeric_money_amount() }

    word = search_for_amount(lines[index  - 1], ignore_percentage=True)
    if word and eligible_tax_amount(word, grand_total):
        return { 'name': field, 'amount': word.numeric_money_amount() }

    return {}

def eligible_tax_amount(tax_amount, grand_total):
    # if grand_total is 0, comparing the tax amount isn't useful
    if not grand_total.numeric_money_amount():
        return True

    # most likely did not pick out the right amount
    if grand_total.numeric_money_amount() < tax_amount.numeric_money_amount():
        return False

    return True

def search_for_amount(line, ignore_percentage=False):
    for word in line:
        if ignore_percentage and word.is_percentage():
            continue
        if word.is_money():
            return word
