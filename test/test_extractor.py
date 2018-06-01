import vcr
from test import BaseTestCase
from nose.tools import eq_
from decimal import Decimal
from vision.scan2 import scan

class TestExtractor(BaseTestCase):
    def scan_expense(self, image):
        url = "http://afn85.webfactional.com/receipts/{}".format(image)
        return scan(url)

    @vcr.use_cassette('fixtures/vcr_cassettes/1.yaml', filter_query_parameters=['key'])
    def test_1(self):
        expense = self.scan_expense('3000057-11667.png')
        eq_(expense['sub_total'], Decimal("388.59"))
        eq_(expense['grand_total'], Decimal("420.69"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/2.yaml', filter_query_parameters=['key'])
    # def test_2(self):
    #     expense = self.scan_expense('3000060-26246.jpeg')
    #     import pdb; pdb.set_trace()
    #     eq_(expense['sub_total'], Decimal("56.81"))
    #     eq_(expense['grand_total'], Decimal("61.92"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/3.yaml', filter_query_parameters=['key'])
    # def test_3(self):
    #     expense = self.scan_expense('3000119-1132.jpeg')
    #     eq_(expense['sub_total'], Decimal("0.00"))
    #     eq_(expense['grand_total'], Decimal("0.00"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/4.yaml', filter_query_parameters=['key'])
    # def test_4(self):
    #     expense = self.scan_expense('3000119-4598605.jpeg')
    #     eq_(expense['sub_total'], Decimal("107.35"))
    #     eq_(expense['grand_total'], Decimal("107.35"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/5.yaml', filter_query_parameters=['key'])
    # def test_5(self):
    #     expense = self.scan_expense('3000119-5304795.jpeg')
    #     eq_(expense['sub_total'], Decimal("26.43"))
    #     eq_(expense['grand_total'], Decimal("27.75"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/6.yaml', filter_query_parameters=['key'])
    # def test_6(self):
    #     expense = self.scan_expense('3000119-804319.jpeg')
    #     eq_(expense['sub_total'], Decimal("156.05"))
    #     eq_(expense['grand_total'], Decimal("163.20"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/7.yaml', filter_query_parameters=['key'])
    # def test_7(self):
    #     expense = self.scan_expense('3000119-804383.jpeg')
    #     eq_(expense['sub_total'], Decimal("15.00"))
    #     eq_(expense['grand_total'], Decimal("15.75"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/8.yaml', filter_query_parameters=['key'])
    # def test_8(self):
    #     expense = self.scan_expense('3000138-1304099.jpeg')
    #     eq_(expense['sub_total'], Decimal("6.09"))
    #     eq_(expense['grand_total'], Decimal("6.09"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/9.yaml', filter_query_parameters=['key'])
    # def test_9(self):
    #     expense = self.scan_expense('3000138-2422.jpeg')
    #     eq_(expense['sub_total'], Decimal("9.28"))
    #     eq_(expense['grand_total'], Decimal("9.28"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/10.yaml', filter_query_parameters=['key'])
    # def test_10(self):
    #     expense = self.scan_expense('3000138-2463.jpeg')
    #     eq_(expense['sub_total'], Decimal("78.21"))
    #     eq_(expense['grand_total'], Decimal("78.21"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/11.yaml', filter_query_parameters=['key'])
    # def test_11(self):
    #     expense = self.scan_expense('3000138-298017.png')
    #     eq_(expense['sub_total'], Decimal("9.95"))
    #     eq_(expense['grand_total'], Decimal("9.95"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/12.yaml', filter_query_parameters=['key'])
    # def test_12(self):
    #     expense = self.scan_expense('3000171-119353.jpeg')
    #     eq_(expense['sub_total'], Decimal("63.08"))
    #     eq_(expense['grand_total'], Decimal("68.36"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/13.yaml', filter_query_parameters=['key'])
    # def test_13(self):
    #     expense = self.scan_expense('3000382-2771981.jpeg')
    #     eq_(expense['sub_total'], Decimal("18.57"))
    #     eq_(expense['grand_total'], Decimal("20.98"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/14.yaml', filter_query_parameters=['key'])
    # def test_14(self):
    #     expense = self.scan_expense('3000399-26743.jpeg')
    #     eq_(expense['sub_total'], Decimal("18.50"))
    #     eq_(expense['grand_total'], Decimal("18.50"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/15.yaml', filter_query_parameters=['key'])
    # def test_15(self):
    #     expense = self.scan_expense('3000464-1271.jpeg')
    #     eq_(expense['sub_total'], Decimal("0.00"))
    #     eq_(expense['grand_total'], Decimal("0.00"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/16.yaml', filter_query_parameters=['key'])
    # def test_16(self):
    #     expense = self.scan_expense('3000495-11665.jpeg')
    #     eq_(expense['sub_total'], Decimal("0.00"))
    #     eq_(expense['grand_total'], Decimal("0.00"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/17.yaml', filter_query_parameters=['key'])
    # def test_17(self):
    #     expense = self.scan_expense('3000527-1332.jpeg')
    #     eq_(expense['sub_total'], Decimal("0.00"))
    #     eq_(expense['grand_total'], Decimal("0.00"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/18.yaml', filter_query_parameters=['key'])
    # def test_18(self):
    #     expense = self.scan_expense('3000533-1153196.png')
    #     eq_(expense['sub_total'], Decimal("9.50"))
    #     eq_(expense['grand_total'], Decimal("9.50"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/19.yaml', filter_query_parameters=['key'])
    # def test_19(self):
    #     expense = self.scan_expense('3000533-17606.png')
    #     eq_(expense['sub_total'], Decimal("5.80"))
    #     eq_(expense['grand_total'], Decimal("5.80"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/20.yaml', filter_query_parameters=['key'])
    # def test_20(self):
    #     expense = self.scan_expense('3000533-2350236.png')
    #     eq_(expense['sub_total'], Decimal("55.83"))
    #     eq_(expense['grand_total'], Decimal("55.83"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/21.yaml', filter_query_parameters=['key'])
    # def test_21(self):
    #     expense = self.scan_expense('3000533-2350240.png')
    #     eq_(expense['sub_total'], Decimal("4.84"))
    #     eq_(expense['grand_total'], Decimal("4.84"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/22.yaml', filter_query_parameters=['key'])
    # def test_22(self):
    #     expense = self.scan_expense('3000533-2703411.png')
    #     eq_(expense['sub_total'], Decimal("0.00"))
    #     eq_(expense['grand_total'], Decimal("0.00"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/23.yaml', filter_query_parameters=['key'])
    # def test_23(self):
    #     expense = self.scan_expense('3000533-42941.jpeg')
    #     eq_(expense['sub_total'], Decimal("21.18"))
    #     eq_(expense['grand_total'], Decimal("22.93"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/24.yaml', filter_query_parameters=['key'])
    # def test_24(self):
    #     expense = self.scan_expense('3000542-12521.jpeg')
    #     eq_(expense['sub_total'], Decimal("99.96"))
    #     eq_(expense['grand_total'], Decimal("108.71"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/25.yaml', filter_query_parameters=['key'])
    # def test_25(self):
    #     expense = self.scan_expense('3000558-200917.jpeg')
    #     eq_(expense['sub_total'], Decimal("49.99"))
    #     eq_(expense['grand_total'], Decimal("53.99"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/26.yaml', filter_query_parameters=['key'])
    # def test_26(self):
    #     expense = self.scan_expense('3000582-2747685.png')
    #     eq_(expense['sub_total'], Decimal("1.90"))
    #     eq_(expense['grand_total'], Decimal("2.00"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/27.yaml', filter_query_parameters=['key'])
    # def test_27(self):
    #     expense = self.scan_expense('3000618-1995.jpeg')
    #     eq_(expense['sub_total'], Decimal("25.00"))
    #     eq_(expense['grand_total'], Decimal("25.00"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/28.yaml', filter_query_parameters=['key'])
    # def test_28(self):
    #     expense = self.scan_expense('3000618-2156.jpeg')
    #     eq_(expense['sub_total'], Decimal("37.80"))
    #     eq_(expense['grand_total'], Decimal("39.69"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/29.yaml', filter_query_parameters=['key'])
    # def test_29(self):
    #     expense = self.scan_expense('3000618-4988077.jpeg')
    #     eq_(expense['sub_total'], Decimal("31.12"))
    #     eq_(expense['grand_total'], Decimal("32.98"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/30.yaml', filter_query_parameters=['key'])
    # def test_30(self):
    #     expense = self.scan_expense('3000618-5267057.jpeg')
    #     eq_(expense['sub_total'], Decimal("10.80"))
    #     eq_(expense['grand_total'], Decimal("11.45"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/31.yaml', filter_query_parameters=['key'])
    # def test_31(self):
    #     expense = self.scan_expense('3000715-1999.png')
    #     eq_(expense['sub_total'], Decimal("136.46"))
    #     eq_(expense['grand_total'], Decimal("136.46"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/32.yaml', filter_query_parameters=['key'])
    # def test_32(self):
    #     expense = self.scan_expense('3000753-1980112.png')
    #     eq_(expense['sub_total'], Decimal("12.95"))
    #     eq_(expense['grand_total'], Decimal("12.95"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/33.yaml', filter_query_parameters=['key'])
    # def test_33(self):
    #     expense = self.scan_expense('3000793-2112957.jpeg')
    #     eq_(expense['sub_total'], Decimal("224.79"))
    #     eq_(expense['grand_total'], Decimal("254.01"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/34.yaml', filter_query_parameters=['key'])
    # def test_34(self):
    #     expense = self.scan_expense('3000793-2112982.jpeg')
    #     eq_(expense['sub_total'], Decimal("241.50"))
    #     eq_(expense['grand_total'], Decimal("272.90"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/35.yaml', filter_query_parameters=['key'])
    # def test_35(self):
    #     expense = self.scan_expense('3000793-3130527.jpeg')
    #     eq_(expense['sub_total'], Decimal("191.12"))
    #     eq_(expense['grand_total'], Decimal("215.97"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/36.yaml', filter_query_parameters=['key'])
    # def test_36(self):
    #     expense = self.scan_expense('3000793-3130879.jpeg')
    #     eq_(expense['sub_total'], Decimal("149.06"))
    #     eq_(expense['grand_total'], Decimal("168.44"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/37.yaml', filter_query_parameters=['key'])
    # def test_37(self):
    #     expense = self.scan_expense('3000793-3131917.jpeg')
    #     eq_(expense['sub_total'], Decimal("10.00"))
    #     eq_(expense['grand_total'], Decimal("11.30"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/38.yaml', filter_query_parameters=['key'])
    # def test_38(self):
    #     expense = self.scan_expense('3000793-3230225.jpeg')
    #     eq_(expense['sub_total'], Decimal("39.88"))
    #     eq_(expense['grand_total'], Decimal("45.06"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/39.yaml', filter_query_parameters=['key'])
    # def test_39(self):
    #     expense = self.scan_expense('3000793-3233389.jpeg')
    #     eq_(expense['sub_total'], Decimal("4.74"))
    #     eq_(expense['grand_total'], Decimal("41.21"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/40.yaml', filter_query_parameters=['key'])
    # def test_40(self):
    #     expense = self.scan_expense('3000793-3233459.jpeg')
    #     eq_(expense['sub_total'], Decimal("19.96"))
    #     eq_(expense['grand_total'], Decimal("22.55"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/41.yaml', filter_query_parameters=['key'])
    # def test_41(self):
    #     expense = self.scan_expense('3001071-10570.jpeg')
    #     eq_(expense['sub_total'], Decimal("11.50"))
    #     eq_(expense['grand_total'], Decimal("11.50"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/42.yaml', filter_query_parameters=['key'])
    # def test_42(self):
    #     expense = self.scan_expense('3001071-10571.jpeg')
    #     eq_(expense['sub_total'], Decimal("0.00"))
    #     eq_(expense['grand_total'], Decimal("0.00"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/43.yaml', filter_query_parameters=['key'])
    # def test_43(self):
    #     expense = self.scan_expense('3001110-3995.jpeg')
    #     eq_(expense['sub_total'], Decimal("44.97"))
    #     eq_(expense['grand_total'], Decimal("49.78"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/44.yaml', filter_query_parameters=['key'])
    # def test_44(self):
    #     expense = self.scan_expense('3001252-5698.jpeg')
    #     eq_(expense['sub_total'], Decimal("36.03"))
    #     eq_(expense['grand_total'], Decimal("36.03"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/45.yaml', filter_query_parameters=['key'])
    # def test_45(self):
    #     expense = self.scan_expense('3001256-4117.png')
    #     eq_(expense['sub_total'], Decimal("0.00"))
    #     eq_(expense['grand_total'], Decimal("0.00"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/46.yaml', filter_query_parameters=['key'])
    # def test_46(self):
    #     expense = self.scan_expense('3001288-7325.jpeg')
    #     eq_(expense['sub_total'], Decimal("4.00"))
    #     eq_(expense['grand_total'], Decimal("4.00"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/47.yaml', filter_query_parameters=['key'])
    # def test_47(self):
    #     expense = self.scan_expense('3001400-6913.jpeg')
    #     eq_(expense['sub_total'], Decimal("0.00"))
    #     eq_(expense['grand_total'], Decimal("0.00"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/48.yaml', filter_query_parameters=['key'])
    # def test_48(self):
    #     expense = self.scan_expense('3001421-16722.jpeg')
    #     eq_(expense['sub_total'], Decimal("0.00"))
    #     eq_(expense['grand_total'], Decimal("0.00"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/49.yaml', filter_query_parameters=['key'])
    # def test_49(self):
    #     expense = self.scan_expense('3001427-2253740.jpeg')
    #     eq_(expense['sub_total'], Decimal("13.48"))
    #     eq_(expense['grand_total'], Decimal("13.48"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/50.yaml', filter_query_parameters=['key'])
    # def test_50(self):
    #     expense = self.scan_expense('3001505-104668.jpeg')
    #     eq_(expense['sub_total'], Decimal("305.65"))
    #     eq_(expense['grand_total'], Decimal("323.99"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/51.yaml', filter_query_parameters=['key'])
    # def test_51(self):
    #     expense = self.scan_expense('3001505-2238320.jpeg')
    #     eq_(expense['sub_total'], Decimal("257.81"))
    #     eq_(expense['grand_total'], Decimal("273.28"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/52.yaml', filter_query_parameters=['key'])
    # def test_52(self):
    #     expense = self.scan_expense('3001505-2708070.png')
    #     eq_(expense['sub_total'], Decimal("40.00"))
    #     eq_(expense['grand_total'], Decimal("40.00"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/53.yaml', filter_query_parameters=['key'])
    # def test_53(self):
    #     expense = self.scan_expense('3001505-2712263.png')
    #     eq_(expense['sub_total'], Decimal("36.02"))
    #     eq_(expense['grand_total'], Decimal("36.02"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/54.yaml', filter_query_parameters=['key'])
    # def test_54(self):
    #     expense = self.scan_expense('3001505-2712293.png')
    #     eq_(expense['sub_total'], Decimal("40.00"))
    #     eq_(expense['grand_total'], Decimal("40.00"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/55.yaml', filter_query_parameters=['key'])
    # def test_55(self):
    #     expense = self.scan_expense('3001505-2779361.png')
    #     eq_(expense['sub_total'], Decimal("40.00"))
    #     eq_(expense['grand_total'], Decimal("40.00"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/56.yaml', filter_query_parameters=['key'])
    # def test_56(self):
    #     expense = self.scan_expense('3001505-2894461.png')
    #     eq_(expense['sub_total'], Decimal("40.00"))
    #     eq_(expense['grand_total'], Decimal("40.00"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/57.yaml', filter_query_parameters=['key'])
    # def test_57(self):
    #     expense = self.scan_expense('3001505-3051601.png')
    #     eq_(expense['sub_total'], Decimal("16.82"))
    #     eq_(expense['grand_total'], Decimal("17.83"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/58.yaml', filter_query_parameters=['key'])
    # def test_58(self):
    #     expense = self.scan_expense('3001505-3123233.png')
    #     eq_(expense['sub_total'], Decimal("95.59"))
    #     eq_(expense['grand_total'], Decimal("95.59"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/59.yaml', filter_query_parameters=['key'])
    # def test_59(self):
    #     expense = self.scan_expense('3001505-3157021.png')
    #     eq_(expense['sub_total'], Decimal("115.38"))
    #     eq_(expense['grand_total'], Decimal("122.30"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/60.yaml', filter_query_parameters=['key'])
    # def test_60(self):
    #     expense = self.scan_expense('3001505-3217169.png')
    #     eq_(expense['sub_total'], Decimal("15.89"))
    #     eq_(expense['grand_total'], Decimal("16.84"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/61.yaml', filter_query_parameters=['key'])
    # def test_61(self):
    #     expense = self.scan_expense('3001505-3623851.png')
    #     eq_(expense['sub_total'], Decimal("10.64"))
    #     eq_(expense['grand_total'], Decimal("11.19"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/62.yaml', filter_query_parameters=['key'])
    # def test_62(self):
    #     expense = self.scan_expense('3001505-4580349.png')
    #     eq_(expense['sub_total'], Decimal("0.00"))
    #     eq_(expense['grand_total'], Decimal("0.00"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/63.yaml', filter_query_parameters=['key'])
    # def test_63(self):
    #     expense = self.scan_expense('3001505-4589165.png')
    #     eq_(expense['sub_total'], Decimal("25.00"))
    #     eq_(expense['grand_total'], Decimal("25.00"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/64.yaml', filter_query_parameters=['key'])
    # def test_64(self):
    #     expense = self.scan_expense('3001505-4712789.png')
    #     eq_(expense['sub_total'], Decimal("50.00"))
    #     eq_(expense['grand_total'], Decimal("50.00"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/65.yaml', filter_query_parameters=['key'])
    # def test_65(self):
    #     expense = self.scan_expense('3001505-4846925.png')
    #     eq_(expense['sub_total'], Decimal("26.05"))
    #     eq_(expense['grand_total'], Decimal("26.05"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/66.yaml', filter_query_parameters=['key'])
    # def test_66(self):
    #     expense = self.scan_expense('3001505-4952457.png')
    #     eq_(expense['sub_total'], Decimal("18.27"))
    #     eq_(expense['grand_total'], Decimal("18.27"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/67.yaml', filter_query_parameters=['key'])
    # def test_67(self):
    #     expense = self.scan_expense('3001505-5158983.png')
    #     eq_(expense['sub_total'], Decimal("40.00"))
    #     eq_(expense['grand_total'], Decimal("40.00"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/68.yaml', filter_query_parameters=['key'])
    # def test_68(self):
    #     expense = self.scan_expense('3001505-5216581.png')
    #     eq_(expense['sub_total'], Decimal("588.31"))
    #     eq_(expense['grand_total'], Decimal("623.61"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/69.yaml', filter_query_parameters=['key'])
    # def test_69(self):
    #     expense = self.scan_expense('3001505-5261225.png')
    #     eq_(expense['sub_total'], Decimal("628.51"))
    #     eq_(expense['grand_total'], Decimal("666.22"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/70.yaml', filter_query_parameters=['key'])
    # def test_70(self):
    #     expense = self.scan_expense('3001505-5426377.png')
    #     eq_(expense['sub_total'], Decimal("312.19"))
    #     eq_(expense['grand_total'], Decimal("330.92"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/71.yaml', filter_query_parameters=['key'])
    # def test_71(self):
    #     expense = self.scan_expense('3001645-14748.jpeg')
    #     eq_(expense['sub_total'], Decimal("0.00"))
    #     eq_(expense['grand_total'], Decimal("0.00"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/72.yaml', filter_query_parameters=['key'])
    # def test_72(self):
    #     expense = self.scan_expense('3001645-6775.png')
    #     eq_(expense['sub_total'], Decimal("0.00"))
    #     eq_(expense['grand_total'], Decimal("0.00"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/73.yaml', filter_query_parameters=['key'])
    # def test_73(self):
    #     expense = self.scan_expense('3001770-6642.png')
    #     eq_(expense['sub_total'], Decimal("10.00"))
    #     eq_(expense['grand_total'], Decimal("10.00"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/74.yaml', filter_query_parameters=['key'])
    # def test_74(self):
    #     expense = self.scan_expense('3001840-978704.jpeg')
    #     eq_(expense['sub_total'], Decimal("20.00"))
    #     eq_(expense['grand_total'], Decimal("20.00"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/75.yaml', filter_query_parameters=['key'])
    # def test_75(self):
    #     expense = self.scan_expense('3001848-6212.jpeg')
    #     eq_(expense['sub_total'], Decimal("7.50"))
    #     eq_(expense['grand_total'], Decimal("8.13"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/76.yaml', filter_query_parameters=['key'])
    # def test_76(self):
    #     expense = self.scan_expense('3001872-160600.png')
    #     eq_(expense['sub_total'], Decimal("35.00"))
    #     eq_(expense['grand_total'], Decimal("35.00"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/77.yaml', filter_query_parameters=['key'])
    # def test_77(self):
    #     expense = self.scan_expense('3001872-18614.png')
    #     eq_(expense['sub_total'], Decimal("99.00"))
    #     eq_(expense['grand_total'], Decimal("99.00"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/78.yaml', filter_query_parameters=['key'])
    # def test_78(self):
    #     expense = self.scan_expense('3001872-2034001.png')
    #     eq_(expense['sub_total'], Decimal("120.00"))
    #     eq_(expense['grand_total'], Decimal("120.00"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/79.yaml', filter_query_parameters=['key'])
    # def test_79(self):
    #     expense = self.scan_expense('3002033-8336.jpeg')
    #     eq_(expense['sub_total'], Decimal("44.97"))
    #     eq_(expense['grand_total'], Decimal("48.12"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/80.yaml', filter_query_parameters=['key'])
    # def test_80(self):
    #     expense = self.scan_expense('3002034-16054.png')
    #     eq_(expense['sub_total'], Decimal("0.00"))
    #     eq_(expense['grand_total'], Decimal("0.00"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/81.yaml', filter_query_parameters=['key'])
    # def test_81(self):
    #     expense = self.scan_expense('3002054-2108818.jpeg')
    #     eq_(expense['sub_total'], Decimal("185.00"))
    #     eq_(expense['grand_total'], Decimal("185.00"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/82.yaml', filter_query_parameters=['key'])
    # def test_82(self):
    #     expense = self.scan_expense('3002054-2459080.jpeg')
    #     eq_(expense['sub_total'], Decimal("100.00"))
    #     eq_(expense['grand_total'], Decimal("100.00"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/83.yaml', filter_query_parameters=['key'])
    # def test_83(self):
    #     expense = self.scan_expense('3002054-996844.jpeg')
    #     eq_(expense['sub_total'], Decimal("80.00"))
    #     eq_(expense['grand_total'], Decimal("80.00"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/84.yaml', filter_query_parameters=['key'])
    # def test_84(self):
    #     expense = self.scan_expense('3002082-6898.png')
    #     eq_(expense['sub_total'], Decimal("21.16"))
    #     eq_(expense['grand_total'], Decimal("21.16"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/85.yaml', filter_query_parameters=['key'])
    # def test_85(self):
    #     expense = self.scan_expense('3002126-3177433.jpeg')
    #     eq_(expense['sub_total'], Decimal("15.00"))
    #     eq_(expense['grand_total'], Decimal("15.00"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/86.yaml', filter_query_parameters=['key'])
    # def test_86(self):
    #     expense = self.scan_expense('3002206-27069.jpeg')
    #     eq_(expense['sub_total'], Decimal("105.00"))
    #     eq_(expense['grand_total'], Decimal("105.00"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/87.yaml', filter_query_parameters=['key'])
    # def test_87(self):
    #     expense = self.scan_expense('3002211-2743039.jpeg')
    #     eq_(expense['sub_total'], Decimal("27.15"))
    #     eq_(expense['grand_total'], Decimal("27.15"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/88.yaml', filter_query_parameters=['key'])
    # def test_88(self):
    #     expense = self.scan_expense('3002211-3051555.jpeg')
    #     eq_(expense['sub_total'], Decimal("8.00"))
    #     eq_(expense['grand_total'], Decimal("8.00"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/89.yaml', filter_query_parameters=['key'])
    # def test_89(self):
    #     expense = self.scan_expense('3002346-3377405.jpeg')
    #     eq_(expense['sub_total'], Decimal("33.89"))
    #     eq_(expense['grand_total'], Decimal("33.89"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/90.yaml', filter_query_parameters=['key'])
    # def test_90(self):
    #     expense = self.scan_expense('3002346-3377983.jpeg')
    #     eq_(expense['sub_total'], Decimal("8.00"))
    #     eq_(expense['grand_total'], Decimal("8.62"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/91.yaml', filter_query_parameters=['key'])
    # def test_91(self):
    #     expense = self.scan_expense('3002346-3472905.png')
    #     eq_(expense['sub_total'], Decimal("164.00"))
    #     eq_(expense['grand_total'], Decimal("164.00"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/92.yaml', filter_query_parameters=['key'])
    # def test_92(self):
    #     expense = self.scan_expense('3002346-461708.jpeg')
    #     eq_(expense['sub_total'], Decimal("92.44"))
    #     eq_(expense['grand_total'], Decimal("99.60"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/93.yaml', filter_query_parameters=['key'])
    # def test_93(self):
    #     expense = self.scan_expense('3002365-1165312.jpeg')
    #     eq_(expense['sub_total'], Decimal("50.21"))
    #     eq_(expense['grand_total'], Decimal("50.21"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/94.yaml', filter_query_parameters=['key'])
    # def test_94(self):
    #     expense = self.scan_expense('3002421-7536.jpeg')
    #     eq_(expense['sub_total'], Decimal("210.00"))
    #     eq_(expense['grand_total'], Decimal("210.00"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/95.yaml', filter_query_parameters=['key'])
    # def test_95(self):
    #     expense = self.scan_expense('3002632-11679.jpeg')
    #     eq_(expense['sub_total'], Decimal("0.00"))
    #     eq_(expense['grand_total'], Decimal("0.00"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/96.yaml', filter_query_parameters=['key'])
    # def test_96(self):
    #     expense = self.scan_expense('3002677-53694.jpeg')
    #     eq_(expense['sub_total'], Decimal("83.98"))
    #     eq_(expense['grand_total'], Decimal("83.98"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/97.yaml', filter_query_parameters=['key'])
    # def test_97(self):
    #     expense = self.scan_expense('3002677-53696.jpeg')
    #     eq_(expense['sub_total'], Decimal("18.50"))
    #     eq_(expense['grand_total'], Decimal("21.09"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/98.yaml', filter_query_parameters=['key'])
    # def test_98(self):
    #     expense = self.scan_expense('3002677-62001.png')
    #     eq_(expense['sub_total'], Decimal("56.00"))
    #     eq_(expense['grand_total'], Decimal("56.00"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/99.yaml', filter_query_parameters=['key'])
    # def test_99(self):
    #     expense = self.scan_expense('3002745-1047373.jpeg')
    #     eq_(expense['sub_total'], Decimal("95.00"))
    #     eq_(expense['grand_total'], Decimal("95.00"))

    # @vcr.use_cassette('fixtures/vcr_cassettes/100.yaml', filter_query_parameters=['key'])
    # def test_100(self):
    #     expense = self.scan_expense('3002745-189919.jpeg')
    #     eq_(expense['sub_total'], Decimal("109.00"))
    #     eq_(expense['grand_total'], Decimal("109.00"))
