import io
import os
import requests
from PIL import Image, ImageDraw
from enum import Enum

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

from commands.block_command import BlockCommand


client = vision.ImageAnnotatorClient()

receipts = [
    'http://www.researchpaperspot.com/wp-content/uploads/2017/09/home-depot-receipt-template-professional-templates-for-home-depot-receipt-template.jpg',
    'https://igx.4sqi.net/img/general/600x600/42022189_iVNqS0PnOi_6vpTmmdURFIqjuW9DIPw6aX011Lktao0.jpg',
    'https://i.imgur.com/mIuLkAF.png',
    'https://i1.wp.com/fsatips.com/wp-content/uploads/2016/04/health_receipt_target.jpg', #calculates tax wrong
    'https://thewineraconteur.files.wordpress.com/2015/06/lcbo-receipt-612151.jpg', # can't find total,
    'https://forum.smartcanucks.ca/attachments/canadian-coupons/57241d1304383489-yes-you-can-stack-sof-newton-nordel-receipt-pic-scan_pic0001.jpg', # fails on coupons
    'http://receiptz.tk/wp-content/uploads/2018/03/walmart-receipt-template-walmart-receipt-template-template-for-walmart-receipt-template.jpg', # picks wrong number

]


for index, receipt in enumerate(receipts):
    google_response = client.annotate_image({
        'image': {
            'source': {
                'image_uri': receipt
            },
        },
        'features': [
            {'type': vision.enums.Feature.Type.LOGO_DETECTION},
            {'type': vision.enums.Feature.Type.DOCUMENT_TEXT_DETECTION}
        ],
    })


    print('\n\nRECEIPT ' + str(index))
    full_text_response = BlockCommand().generate_receipt(google_response, print_entire_receipt=False)
