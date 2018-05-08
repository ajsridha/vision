from decimal import Decimal
import unicodedata
from constants import GRAND_TOTAL_FIELDS, SUBTOTAL_FIELDS, TAX_FIELDS


class Word():
    def __init__(self, text, bounding_box):
        self.is_number = False
        self.is_money = False
        self.text = self.clean(text)
        self.bounding_box = bounding_box

    def height(self):
        vertices = self.bounding_box.vertices
        return vertices[2].y - vertices[0].y

    def clean(self, text):
        if text.startswith("$"):
            text = text[1:]
            self.is_money = True

        try:
            float(text)
            self.is_number = True
        except ValueError:
            pass

        try:
            unicodedata.numeric(text)
            self.is_number = True
        except (TypeError, ValueError):
            pass

        return text

class BlockCommand():

    def __init__(self):
        self.words = []
        self.lines = []

    def generate_receipt(self, annotated_image_response, print_entire_receipt=False):
        pages = annotated_image_response.full_text_annotation.pages
        self.words = self.build_words(annotated_image_response.full_text_annotation)
        self.lines = self.build_lines(self.words)

        if print_entire_receipt:
            for key in sorted(self.lines.keys()):
                for word in self.lines[key]:
                    print(word.text, end=" ")
                print("\n")

        self.print_total()

    def build_words(self, full_text_annotation):
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

                    words_in_document.append(
                        Word(text=string_representation, bounding_box=word.bounding_box))

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


    def build_lines(self, words):
        # sort all the words by x coordinate first, so we can ensure
        # reading order
        words = sorted(
            words,
            key=lambda k: k.bounding_box.vertices[0].x)

        lines_map = {}
        for word in words:
            key = word.bounding_box.vertices[0].y
            for y_coordinate in lines_map.keys():
                if abs(key - y_coordinate) < word.height():
                    key = y_coordinate
                    break

            if lines_map.get(key):
                lines_map[key].append(word)
            else:
                lines_map[key] = [word]

        return lines_map

    def print_total(self):
        targeted_words = []
        words_of_interest = []
        fields_of_interest = GRAND_TOTAL_FIELDS + SUBTOTAL_FIELDS + TAX_FIELDS

        for key in self.lines.keys():
            for index_of_word, word in enumerate(self.lines[key]):
                if str(word.text).upper() in (field.upper() for field in fields_of_interest):
                    targeted_words.append(word.text)
                    words_of_interest.extend(self.lines[key])

        # find a value for each targetted words
        proposed_amounts = []
        for word in words_of_interest:
            if word.is_number:
                proposed_amounts.append(word)

        if not proposed_amounts:
            print("Shit, failed.")
            return

        sorted_proposed_amounts = sorted(
            proposed_amounts,
            key=lambda k: Decimal(k.text))

        print("Total: " + sorted_proposed_amounts[-1].text)
        print("Tax: " + sorted_proposed_amounts[0].text)


    def search_for_amount(self):
        index_of_line, index_of_word = self.search_for_total()
        for word in self.lines[index_of_line]:
            if word.is_number:
                return word.text
