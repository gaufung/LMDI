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
class TestAttribute(unittest.TestCase):
    '''
    test emx
    '''
    def setUp(self):
        '''
        初始化条件
        '''
        dmus_2006 = DataRead.read_dmus(GlobalVaribales.PRO_2006_COL, GlobalVaribales.SHEET_2006)
        dmus_2007 = DataRead.read_dmus(GlobalVaribales.PRO_2007_COL, GlobalVaribales.SHEET_2007)
        dmus_2008 = DataRead.read_dmus(GlobalVaribales.PRO_2008_COL, GlobalVaribales.SHEET_2008)
        self.lmdi_2006_2007 = LMDI.Lmdi(dmus_2006, dmus_2007, '2006-2007')
        self.lmdi_2006_2008 = LMDI.Lmdi(dmus_2006, dmus_2008, '2006-2008')
        self.spaam_2006_2007 = Spaam(dmus_2006, dmus_2007, '2006-2007')
        self.spaam_2006_2008 = Spaam(dmus_2006, dmus_2008, '2006-2008')
    def test_province_name(self):
        '''
        省份名称
        '''
        self.assertEqual(len(self.spaam_2006_2007.province_names), 30)
    def test_emx(self):
        '''
        emx checked
        '''
        sum_value = sum([k*v for k, v in zip(self.spaam_2006_2007.remx(),
                                             self.spaam_2006_2007.emx_ratio())])
        total_value = math.exp(sum(list(self.lmdi_2006_2007.emx()))) - 1
        self.assertAlmostEqual(sum_value, total_value, places=5)
        self.assertAlmostEqual(total_value+1, self.spaam_2006_2007.emx)
    def test_pis(self):
        '''
        pis checked
        '''
        sum_value = sum([k*v for k, v in zip(self.spaam_2006_2007.rpis(),
                                             self.spaam_2006_2007.pis_ratio())])
        total_sum = math.exp(sum(list(self.lmdi_2006_2007.pis()))) - 1
        self.assertAlmostEqual(sum_value, total_sum, places=5)
        self.assertAlmostEqual(total_sum+1, self.spaam_2006_2007.pis)
    def test_pei(self):
        '''
        pei checked
        '''
        sum_value = sum([k*v for k, v in zip(self.spaam_2006_2007.rpei(),
                                             self.spaam_2006_2007.pei_ratio())])
        total_value = math.exp(sum(list(self.lmdi_2006_2007.pei()))) - 1
        self.assertAlmostEqual(sum_value, total_value, places=5)
        self.assertAlmostEqual(total_value+1, self.spaam_2006_2007.pei)
    def test_isg(self):
        '''
        isg checked
        '''
        sum_value = sum([k*v for k, v in zip(self.spaam_2006_2007.risg(),
                                             self.spaam_2006_2007.isg_ratio())])
        total_value = math.exp(sum(list(self.lmdi_2006_2007.isg()))) - 1
        self.assertAlmostEqual(sum_value, total_value, places=5)
        self.assertAlmostEqual(total_value+1, self.spaam_2006_2007.isg)
    def test_eue(self):
        '''
        eue checked
        '''
        sum_value = sum([k*v for k, v in zip(self.spaam_2006_2007.reue(),
                                             self.spaam_2006_2007.eue_ratio())])
        total_value = math.exp(sum(list(self.lmdi_2006_2007.eue()))) - 1
        self.assertAlmostEqual(sum_value, total_value, places=5)
        self.assertAlmostEqual(total_value+1, self.spaam_2006_2007.eue)
    def test_est(self):
        '''
        est checked
        '''
        sum_value = sum([k*v for k, v in zip(self.spaam_2006_2007.rest(),
                                             self.spaam_2006_2007.est_ratio())])
        total_value = math.exp(sum(list(self.lmdi_2006_2007.est()))) - 1
        self.assertAlmostEqual(sum_value, total_value, places=5)
        self.assertAlmostEqual(total_value+1, self.spaam_2006_2007.est)
    def test_yoe(self):
        '''
        yoe checked
        '''
        sum_value = sum([k*v for k, v in zip(self.spaam_2006_2007.ryoe(),
                                             self.spaam_2006_2007.yoe_ratio())])
        total_value = math.exp(sum(list(self.lmdi_2006_2007.yoe()))) - 1
        self.assertAlmostEqual(sum_value, total_value, places=5)
        self.assertAlmostEqual(total_value+1, self.spaam_2006_2007.yoe)
    def test_yct(self):
        '''
        yct checked
        '''
        sum_value = sum([k*v for k, v in zip(self.spaam_2006_2007.ryct(),
                                             self.spaam_2006_2007.yct_ratio())])
        total_value = math.exp(sum(list(self.lmdi_2006_2007.yct()))) - 1
        self.assertAlmostEqual(sum_value, total_value, places=5)
        self.assertAlmostEqual(total_value+1, self.spaam_2006_2007.yct)

if __name__ == '__main__':
    unittest.main()