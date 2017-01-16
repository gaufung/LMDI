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
        #self.lmdi_2006_2008 = LMDI.Lmdi(dmus_2006, dmus_2008, '2006-2008')
        self.spaam = Spaam(dmus_2006, dmus_2014, '2006-2004')
        #self.mpaam_2006_2007 = Mpaam([dmus_2006, dmus_2007], '2006-2007')
        self.mpaam = Mpaam([dmus_2006, dmus_2007, dmus_2008, dmus_2009, dmus_2010, dmus_2011
                            , dmus_2012, dmus_2013, dmus_2014], '2006-2004')
    def test_emx_multi_single(self):
        '''
        check 2006, 2007, 2008 mulitperid
        '''
        emx_single = self.spaam.emx - 1
        emx_multi = sum(self.mpaam.emx())
        self.assertAlmostEqual(emx_multi, emx_single, places=5)
    def test_pei_multi_single(self):
        '''
        check 2006, 2007, 2008 mulitperid
        '''
        pei_single = self.spaam.pei - 1
        pei_multi = sum(self.mpaam.pei())
        self.assertAlmostEqual(pei_multi, pei_single, places=5)
    def test_pis_multi_single(self):
        '''
        check
        '''
        pis_single = self.spaam.pis - 1
        pis_multi = sum(self.mpaam.pis())
        self.assertAlmostEqual(pis_multi, pis_single, places=5)
    def test_isg_multi_single(self):
        '''
        check
        '''
        isg_single = self.spaam.isg - 1
        isg_multi = sum(self.mpaam.isg())
        self.assertAlmostEqual(isg_single, isg_multi, places=5)
    def test_eue_multi_single(self):
        '''
        check
        '''
        eue_single = self.spaam.eue - 1
        eue_multi = sum(self.mpaam.eue())
        self.assertAlmostEqual(eue_multi, eue_single, places=5)
    def test_est_multi_single(self):
        '''
        check
        '''
        est_single = self.spaam.est - 1
        est_multi = sum(self.mpaam.est())
        self.assertAlmostEqual(est_multi, est_single, places=5)
    def test_yoe_multi_single(self):
        '''
        check
        '''
        yoe_single = self.spaam.yoe - 1
        yoe_multi = sum(self.mpaam.yoe())
        self.assertAlmostEqual(yoe_multi, yoe_single, places=5)
    def test_yct_multi_single(self):
        '''
        check
        '''
        yct_single = self.spaam.yct - 1
        yct_multi = sum(self.mpaam.yct())
        self.assertAlmostEqual(yct_multi, yct_single, places=5)
    
if __name__ == '__main__':
    unittest.main()
