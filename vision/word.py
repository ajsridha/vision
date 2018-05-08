import re
import unicodedata

class Word():
    def __init__(self, text, bounding_box):
        self.is_number = False
        self.is_money = False
        self.text = self.clean(text)
        self.bounding_box = bounding_box

    def max_y(self):
        return max(self.bounding_box.vertices[2].y, self.bounding_box.vertices[3].y)

    def min_y(self):
        return min(self.bounding_box.vertices[0].y, self.bounding_box.vertices[1].y)

    def height(self):
        return self.max_y() - self.min_y()

    def clean(self, text):
        if text.startswith("$"):
            text = text[1:]
            self.is_money = True

        pattern = re.compile('^[+-]?[0-9]{1,3}(?:,?[0-9]{3})*\.[0-9]{2}$')
        if pattern.match(text):
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
