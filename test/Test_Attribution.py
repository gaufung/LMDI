# -*- coding:utf8 -*-
'''
test signle attribution
'''
import sys
sys.path.append('..')

'''
Test module
'''
import unittest
import math
from PDA.config import *
import PDA.DataRead
import PDA.Model
import PDA.LMDI
from PDA.SinglePeriodAAM import Spaam
from PDA.MultiPeriodAAM import Mpaam
from PDA.WriteData import WriteLmdiData, WriteSpaamData
from operator import mul
class TestAttribute(unittest.TestCase):
    '''
    test emx
    '''
    def setUp(self):
        '''
        初始化条件
        '''
        dmus_2006 = PDA.DataRead.read_dmus(PRO_2006_COL, SHEET_2006)
        dmus_2007 = PDA.DataRead.read_dmus(PRO_2007_COL, SHEET_2007)
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
    def test_ci_province(self):
        '''
        test ci by province 
        '''
        ci_province = self.spaam_2006_2007.ci_by_province
        emx_province = self.spaam_2006_2007.emx_by_province
        cef_province = self.spaam_2006_2007.cef_by_province
        pei_province = self.spaam_2006_2007.pei_by_province
        eue_province = self.spaam_2006_2007.eue_by_province
        est_province = self.spaam_2006_2007.est_by_province
        for idx, _ in enumerate(ci_province):
            product = emx_province[idx] + cef_province[idx] + pei_province[idx] + \
                      0 + 0 + eue_province[idx] + \
                      est_province[idx] + 0 + 0
            self.assertAlmostEqual(ci_province[idx], math.exp(product))
if __name__ == '__main__':
    unittest.main()
