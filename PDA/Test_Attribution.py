# -*- coding:utf8 -*-

'''
Test module
'''
import unittest
from config import *
import DataRead
import Model
import LMDI
from SinglePeriodAAM import Spaam
from MultiPeriodAAM import Mpaam
from WriteData import WriteLmdiData, WriteSpaamData
from operator import mul
class TestAttribute(unittest.TestCase):
    '''
    test emx
    '''
    def setUp(self):
        '''
        初始化条件
        '''
        dmus_2006 = DataRead.read_dmus(PRO_2006_COL, SHEET_2006)
        dmus_2007 = DataRead.read_dmus(PRO_2007_COL, SHEET_2007)
        self.spaam_2006_2007 = Spaam(dmus_2006, dmus_2007, '2006-2007')
    def test_province_name(self):
        '''
        省份数量
        '''
        self.assertEqual(len(self.spaam_2006_2007.province_names), 30)
    def test_emx(self):
        '''
        emx checked
        '''
        sum_value = sum(self.spaam_2006_2007.emx_attributions)
        total_value = self.spaam_2006_2007.emx - 1
        self.assertAlmostEqual(sum_value, total_value)
    def test_pis(self):
        '''
        pis checked
        '''
        sum_value = sum(self.spaam_2006_2007.pis_attributions)
        total_value = self.spaam_2006_2007.pis - 1
        self.assertAlmostEqual(sum_value, total_value)
    def test_pei(self):
        '''
        pei checked
        '''
        sum_value = sum(self.spaam_2006_2007.pei_attributions)
        total_value = self.spaam_2006_2007.pei - 1
        self.assertAlmostEqual(sum_value, total_value)
    def test_isg(self):
        '''
        isg checked
        '''
        sum_value = sum(self.spaam_2006_2007.isg_attributions)
        total_value = self.spaam_2006_2007.isg - 1
        self.assertAlmostEqual(sum_value, total_value)
    def test_eue(self):
        '''
        eue checked
        '''
        sum_value = sum(self.spaam_2006_2007.eue_attributions)
        total_value = self.spaam_2006_2007.eue - 1
        self.assertAlmostEqual(sum_value, total_value)
    def test_est(self):
        '''
        est checked
        '''
        sum_value = sum(self.spaam_2006_2007.est_attributions)
        total_value = self.spaam_2006_2007.est - 1
        self.assertAlmostEqual(sum_value, total_value)
    def test_yoe(self):
        '''
        yoe checked
        '''
        sum_value = sum(self.spaam_2006_2007.yoe_attributions)
        total_value = self.spaam_2006_2007.yoe - 1
        self.assertAlmostEqual(sum_value, total_value)
    def test_yct(self):
        '''
        yct checked
        '''
        sum_value = sum(self.spaam_2006_2007.yct_attributions)
        total_value = self.spaam_2006_2007.yct - 1
        self.assertAlmostEqual(sum_value, total_value)
    def test_cef(self):
        '''
        cef test
        '''
        sum_value = sum(self.spaam_2006_2007.cef_attributions)
        total_value = self.spaam_2006_2007.cef - 1
        self.assertAlmostEqual(sum_value, total_value)
    def test_ci(self):
        '''
        test ci
        '''
        self.assertAlmostEqual(self.spaam_2006_2007.ci, reduce(mul, self.spaam_2006_2007.indexes))
if __name__ == '__main__':
    unittest.main()
