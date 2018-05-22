from decimal import Decimal
from vision.scan import scan
from prettytable import PrettyTable
import csv
import os
import sys

def check_receipt(image, expected_total):
    try:
        result = {
            'status': 'ok'
        }
        url = "http://afn85.webfactional.com/receipts/{}".format(image)
        expense = scan(url)
        # if str(expense['sub_total']) != sub_total:
        #     errors.append("sub_total (ex: {}, ac: {})".format(sub_total, expense['sub_total']))

        # taxes = expense['taxes']
        # if tax1:
        #     if len(taxes) == 0:
        #         errors.append("tax1 missing")
        #     elif taxes[0] != tax1:
        #         errors.append("tax1 (ex: {}, ac: {})".format(tax1, taxes[0]))

        # if tax2:
        #     if len(taxes) < 2:
        #         errors.append("tax2 missing")
        #     elif taxes[1] != tax2:
        #         errors.append("tax2 (ex: {}, ac: {})".format(tax2, taxes[1]))

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
        results_table = PrettyTable(['#', 'Image', 'Expected Total', 'Actual Total', 'Status'])
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
                result['total']['expected'],
                result['total']['actual'],
                result['status']
            ])

            num_receipts = num_receipts + 1
            if result['status'] == 'failed':
                print('F', end='', flush=True)
                continue

            num_success = num_success + 1
            print('.', end='', flush=True)


        results_table.add_row(['','','','',''])
        results_table.add_row([
            'Results',
            "{}/{} Succeeded".format(num_success, num_receipts),
            '',
            '',
            ''
        ])
        print('\n\nSummary:')
        print(results_table)


if __name__ == "__main__":
    main()
