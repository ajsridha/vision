from vision.algorithms.scanner_detection.scanner_extractor import ScannerExtractor
from vision.constants import GRAND_TOTAL_FIELDS, SUBTOTAL_FIELDS, TAX_FIELDS, CASH_FIELDS

class ScannerAnalyzer(object):
    def __init__(self, data, image):
        self.extractor = ScannerExtractor(data, image)
        self.lines = self.extractor.lines

    def build_amounts(self):
        grand_total = None
        sub_total = None
        taxes = []
        grand_total_line = 0
        sub_total_line = 0

        lines_with_amounts = list(filter(self.has_price, self.lines))
        for line_number, line in enumerate(lines_with_amounts):
            for field in SUBTOTAL_FIELDS:
                if line.contains(field):
                    sub_total_line = line_number
                    sub_total = line.decimal_amount
                    break
            if sub_total:
                break

        for line_number, line in enumerate(lines_with_amounts[sub_total_line + 1:]):
            for field in GRAND_TOTAL_FIELDS:
                if line.contains(field) and \
                        line.not_contains("sub") and \
                        line.not_contains("tax") and \
                        line.not_contains("beverage") and \
                        line.not_contains("excl"):
                    grand_total_line = line_number
                    grand_total = line.decimal_amount
                    break
            if grand_total:
                break

        # if (not grand_total or grand_total.numeric_money_amount() == 0):
        #     if sub_total and sub_total.numeric_money_amount():
        #         grand_total = sub_total
        #     else:
        #         _, grand_total = self.find_largest_amount(lines_with_amounts, index=0)

        # if not sub_total or not sub_total.numeric_money_amount():
        #     if grand_total and grand_total.numeric_money_amount() > 0:
        #         sub_total = grand_total

        # taxes = []
        # for line_number, line in enumerate(lines_with_amounts):
        #     for field in TAX_FIELDS:
        #         if line.contains(field) and line.amount:
        #             taxes.append(Word(line.amount))
        #             break

        return sub_total, taxes, grand_total

    def determine_taxes(self):
        found_amounts = []
        taxes = []
        lines_with_amounts = list(filter(self.has_price, self.lines))
        for line_number, line in enumerate(lines_with_amounts):
            if line.contains('Tax preparation'):
                continue

            if line.contains('Less tax'):
                continue

            if line.contains('Before tax'):
                continue

            for field in TAX_FIELDS:

                if line.contains(field) and line.amount:
                    if line.amount in found_amounts:
                        continue


                    found_amounts.append(line.amount)
                    taxes.append({
                        'name': field,
                        'amount': line.decimal_amount
                    })
        return taxes

    def find_largest_amount(self, lines, index, ignore_amount=None):
        cash_used = False
        for line in lines:
            for field in CASH_FIELDS:
                if line.contains(field):
                    cash_used = True
                    break

        amounts = []
        for line_number, line in enumerate(lines[index:]):
            if ignore_amount and line.decimal_amount == ignore_amount.numeric_money_amount:
                continue

            amounts.append({
                'line_number': index + line_number,
                'line': line
            })

        if amounts:
            if ignore_amount:
                amounts = list(filter(lambda x: x["line"].decimal_amount != ignore_amount.numeric_money_amount(), amounts))
            amounts.sort(key=lambda x: x["line"].decimal_amount, reverse=True)

            if cash_used and len(amounts) > 1:
                return amounts[1]['line_number'], Word(amounts[1]['line'].amount)

            if amounts:
                return amounts[0]['line_number'], Word(amounts[0]['line'].amount)

            return 0, Word('0.00')

        return 0, Word('0.00')


    def has_price(self, line):
        return True if line.amount is not None else False
