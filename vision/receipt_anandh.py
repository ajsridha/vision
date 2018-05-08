from word import Word
from decimal import Decimal
from constants import GRAND_TOTAL_FIELDS, SUBTOTAL_FIELDS, TAX_FIELDS
from google.cloud import vision

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


def generate_receipt(annotated_image_response, print_entire_receipt=False):
    pages = annotated_image_response.full_text_annotation.pages
    words = build_words(annotated_image_response.full_text_annotation)
    lines = build_lines(words)

    if print_entire_receipt:
        for key in sorted(lines.keys()):
            for word in lines[key]:
                print(word.text, end=" ")
            print("\n")

    print_total(lines)

def build_words(full_text_annotation):
    words_in_document = []
    pages = full_text_annotation.pages
    # we only care about the first page, since receipts are usually one page
    blocks = pages[0].blocks
    for block in blocks:
        paragraphs = block.paragraphs
        for paragraph in paragraphs:
            words = paragraph.words
            for word in words:
                string_representation = ""
                for symbol in word.symbols:
                    string_representation = string_representation + symbol.text

                if string_representation.strip():
                    words_in_document.append(
                        Word(text=string_representation.strip(), bounding_box=word.bounding_box))

    # Goolge sometimes breaks aparts numbers. Stitch them back together
    fixed_words_in_document = []
    skip_indices = []
    for index in range(len(words_in_document)):
        if index in skip_indices:
            continue

        word = words_in_document[index]
        try:
            if word.is_number and words_in_document[index+1].text == "." and words_in_document[index+2].is_number and index + 2 < len(words_in_document):
                new_word = Word(
                    text=word.text + "." + words_in_document[index+2].text,
                    bounding_box=word.bounding_box)
                fixed_words_in_document.append(new_word)
                skip_indices.extend([index+1, index+2])
                continue
        except IndexError:
            pass

        fixed_words_in_document.append(word)

    return fixed_words_in_document


def build_lines(words):
    # sort all the words by x coordinate first, so we can ensure
    # reading order
    words = sorted(
        words,
        key=lambda k: k.bounding_box.vertices[0].x)

    lines_map = {}
    for word in words:
        key = word.max_y()
        for y_coordinate in lines_map.keys():
            if abs(key - y_coordinate) < word.height():
                key = y_coordinate
                break

        if lines_map.get(key):
            lines_map[key].append(word)
        else:
            lines_map[key] = [word]

    list_of_lines = []
    for key in sorted(lines_map.keys()):
        list_of_lines.append(lines_map[key])

    return list_of_lines

def print_total(lines):
    targeted_words = []
    words_of_interest = []
    fields_of_interest = GRAND_TOTAL_FIELDS + SUBTOTAL_FIELDS + TAX_FIELDS

    for index_of_line, line in enumerate(lines):
        for index_of_word, word in enumerate(line):
            if str(word.text).upper() in (field.upper() for field in fields_of_interest):
                targeted_words.append(word.text)
                words_of_interest.extend(line)
                # get nearby lines to account for slanted receipts
                if index_of_line + 1 < len(lines):
                    words_of_interest.extend(lines[index_of_line + 1])
                if index_of_line - 1 > 0:
                    words_of_interest.extend(lines[index_of_line - 1])

    # find a value for each targetted words
    proposed_amounts = []
    for word in set(words_of_interest):
        if word.is_money and word.is_number:
            proposed_amounts.append(word.text)

    if not proposed_amounts:
        print("Shit, failed.")
        return

    sorted_proposed_amounts = sorted(
        set(proposed_amounts),
        key=lambda k: Decimal(k))

    print("Total: " + sorted_proposed_amounts[-1])
    print("Tax: " + sorted_proposed_amounts[0])

analyze(
    "http://4xhost.club/wp-content/uploads/2017/09/walmart-receipt-mart-receipt-receipt-plan-template-business-plan-in-receipt-template-mart-receipt-tax-codes-walmart-receipt-policy-checking.jpg"
)