import sys
from vision.scan import scan
from prettytable import PrettyTable

def main():
    if len(sys.argv) != 2:
        print("USAGE: python ocr.py url")
        exit()
    url = sys.argv[1]
    expense = scan(url)
    results = PrettyTable(['Field', 'Result'])

    results.add_row(['Vendor', expense['vendor']])
    results.add_row(['Date', expense['date']])
    results.add_row(['Sub Total', expense['sub_total']])
    for tax in expense['taxes']:
        results.add_row([
            tax['name'],
            tax['amount']
        ])
    results.add_row(['Grand Total', expense['grand_total']])

    print(results)

if __name__ == "__main__":
    main()
