# -*- coding:utf8 -*-

'''
Test module
'''
import unittest
import GlobalVaribales
import DataRead

class TestDataRead(unittest.TestCase):
    '''
    Test DataRead module
    '''
    def test_count(self):
        '''
        test count
        '''
        dmu_2006 = DataRead.read_dmus(GlobalVaribales.PRO_2006_COL,
                                      GlobalVaribales.SHEET_2006)
        self.assertEqual(len(dmu_2006), 30)
    def test_value(self):
        '''
        test value
        '''
        dmu_2006 = DataRead.read_dmus(GlobalVaribales.PRO_2006_COL,
                                      GlobalVaribales.SHEET_2006)
        dmu = dmu_2006[0]
        self.assertAlmostEquals(dmu.pro.production, 1821.86, places=2)
        self.assertAlmostEquals(dmu.ene.total, 1470.19, places=2)
        self.assertAlmostEquals(dmu.co2.total, 3711.3, places=2)
        
if __name__ == '__main__':
    unittest.main()
