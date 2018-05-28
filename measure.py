from decimal import Decimal
from vision.scan import scan
from prettytable import PrettyTable
from termcolor import colored
import csv
import os
import sys

IMAGE_FIELD = 0
VENDOR_FIELD = 1
SUBTOTAL_FIELD = 2
TAX1_NAME_FIELD = 3
TAX1_AMOUNT_FIELD = 4
TAX2_NAME_FIELD = 5
TAX2_AMOUNT_FIELD = 6
TAX3_NAME_FIELD = 7
TAX3_AMOUNT_FIELD = 8
TOTAL_FIELD = 9
DATE_FIELD = 10

expense_csv_mapping = {
    'vendor': VENDOR_FIELD,
    'date': DATE_FIELD,
    'sub_total': SUBTOTAL_FIELD,
    'tax1_amount': TAX1_AMOUNT_FIELD,
    'tax2_amount': TAX2_AMOUNT_FIELD,
    'tax3_amount': TAX3_AMOUNT_FIELD,
    'grand_total': TOTAL_FIELD
}

def check_receipt(expected):
    status = True
    url = "http://afn85.webfactional.com/receipts/{}".format(expected[IMAGE_FIELD])

    expense = scan(url)

    num_fields = 0
    num_correct = 0
    for field, csv_field_index in expense_csv_mapping.items():
        if not expected[csv_field_index]:
            continue

        num_fields += 1
        if expected[csv_field_index].lower() == str(expense[field]).lower():
            num_correct += 1
            continue

    if not num_correct:
        if not expense['grand_total']:
            return 100, expense
        return 0.0, expense

    return round(num_correct/num_fields * 100, 1), expense

def main():
    image_override = None
    if len(sys.argv) > 1:
        image_override = sys.argv[1]

    with open('measure.csv', 'r') as csvfile:
        num_success = 0
        num_receipts = 0

        results_table = PrettyTable(['#', 'Image', 'Result', 'Vendor', 'Date', 'Subtotal', 'Tax1', 'Tax2', 'Tax3', 'Total', 'Status'])
        receipts = csv.reader(csvfile, delimiter=',', quotechar='"')

        print('Progress:')
        for i, receipt in enumerate(receipts):
            if image_override and image_override != receipt[IMAGE_FIELD]:
                    continue

            text = colored(" {}) {}: ".format(i+1, receipt[IMAGE_FIELD]), 'blue')
            print(text, end='')
            status, result = check_receipt(receipt)

            num_success += status

            results_table.add_row([
                i + 1,
                receipt[IMAGE_FIELD],
                'Expected',
                receipt[VENDOR_FIELD],
                receipt[DATE_FIELD],
                receipt[SUBTOTAL_FIELD],
                receipt[TAX1_AMOUNT_FIELD],
                receipt[TAX2_AMOUNT_FIELD],
                receipt[TAX2_AMOUNT_FIELD],
                receipt[TOTAL_FIELD],
                "✔" if status == 1 else "{} %".format(status)
            ])
            results_table.add_row([
                '',
                '',
                'Actual',
                result['vendor'] if result['vendor'] else '',
                result['date'] if result['date'] else '',
                result['sub_total'] if result['sub_total'] else '',
                result['tax1_amount'],
                result['tax2_amount'],
                result['tax2_amount'],
                result['grand_total'] if result['grand_total'] else '',
                ''
            ])
            results_table.add_row(['-','-','-','-','-','-','-','-','-','-','-'])

            num_receipts = num_receipts + 1
            if status != 100:
                text = colored("{}%".format(status), 'red')
                print(text, flush=True)
                continue

            print('✔', flush=True)


        correct_percentage = (num_success / (num_receipts * 100)) * 100
        results_table.add_row(['','','','','','','','','','',''])
        results_table.add_row([
            'Results',
            "{}% Succeeded".format(round(correct_percentage, 1)),
            '',
            '',
            '',
            '',
            '',
            '',
            '',
            '',
            ''
        ])
        print('\n\nSummary:')
        print(results_table)


if __name__ == "__main__":
    main()
