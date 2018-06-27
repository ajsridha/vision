import base64
import logging
import os
import requests

from decimal import Decimal
from vision.constants import LOGO_DETECTION, TEXT_DETECTION
from vision.algorithms.new_line_detection.analyzer import NewLineAnalyzer
from vision.algorithms.scanner_detection.analyzer import ScannerAnalyzer
from vision.models.receipt import Receipt


log = logging.getLogger(__name__)


def scan(image_uri):
    response = requests.get(image_uri)
    image = Receipt(response.content)
    content = encode_file(response.content)
    return _scan_content(content, image)


def scan_file(file_path):
    # Instantiates a client
    with open(file_path, 'rb') as fp:
        content = fp.read()
        image = Receipt(content)
        content = encode_file(content)
        return _scan_content(content, image)


def scan_content(content):
    image = Receipt(content)
    content = encode_file(content)
    return _scan_content(content, image)


def _scan_content(content, image):
    google_api_key = os.environ.get('GOOGLE_API_KEY')
    if not google_api_key:
        raise Exception("Unable to find Google API Key")

    response = requests.post(
        'https://vision.googleapis.com/v1/images:annotate?key={}'.format(google_api_key),
        json={
            "requests": [{
                "image": {
                    "content": content
                },
                "features": [
                    {'type': LOGO_DETECTION},
                    {'type': TEXT_DETECTION}
                ]
            }]
        })

    if response.status_code != 200:
        log.info('Google Error. returned: %s', response.status_code)
        log.info(response.text)
        raise Exception("Google Error")

    data = response.json()['responses'][0]
    return build(data, image)


def encode_file(bytes):
    content = base64.b64encode(bytes)
    return content.decode('ascii')


def build(annotated_image_response, image):
    receipt = {
        'vendor': '',
        'date': None,
        'sub_total': None,
        'grand_total': None,
        'taxes': []
    }
    if not annotated_image_response.get('textAnnotations'):
        return receipt

    new_line_analyzer = NewLineAnalyzer(annotated_image_response)
    scanner_analyzyer = ScannerAnalyzer(annotated_image_response, image)
    sub_total, taxes, grand_total = scanner_analyzyer.build_amounts()

    receipt['address'] = new_line_analyzer.determine_address()
    vendor, types = new_line_analyzer.determine_vendor()
    receipt['vendor'] = vendor
    receipt['date'] = new_line_analyzer.determine_date()
    receipt['sub_total'] = sub_total
    receipt['taxes'] = taxes
    receipt['grand_total'] = grand_total
    receipt['types'] = grand_total

    receipt['analyzer'] = scanner_analyzyer

    return receipt
