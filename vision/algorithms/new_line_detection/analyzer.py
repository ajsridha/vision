import os
import requests
import urllib
from datetime import datetime
from decimal import Decimal
from date_detector import Parser
from vision.word import Word
from vision.constants import GRAND_TOTAL_FIELDS, SUBTOTAL_FIELDS, TAX_FIELDS, CASH_FIELDS
from commonregex import CommonRegex


class NewLineAnalyzer(object):
    def __init__(self, annotated_image_response):
        self.annotated_image_response = annotated_image_response

    def determine_vendor(self):
        if self.annotated_image_response.get('logoAnnotations'):
            return self.annotated_image_response.get('logoAnnotations')[0].get('description')

        places_api_key = os.environ.get('GOOGLE_PLACES_API_KEY')
        if not places_api_key:
            return

        lines = self.build_lines(
            self.annotated_image_response.get('textAnnotations')[0].get('description'))

        search_query = ""
        enough_data = False
        for line in lines[0:10]:
            if len(line) >= 2:
                for word in line:
                    search_query = search_query + word.text + " "
                enough_data = enough_data + 1
                if enough_data > 2:
                    break

        response = requests.get(
            'https://maps.googleapis.com/maps/api/place/textsearch/json?query='
            + urllib.quote_plus(search_query)
            + "&key=" + places_api_key)

        data = response.json()
        if data.get('results') and data['results'][0].get('name'):
            return data['results'][0]['name']

    def determine_date(self):
        description = self.annotated_image_response.get('textAnnotations')[0].get('description')
        parser = Parser()
        dates = []
        for match in parser.parse(description):
            if match.date <= datetime.today().date():
                dates.append(match.date)

        if dates:
            dates.sort(reverse=True)
            return dates[0]

    def determine_address(self):
        description = self.annotated_image_response.get('textAnnotations')[0].get('description')
        parsed_text = CommonRegex(description.replace('\n', ' '))
        addresses = parsed_text.street_addresses
        if len(addresses):
            return addresses[0]
        return ''

    def build_lines(self, description):
        lines = []
        for words in description.split('\n'):
            line = []
            for word in words.split(' '):
                word = Word(word)
                line.append(word)
            lines.append(line)

        return lines

    def build_amounts(self):
        lines = self.build_lines(
            self.annotated_image_response.get('textAnnotations')[0].get('description'))
        grand_total = Word('0.00')
        sub_total = Word('')
        taxes = []
        grand_total_line = None
        sub_total_line = None

        for index, line in enumerate(lines):
            for field in GRAND_TOTAL_FIELDS:
                if any(word.text.upper() == field.upper() for word in line):
                    grand_total_line, grand_total = self.find_total(lines, index)
                    break
            if grand_total.numeric_money_amount():
                break

        # if we couldn't find the word total on the receipt, look for the largest
        # number
        if not grand_total or grand_total.numeric_money_amount() == 0:
            grand_total_line, grand_total = self.find_largest_amount(lines, index=0)

        if grand_total_line:
            # Look for the next highest number before the grand total
            for index, line in enumerate(lines[:grand_total_line]):
                for field in SUBTOTAL_FIELDS:
                    if any(word.text.upper() == field.upper() for word in line):
                        sub_total_line, sub_total = self.find_total(lines, index)
                        break
                if sub_total.numeric_money_amount():
                    break

        if grand_total_line and sub_total_line:
            tax_lines = lines[sub_total_line + 1:grand_total_line]
            taxes = self.find_taxes(tax_lines, sub_total, grand_total)

        if not sub_total.is_money():
            sub_total = grand_total

        return sub_total.numeric_money_amount(), taxes, grand_total.numeric_money_amount()


    def find_total(self, lines, index, ignore_amount=None):
        total = self.search_for_amount(lines[index])
        if total:
            return index, total

        return self.find_largest_amount(lines, index, ignore_amount)


    def find_largest_amount(self, lines, index, ignore_amount=None):
        # check for the presence of the word "cash". When a person pays by
        # cash, they usually make a payment that is equal to or more the total.
        # This will be useful so we don't pick the largest amount, but the second
        # largest amount
        cash_used = False
        for line in lines:
            for word in line:
                if word.text.upper() in CASH_FIELDS:
                    cash_used = True

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

            if cash_used and len(amounts) > 1:
                return amounts[1]['line_number'], amounts[1]['word']

            if amounts:
                return amounts[0]['line_number'], amounts[0]['word']

            return 0, Word('0.00')

        return 0, Word('0.00')

    def find_taxes(self, lines, sub_total, grand_total):
        # A safe assumption to make is that the taxes will be lower than the
        # subtotal. Often receipts have "X% of SUBTOTAL" as a line item.
        # We want to ignore any amounts that are >= to the subtotal

        taxes = []
        for line in lines:
            word = self.search_for_amount(line, ignore_percentage=True)
            if word and self.eligible_tax_amount(word, sub_total, grand_total):
                taxes.append(word.numeric_money_amount())

        return taxes

    def eligible_tax_amount(self, tax_amount, sub_total, grand_total):
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

    def search_for_amount(self, line, ignore_percentage=False):
        for word in line:
            if ignore_percentage and word.is_percentage():
                continue
            if word.is_money():
                return word
