# -*- coding:utf8 -*-

'''
Test module
'''
import unittest
import math
import GlobalVaribales
import DataRead
import Model
import LMDI
from SinglePeriodAAM import Spaam
from MultiPeriodAAM import Mpaam
from WriteData import WriteLmdiData, WriteSpaamData

class Test_Attribuioin_Multi(unittest.TestCase):
    '''
    Test multi period attribution
    '''
    def setUp(self):
        '''
        初始化条件
        '''
        dmus_2006 = DataRead.read_dmus(GlobalVaribales.PRO_2006_COL, GlobalVaribales.SHEET_2006)
        dmus_2007 = DataRead.read_dmus(GlobalVaribales.PRO_2007_COL, GlobalVaribales.SHEET_2007)
        dmus_2008 = DataRead.read_dmus(GlobalVaribales.PRO_2008_COL, GlobalVaribales.SHEET_2008)
        dmus_2009 = DataRead.read_dmus(GlobalVaribales.PRO_2009_COL, GlobalVaribales.SHEET_2009)
        dmus_2010 = DataRead.read_dmus(GlobalVaribales.PRO_2010_COL, GlobalVaribales.SHEET_2010)
        dmus_2011 = DataRead.read_dmus(GlobalVaribales.PRO_2011_COL, GlobalVaribales.SHEET_2011)
        dmus_2012 = DataRead.read_dmus(GlobalVaribales.PRO_2012_COL, GlobalVaribales.SHEET_2012)
        dmus_2013 = DataRead.read_dmus(GlobalVaribales.PRO_2013_COL, GlobalVaribales.SHEET_2013)
        dmus_2014 = DataRead.read_dmus(GlobalVaribales.PRO_2014_COL, GlobalVaribales.SHEET_2014)
        self.mpaam = Mpaam([dmus_2006, dmus_2007, dmus_2008, dmus_2009, dmus_2010, dmus_2011
                            , dmus_2012, dmus_2013, dmus_2014], '2006-2004')
    def test_emx(self):
        '''
        test emx
        '''
        emx_total = self.mpaam.emx_t(8)
        emx_attribution = sum(self.mpaam.emx())
        self.assertAlmostEqual(emx_total - 1, emx_attribution, places=5)
    def test_pei(self):
        '''
        test pei
        '''
        pei_total = self.mpaam.pei_t(8)
        pei_attribution = sum(self.mpaam.pei())
        self.assertAlmostEqual(pei_total - 1, pei_attribution, places=5)
    def test_pis(self):
        '''
        test pis
        '''
        pis_total = self.mpaam.pis_t(8)
        pis_attribution = sum(self.mpaam.pis())
        self.assertAlmostEqual(pis_total - 1, pis_attribution, places=5)
    def test_isg(self):
        '''
        test isg
        '''
        isg_total = self.mpaam.isg_t(8)
        isg_attribution = sum(self.mpaam.isg())
        self.assertAlmostEqual(isg_total - 1, isg_attribution, places=5)
    def test_eue(self):
        '''
        test eue
        '''
        eue_total = self.mpaam.eue_t(8)
        eue_attribution = sum(self.mpaam.eue())
        self.assertAlmostEquals(eue_total - 1, eue_attribution, places=5)
    def test_est(self):
        '''
        test est
        '''
        est_total = self.mpaam.est_t(8)
        est_attribution = sum(self.mpaam.est())
        self.assertAlmostEqual(est_total - 1, est_attribution, places=5)
    def test_yoe(self):
        '''
        test yoe
        '''
        yoe_total = self.mpaam.yoe_t(8)
        yoe_attribution = sum(self.mpaam.yoe())
        self.assertAlmostEqual(yoe_total - 1, yoe_attribution, places=5)
    def test_yct(self):
        '''
        test yct
        '''
        yct_total = self.mpaam.yct_t(8)
        yct_attribution = sum(self.mpaam.yct())
        self.assertAlmostEqual(yct_total - 1, yct_attribution, places=5)
if __name__ == '__main__':
    unittest.main()
