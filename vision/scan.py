from decimal import Decimal
from google.cloud import vision
from vision.word import Word
from vision.constants import GRAND_TOTAL_FIELDS, SUBTOTAL_FIELDS, TAX_FIELDS


def scan(image_uri):
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
    return build(annotated_image_response)


def scan_file(file_path):
    # Instantiates a client
    with open(file_path, 'rb') as fp:
        data = fp.read()
        return scan_content(data)


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
            'grand_total': '0.00',
            'taxes': []
        }
    description = annotated_image_response.text_annotations[0].description
    lines = build_lines(description)
    return build_receipt(lines)


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
    grand_total = Word('0.00')
    sub_total = Word('0.00')
    taxes = []
    grand_total_line = None
    sub_total_line = None

    for index, line in enumerate(lines):
        for field in GRAND_TOTAL_FIELDS:
            if any(word.text.upper() == field.upper() for word in line):
                grand_total_line, grand_total = find_total(lines, index)
                break
        if grand_total.numeric_money_amount():
            break

    if grand_total_line:
        # Look for the next highest number before the grand total
        for index, line in enumerate(lines[:grand_total_line]):
            for field in SUBTOTAL_FIELDS:
                if any(word.text.upper() == field.upper() for word in line):
                    sub_total_line, sub_total = find_total(lines, index, ignore_amount=grand_total)
                    break
            if sub_total.numeric_money_amount():
                break

    if grand_total_line and sub_total_line:
        tax_lines = lines[sub_total_line + 1:grand_total_line]
        taxes = find_taxes(tax_lines, sub_total, grand_total)
        # taxes.append(find_taxes(lines, grand_total_line, sub_total_line, field, grand_total, sub_total))

    return {
        'grand_total': grand_total.numeric_money_amount(),
        'sub_total': sub_total.numeric_money_amount(),
        'taxes': taxes
    }

def find_total(lines, index, ignore_amount=None):
    total = search_for_amount(lines[index])
    if total:
        return index, total

    # The most important part of the receipt of the total.
    # If we could not find it, try a weaker alterative

    # scan the document for the highest money amount
    amounts = []
    for line_number, line in enumerate(lines[index:]):
        for word in line:
            if word.is_money():
                if ignore_amount and word.numeric_money_amount() == ignore_amount.numeric_money_amount:
                    continue

                amounts.append({
                    'line_number': index + line_number,
                    'word': word
                })

    if amounts:
        amounts = list(filter(lambda x: x["word"].numeric_money_amount() is not None, amounts))
        if ignore_amount:
            amounts = list(filter(lambda x: x["word"].numeric_money_amount() != ignore_amount.numeric_money_amount(), amounts))
        amounts.sort(key=lambda x: x["word"].numeric_money_amount(), reverse=True)
        return amounts[0]['line_number'], amounts[0]['word']

    return 0, Word('0.00')


def find_taxes(lines, sub_total, grand_total):
    # A safe assumption to make is that the taxes will be lower than the
    # subtotal. Often receipts have "X% of SUBTOTAL" as a line item.
    # We want to ignore any amounts that are >= to the subtotal

    taxes = []
    for line in lines:
        word = search_for_amount(line, ignore_percentage=True)
        if word and eligible_tax_amount(word, sub_total, grand_total):
            taxes.append(word)

    return taxes

def eligible_tax_amount(tax_amount, sub_total, grand_total):
    # if grand_total is 0, comparing the tax amount isn't useful
    if not grand_total.numeric_money_amount():
        return True

    # ignore zero dollar taxes
    if tax_amount.numeric_money_amount() == Decimal('0.00'):
        return False

    # most likely did not pick out the right amount
    if grand_total.numeric_money_amount() <= tax_amount.numeric_money_amount():
        return False

    # most likely did not pick out the right amount
    if sub_total.numeric_money_amount() <= tax_amount.numeric_money_amount():
        return False

    return True

def search_for_amount(line, ignore_percentage=False):
    for word in line:
        if ignore_percentage and word.is_percentage():
            continue
        if word.is_money():
            return word
