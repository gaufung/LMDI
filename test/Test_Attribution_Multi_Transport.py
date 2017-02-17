#-*- coding:utf8 -*-
import sys
sys.path.append('..')
import unittest
import operator
from PDA_Transport.config import DMUS_2006_DATA, DMUS_2007_DATA,DMUS_2008_DATA,DMUS_2009_DATA
from PDA_Transport.config import DMUS_2010_DATA, DMUS_2011_DATA, DMUS_2012_DATA, DMUS_2013_DATA, DMUS_2014_DATA
from PDA_Transport.Data_Read import read_dmus
from PDA_Transport.LMDI import Lmdi
from PDA_Transport.MultiPeriodAAM import Mpaam

class TestMPaam(unittest.TestCase):
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
        self.mpaam=Mpaam(global_dmus,'2006-2014', global_dmus)
    def test_emx(self):
        '''
        test emx
        '''
        emx_total = self.mpaam.emx_t(8)
        emx_attribution = sum(self.mpaam.emx())
        self.assertAlmostEqual(emx_total - 1, emx_attribution, places=5)
    def test_cef(self):
        total = self.mpaam.cef_t(8)
        attribution = sum(self.mpaam.cef())
        self.assertAlmostEqual(total-1, attribution)
    def test_pei(self):
        total = self.mpaam.pei_t(8)
        attribution = sum(self.mpaam.pei())
        self.assertAlmostEqual(total-1, attribution)
    def test_est(self):
        total = self.mpaam.est_t(8)
        attribution = sum(self.mpaam.est())
        self.assertAlmostEqual(total-1, attribution)
    def test_eue(self):
        total = self.mpaam.eue_t(8)
        attribution = sum(self.mpaam.eue())
        self.assertAlmostEqual(total-1, attribution)
    def test_pti(self):
        total = self.mpaam.pti_t(8)
        attribution = sum(self.mpaam.pti())
        self.assertAlmostEqual(total-1, attribution)
    def test_yoe(self):
        total = self.mpaam.yoe_t(8)
        attribution = sum(self.mpaam.yoe())
        self.assertAlmostEqual(total-1, attribution)
    def test_yct(self):
        total = self.mpaam.yct_t(8)
        attribution = sum(self.mpaam.yct())
        self.assertAlmostEqual(total-1, attribution)
    def test_rts(self):
        total = self.mpaam.rts_t(8)
        attribution = sum(self.mpaam.rts())
        self.assertAlmostEqual(total-1, attribution)
    
if __name__ == '__main__':
    unittest.main()
    