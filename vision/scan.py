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


def build(annotated_image_response):
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
                taxes.append(find_taxes(lines, index, field, sub_total))
                break

    # The most important part of the receipt of the total.
    # If we could not find an amount, return the highest found amount
    if not grand_total or not grand_total.numeric_money_amount:
        largest_amount = Word('0.00')
        for line in lines:
            for word in line:
                if word.is_money() and word.numeric_money_amount() > largest_amount.numeric_money_amount():
                    largest_amount = word

        return {
            'sub_total': largest_amount.numeric_money_amount(),
            'taxes': [],
            'grand_total': largest_amount.numeric_money_amount()
        }
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


def find_taxes(lines, index, field, sub_total):
    # A safe assumption to make is that the taxes will be lower than the
    # subtotal. Often receipts have "X% of SUBTOTAL" as a line item.
    # We want to ignore any amounts that are >= to the subtotal
    word = search_for_amount(lines[index], ignore_percentage=True)
    if word and eligible_tax_amount(word, sub_total):
        return { 'name': field, 'amount': word.numeric_money_amount() }

    word = search_for_amount(lines[index + 1], ignore_percentage=True)
    if word and eligible_tax_amount(word, sub_total):
        return { 'name': field, 'amount': word.numeric_money_amount() }

    word = search_for_amount(lines[index  - 1], ignore_percentage=True)
    if word and eligible_tax_amount(word, sub_total):
        return { 'name': field, 'amount': word.numeric_money_amount() }

    return {}

def eligible_tax_amount(tax_amount, sub_total):
    # if subtotal is 0, comparing the tax amount isn't useful
    if not sub_total.numeric_money_amount():
        return True

    # most likely did not pick out the right amount
    if sub_total.numeric_money_amount() < tax_amount.numeric_money_amount():
        return False

    return True

def search_for_amount(line, ignore_percentage=False):
    line.reverse()
    for word in line:
        if ignore_percentage and word.is_percentage():
            continue
        if word.is_money():
            return word
