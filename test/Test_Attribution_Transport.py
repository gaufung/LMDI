# -*- coding:utf8 -*-
import sys
sys.path.append('..')
import unittest
import math
import operator
from PDA_Transport.config import DMUS_2006_DATA, DMUS_2007_DATA,DMUS_2008_DATA,DMUS_2009_DATA
from PDA_Transport.config import DMUS_2010_DATA, DMUS_2011_DATA, DMUS_2012_DATA, DMUS_2013_DATA, DMUS_2014_DATA
from PDA_Transport.Data_Read import read_dmus
from PDA_Transport.LMDI import Lmdi
from PDA_Transport.SinglePeriodAAM import Spaam

class TestAttribute(unittest.TestCase):
    def setUp(self):
        dmus_2006 = read_dmus(DMUS_2006_DATA)
        dmus_2007 = read_dmus(DMUS_2007_DATA)
        dmus_2008 = read_dmus(DMUS_2008_DATA)
        dmus_2009 = read_dmus(DMUS_2009_DATA)
        dmus_2010 = read_dmus(DMUS_2010_DATA)
        dmus_2011 = read_dmus(DMUS_2011_DATA)
        dmus_2012 = read_dmus(DMUS_2012_DATA)
        dmus_2013 = read_dmus(DMUS_2013_DATA)
        dmus_2014 = read_dmus(DMUS_2014_DATA)
        global_dmus = [dmus_2006, dmus_2007, dmus_2008, dmus_2009, dmus_2010,
                       dmus_2011, dmus_2012, dmus_2013, dmus_2014]
        self.spaam_2006_2007 = Spaam.build(dmus_2006, dmus_2007, '2006-2007',global_dmus)
    def test_emx(self):
        sum_value = sum(self.spaam_2006_2007.emx_attributions)
        total_value = self.spaam_2006_2007.emx - 1
        self.assertAlmostEqual(sum_value, total_value)
    def test_pei(self):
        '''
        pis checked
        '''
        sum_value = sum(self.spaam_2006_2007.pei_attributions)
        total_value = self.spaam_2006_2007.pei - 1
        self.assertAlmostEqual(sum_value, total_value)
    def test_est(self):
        '''
        pei checked
        '''
        sum_value = sum(self.spaam_2006_2007.est_attributions)
        total_value = self.spaam_2006_2007.est - 1
        self.assertAlmostEqual(sum_value, total_value)
    def test_eue(self):
        '''
        isg checked
        '''
        sum_value = sum(self.spaam_2006_2007.eue_attributions)
        total_value = self.spaam_2006_2007.eue - 1
        self.assertAlmostEqual(sum_value, total_value)
    def test_pti(self):
        '''
        eue checked
        '''
        sum_value = sum(self.spaam_2006_2007.pti_attributions)
        total_value = self.spaam_2006_2007.pti - 1
        self.assertAlmostEqual(sum_value, total_value)
    def test_yoe(self):
        '''
        est checked
        '''
        sum_value = sum(self.spaam_2006_2007.yoe_attributions)
        total_value = self.spaam_2006_2007.yoe - 1
        self.assertAlmostEqual(sum_value, total_value)
    def test_yct(self):
        '''
        yoe checked
        '''
        sum_value = sum(self.spaam_2006_2007.yct_attributions)
        total_value = self.spaam_2006_2007.yct - 1
        self.assertAlmostEqual(sum_value, total_value)
    def test_rts(self):
        '''
        yct checked
        '''
        sum_value = sum(self.spaam_2006_2007.rts_attributions)
        total_value = self.spaam_2006_2007.rts - 1
        self.assertAlmostEqual(sum_value, total_value)
    def test_cef(self):
        '''
        cef test
        '''
        sum_value = sum(self.spaam_2006_2007.cef_attributions)
        total_value = self.spaam_2006_2007.cef - 1
        self.assertAlmostEqual(sum_value, total_value)
if __name__ =='__main__':
    unittest.main()
