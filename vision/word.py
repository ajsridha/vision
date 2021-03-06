import re
from decimal import Decimal


class Word():
    def __init__(self, text):
        self.text = self.clean(text)

    def clean(self, text):
        # remove any non alpha numeric characters, decimals and dash
        return re.sub(r'[^a-zA-Z0-9.,\-\%]', '', text)

    def is_money(self):
        pattern = re.compile('^(-?\$?(\d)*(\.|\,)(\d)+$)')
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
            if char in [".", '-'] or pattern.match(char):
                number = number + char
            if char == ",":
                number = number + "."
        try:
            return Decimal(number)
        except:
            return None

    def __repr__(self):
        if self.is_money():
            str(self.numeric_money_amount())

        return self.text
