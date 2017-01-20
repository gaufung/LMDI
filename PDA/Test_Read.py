# -*- coding:utf8 -*-
# ! /usr/bin/python
'''
test PDA read module
'''
import unittest
from config import PRO_2006_COL, SHEET_2006
import DataRead
import Model
import LMDI
from SinglePeriodAAM import Spaam
from MultiPeriodAAM import Mpaam
from WriteData import WriteLmdiData, WriteSpaamData
class TestDataRead(unittest.TestCase):
    '''
    Test DataRead module
    '''
    def test_count(self):
        '''
        test count
        '''
        dmu_2006 = DataRead.read_dmus(PRO_2006_COL, SHEET_2006)
        self.assertEqual(len(dmu_2006), 30)
    def test_value(self):
        '''
        test value
        '''
        dmu_2006 = DataRead.read_dmus(PRO_2006_COL,
                                      SHEET_2006)
        dmu = dmu_2006[0]
        self.assertAlmostEquals(dmu.pro.production, 1821.86, places=2)
        self.assertAlmostEquals(dmu.ene.total, 1870.706144, places=2)
        self.assertAlmostEquals(dmu.co2.total, 6014.889154, places=2)
if __name__ == '__main__':
    unittest.main()
