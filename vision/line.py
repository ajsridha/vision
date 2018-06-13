import re
from commonregex import CommonRegex
from decimal import Decimal


class Line(object):
    def __init__(self, line):
        self.text = line['text']
        self.parsed_text = CommonRegex(self.text)

    @property
    def amount(self):
        results = self.money_regex().search(self.text)
        if results:
            return results.group(0)
        return None

    @property
    def decimal_amount(self):
        if self.amount:
            return Decimal(self.amount)
        return None

    @property
    def date(self):
        return self.parsed_text.dates[0] if self.parsed_text.dates else None

    @property
    def address(self):
        return self.parsed_text.street_addresses[0] if self.parsed_text.street_addresses else None

    def contains(self, text):
        return text.upper() in self.text.upper()

    def not_contains(self, text):
        return text.upper() not in self.text.upper()

    def money_regex(self):
        return re.compile(u'([0-9]{1,3}(?:,?[0-9]{3})*(?:\.[0-9]{2}$))')

    def __repr__(self):
        return self.text
