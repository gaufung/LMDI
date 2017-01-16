# -*- coding:utf8 -*- 
# !/bin/usr/python
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

class TestModel(unittest.TestCase):
    '''
    test model
    '''
    def test_energy(self):
        '''
        test energy model
        '''
        energy = Model.Energy('北京', [10.2, 33.0, 43.2])
        self.assertEqual(energy.name, '北京')
        self.assertEqual(len(energy), 3)
        self.assertEqual(energy[0], 10.2)
        self.assertEqual(energy[-1], energy.total)
    def test_co2(self):
        '''
        test co2 model
        '''
        co2 = Model.Co2('上海', [88.2, 10.2, 98.4])
        self.assertEqual(co2.name, '上海')
        self.assertEqual(len(co2), 3)
        self.assertEqual(co2[0], 88.2)
        self.assertEqual(co2[-1], co2.total)
    def test_pro(self):
        '''
        test production model
        '''
        pro = Model.Production('江苏', 66)
        self.assertEqual(pro.name, '江苏')
        self.assertEqual(pro.production, 66)
if __name__ == '__main__':
    unittest.main()