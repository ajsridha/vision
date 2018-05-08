# import vcr
from vision.receipt_anandh import analyze
from unittest import TestCase
from nose.tools import eq_

class VisionTest(TestCase):
    # @vcr.use_cassette('fixtures/vcr_cassettes/walmart.yaml')
    def test_walmart(self):
        expense = analyze(
            "http://4xhost.club/wp-content/uploads/2017/09/walmart-receipt-mart-receipt-receipt-plan-template-business-plan-in-receipt-template-mart-receipt-tax-codes-walmart-receipt-policy-checking.jpg"
        )
        eq_(expense, {
            'vendor': 'Walmart',
            'taxes': [
                {
                    'tax': 'TAX',
                    'amount': '0.28'
                }
            ],
            'total': '4.03'
          })

    # @vcr.use_cassette('fixtures/vcr_cassettes/target.yaml')
    # def test_target(self):
    #     expense = self.analyzer.analyze(
    #         "https://i1.wp.com/fsatips.com/wp-content/uploads/2016/04/health_receipt_target.jpg"
    #     )
    #     eq_(expense, {
    #         'vendor': 'Target',
    #         'taxes': [],
    #         'total': '43.59'
    #       })


