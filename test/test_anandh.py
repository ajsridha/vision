import vcr
import mimetypes
import base64
from vision.scan import scan
from unittest import TestCase
from nose.tools import eq_

class TestAnandh(TestCase):
    def scan_receipt(self, path):
        return scan(path)

    @vcr.use_cassette('fixtures/vcr_cassettes/1')
    def test_1(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3001505-2779361.png")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/2')
    def test_2(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3001505-4589165.png")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/3')
    def test_3(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3000171-119353.jpeg")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/4')
    def test_4(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3002082-6898.png")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/5')
    def test_5(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3001427-2253740.jpeg")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/6')
    def test_6(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3001645-6775.png")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/7')
    def test_7(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3001505-5261225.png")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/8')
    def test_8(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3001505-3051601.png")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/9')
    def test_9(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3000542-12521.jpeg")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/10')
    def test_10(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3000618-2156.jpeg")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/11')
    def test_11(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3002211-3051555.jpeg")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/12')
    def test_12(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3001505-2712263.png")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/13')
    def test_13(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3000382-2771981.jpeg")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/14')
    def test_14(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3000533-2350236.png")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/15')
    def test_15(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3000793-3131917.jpeg")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/16')
    def test_16(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3000057-11667.png")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/17')
    def test_17(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3001848-6212.jpeg")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/18')
    def test_18(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3002054-2108818.jpeg")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/19')
    def test_19(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3000618-1995.jpeg")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/20')
    def test_20(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3001252-5698.jpeg")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/21')
    def test_21(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3002677-53694.jpeg")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/22')
    def test_22(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3001256-4117.png")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/23')
    def test_23(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3000119-4598605.jpeg")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/24')
    def test_24(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3001770-6642.png")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/25')
    def test_25(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3000119-1132.jpeg")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/26')
    def test_26(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3001505-5216581.png")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/27')
    def test_27(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3000119-804383.jpeg")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/28')
    def test_28(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3001645-14748.jpeg")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/29')
    def test_29(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3000138-1304099.jpeg")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/30')
    def test_30(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3002346-461708.jpeg")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/31')
    def test_31(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3000618-5267057.jpeg")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/32')
    def test_32(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3001505-2238320.jpeg")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/33')
    def test_33(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3000793-2112982.jpeg")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/34')
    def test_34(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3002054-2459080.jpeg")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/35')
    def test_35(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3000793-3130527.jpeg")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/36')
    def test_36(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3000793-2112957.jpeg")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/37')
    def test_37(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3002054-996844.jpeg")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/38')
    def test_38(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3000138-298017.png")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/39')
    def test_39(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3000533-2703411.png")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/40')
    def test_40(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3001110-3995.jpeg")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/41')
    def test_41(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3002745-189919.jpeg")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/42')
    def test_42(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3000753-1980112.png")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/43')
    def test_43(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3001505-4712789.png")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/44')
    def test_44(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3001505-4846925.png")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/45')
    def test_45(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3001505-3123233.png")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/46')
    def test_46(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3000533-17606.png")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/47')
    def test_47(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3000533-2350240.png")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/48')
    def test_48(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3002211-2743039.jpeg")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/49')
    def test_49(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3001288-7325.jpeg")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/50')
    def test_50(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3000793-3130879.jpeg")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/51')
    def test_51(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3001421-16722.jpeg")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/52')
    def test_52(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3000464-1271.jpeg")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/53')
    def test_53(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3001505-2708070.png")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/54')
    def test_54(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3000495-11665.jpeg")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/55')
    def test_55(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3001872-18614.png")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/56')
    def test_56(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3001071-10571.jpeg")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/57')
    def test_57(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3001872-160600.png")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/58')
    def test_58(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3000060-26246.jpeg")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/59')
    def test_59(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3001505-5426377.png")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/60')
    def test_60(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3000119-804319.jpeg")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/61')
    def test_61(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3002033-8336.jpeg")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/62')
    def test_62(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3000793-3230225.jpeg")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/63')
    def test_63(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3001505-3623851.png")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/64')
    def test_64(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3000793-3233389.jpeg")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/65')
    def test_65(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3001872-2034001.png")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/66')
    def test_66(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3001400-6913.jpeg")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/67')
    def test_67(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3001505-2894461.png")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/68')
    def test_68(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3001505-104668.jpeg")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/69')
    def test_69(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3002745-1047373.jpeg")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/70')
    def test_70(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3001505-3157021.png")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/71')
    def test_71(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3002677-62001.png")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/72')
    def test_72(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3002365-1165312.jpeg")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/73')
    def test_73(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3002346-3472905.png")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/74')
    def test_74(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3000533-42941.jpeg")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/75')
    def test_75(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3000618-4988077.jpeg")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/76')
    def test_76(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3001071-10570.jpeg")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/77')
    def test_77(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3000138-2422.jpeg")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/78')
    def test_78(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3000582-2747685.png")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/79')
    def test_79(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3000138-2463.jpeg")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/80')
    def test_80(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3001505-2712293.png")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/81')
    def test_81(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3000399-26743.jpeg")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/82')
    def test_82(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3000527-1332.jpeg")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/83')
    def test_83(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3001840-978704.jpeg")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/84')
    def test_84(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3002034-16054.png")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/85')
    def test_85(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3001505-4580349.png")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/86')
    def test_86(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3002421-7536.jpeg")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/87')
    def test_87(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3002126-3177433.jpeg")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/88')
    def test_88(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3001505-3217169.png")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/89')
    def test_89(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3002206-27069.jpeg")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/90')
    def test_90(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3000558-200917.jpeg")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/91')
    def test_91(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3002677-53696.jpeg")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/92')
    def test_92(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3002346-3377405.jpeg")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/93')
    def test_93(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3001505-5158983.png")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/94')
    def test_94(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3001505-4952457.png")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/95')
    def test_95(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3002632-11679.jpeg")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/96')
    def test_96(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3002346-3377983.jpeg")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/97')
    def test_97(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3000119-5304795.jpeg")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/98')
    def test_98(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3000793-3233459.jpeg")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/99')
    def test_99(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3000533-1153196.png")
        eq_(expense['grand_total'], 0.00)


    @vcr.use_cassette('fixtures/vcr_cassettes/100')
    def test_100(self):
        expense = self.scan_receipt(
            "http://afn85.webfactional.com/receipts/3000715-1999.png")
        eq_(expense['grand_total'], 0.00)

