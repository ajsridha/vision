import unicodedata
from constants import GRAND_TOTAL_FIELDS


class Word():
    def __init__(self, text, bounding_box):
        self.is_number = False
        self.is_money = False
        self.text = self.clean(text)
        self.bounding_box = bounding_box

    def average_x_position(self):
        vertices = self.bounding_box.vertices
        return (vertices[1].x + vertices[0].x) / 2

    def average_y_position(self):
        vertices = self.bounding_box.vertices
        return (vertices[2].y + vertices[0].y) / 2

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

    def generate_receipt(self, annotated_image_response):
        pages = annotated_image_response.full_text_annotation.pages
        self.words = self.build_words(annotated_image_response.full_text_annotation)
        self.lines = self.build_lines(self.words)

        for line in self.lines:
            for word in line:
                print(word.text, end=" ")
            print("\n")

        amount = self.search_for_amount()
        print("Total: " + amount)

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
                if word.is_number and words_in_document[index+1].text == "." and words_in_document[index+2].is_number:
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
        lines = []
        current_line = []

        y_position = words[0].average_y_position()
        previous_height = words[0].height()

        for word in words:
            # the 10 is an episolon value
            if word.average_y_position() - y_position > previous_height - 10:
                lines.append(current_line)
                current_line = []

            current_line.append(word)
            y_position = word.average_y_position()
            previous_height = word.height()

        return lines

    def search_for_total(self):
        for index_of_line, line in enumerate(self.lines):
            for index_of_word, word in enumerate(line):
                if str(word.text).upper() in (field.upper() for field in GRAND_TOTAL_FIELDS):
                    return index_of_line, index_of_word

    def search_for_amount(self):
        index_of_line, index_of_word = self.search_for_total()
        for word in self.lines[index_of_line]:
            if word.is_number:
                return word.text
