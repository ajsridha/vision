import re
import datetime
from commonregex import CommonRegex
from decimal import Decimal
from date_detector import Parser
from datetime import datetime


class Line(object):
    def __init__(self, line):
        if type(line) is dict:
            self.text = line['text'].encode('utf-8').strip()
        else:
            self.text = line.encode('utf-8').strip()
        self.parsed_text = CommonRegex(self.text)

    @property
    def amount_field(self):
        if not self.amount:
            return ''

        return self.text.replace(self.amount, '')\
            .replace(':', '')\
            .replace('$', '')\
            .strip()

    @property
    def amount(self):
        results = self.money_regex().search(self.text.replace(",", ""))
        if results:
            return results.group(0)
        return None

    @property
    def decimal_amount(self):
        if self.amount:
            return Decimal(self.amount)
        return None

    @property
    def amounts(self):
        results = self.money_regex().search(self.text.replace(",", ""))
        if results:
            return results.group(0)
        return None

    @property
    def decimal_amounts(self):
        if self.amount:
            return Decimal(self.amount)
        return None

    @property
    def date(self):
        parser = Parser()
        dates = []
        for match in parser.parse(self.text):
            if match.date <= datetime.today().date():
                dates.append(match.date)

        if dates:
            dates.sort(reverse=True)
            return dates[0]

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
