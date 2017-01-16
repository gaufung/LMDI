# -*- coding:utf8 -*-
# !/usr/bin/python
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
class TestWrite(unittest.TestCase):

    def setUp(self):
        self._dmus_2006 = DataRead.read_dmus(GlobalVaribales.PRO_2006_COL,
                                             GlobalVaribales.SHEET_2006)
        self._dmus_2007 = DataRead.read_dmus(GlobalVaribales.PRO_2007_COL,
                                             GlobalVaribales.SHEET_2007)
        self._dmus_2008 = DataRead.read_dmus(GlobalVaribales.PRO_2008_COL,
                                             GlobalVaribales.SHEET_2008)
    def test_lmdi_write(self):
        '''
        test write lmdi data
        '''
        lmdi_2006_2007 = LMDI.Lmdi(self._dmus_2006, self._dmus_2007, name='2006-2007')
        lmdi_2007_2008 = LMDI.Lmdi(self._dmus_2007, self._dmus_2008, name='2007-2008')
        with WriteLmdiData('test_lmdi.xls', lmdi_2006_2007, lmdi_2007_2008) as writer:
            writer.write()
    def test_spaam_write(self):
        '''
        test write spaam data
        '''
        spaam_2006_2007 = Spaam(self._dmus_2006, self._dmus_2007, name='2006-2007')
        spaam_2007_2008 = Spaam(self._dmus_2007, self._dmus_2008, name='2007-2008')
        with WriteSpaamData('contributions.xls', spaam_2006_2007, spaam_2007_2008) as writer:
            writer.write()
if __name__ == '__main__':
    unittest.main()