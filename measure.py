from decimal import Decimal
from vision.scan import scan
import csv
import os
import sys

def check_receipt(image, total):
    try:
        errors = []
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

        if str(expense['grand_total']) != total:
            if total != "Fail" and str(expense['grand_total'] != "0.00":
                errors.append("total (expected: {} != actual: {})".format(total, expense['grand_total']))
        return errors
    except:
        return ["Scan fail"]

def main():
    filename = 'measure.csv'
    if len(sys.argv) > 1:
        filename = sys.argv[1]

    with open(filename, 'r') as csvfile:
        num_success = 0
        num_receipts = 0
        image = 0
        total = 1

        receipts = csv.reader(csvfile, delimiter=',', quotechar='"')
        for i, receipt in enumerate(receipts):

            errors = check_receipt(
                receipt[image],
                receipt[total]
            )
            print("Receipt {}) {} status:".format(i + 1, receipt[image]))
            if len(errors) == 0:
                num_success = num_success + 1
                print("Success")
            else:
                pretty_errors = " | ".join(errors)
                print("Failures: {}".format(pretty_errors))
            num_receipts = num_receipts + 1

        print ("{}/{}".format(num_success, num_receipts))


if __name__ == "__main__":
    main()
