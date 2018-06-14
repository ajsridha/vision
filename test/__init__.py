import logging
from vision.scan import scan
from unittest import TestCase

logging.basicConfig()
vcr_log = logging.getLogger("vcr")
vcr_log.setLevel(logging.INFO)
logging.getLogger("urllib3").setLevel(logging.WARNING)

class BaseTestCase(TestCase):
    def scan_expense(self, image):
        url = "http://afn85.webfactional.com/receipts/{}".format(image)
        return scan(url)

    def debug(self, expense):
        print(expense)
        if 'analyzer' in expense:
            print(expense['analyzer'].extractor.lines)
            expense['analyzer'].extractor.preview_original()
