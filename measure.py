from decimal import Decimal
from vision.scan import scan
from prettytable import PrettyTable
import csv
import os
import sys

def check_receipt(image, expected_total):
    try:
        result = {
            'status': 'ok',
            'sub_total': 'Unknown',
            'taxes': 'Unknown'
        }
        url = "http://afn85.webfactional.com/receipts/{}".format(image)
        expense = scan(url)

        result['sub_total'] = str(expense['sub_total'])
        result['taxes'] = expense['taxes']
        actual_total = str(expense['grand_total'])
        result['total'] = {
            'expected': expected_total,
            'actual': expense['grand_total']
        }
        if actual_total != expected_total:
            if expected_total != "Fail" and actual_total != "0.00":
                result['status'] = 'failed'
            else:
                result['total']['actual'] = 'Fail'

        return result
    except KeyboardInterrupt:
        exit()
    except:
        result['total'] = {
            'expected': expected_total,
            'actual': 'Unknown'
        }
        result['status'] = 'failed'
        return result

def main():
    image_override = None
    if len(sys.argv) > 1:
        image_override = sys.argv[1]

    with open('measure.csv', 'r') as csvfile:
        num_success = 0
        num_receipts = 0
        image = 0
        total = 1
        results_table = PrettyTable(['#', 'Image', 'Result', 'Subtotal', 'Taxes', 'Total', 'Status'])
        receipts = csv.reader(csvfile, delimiter=',', quotechar='"')

        print('Progress:')
        for i, receipt in enumerate(receipts):
            if image_override and image_override != receipt[image]:
                    continue

            result = check_receipt(
                receipt[image],
                receipt[total]
            )
            results_table.add_row([
                i + 1,
                receipt[image],
                'Expected',
                '',
                '',
                result['total']['expected'],
                result['status']
            ])
            results_table.add_row([
                '',
                '',
                'Actual',
                result['sub_total'],
                result['taxes'],
                result['total']['actual'],
                ''
            ])
            results_table.add_row(['','','','','','',''])

            num_receipts = num_receipts + 1
            if result['status'] == 'failed':
                print('F', end='', flush=True)
                continue

            num_success = num_success + 1
            print('.', end='', flush=True)


        results_table.add_row(['','','','','','',''])
        results_table.add_row([
            'Results',
            "{}/{} Succeeded".format(num_success, num_receipts),
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
