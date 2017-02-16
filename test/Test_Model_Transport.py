# -*- coding:utf8 -*-
import unittest
import sys
import unittest
sys.path.append('..')
from PDA_Transport.Model import *

class Test_Model(unittest.TestCase):
    '''
    test model
    '''
    def test_energy(self):
        energy = Energy('北京', [10.2, 0, 10])
        self.assertEqual('北京', energy.name)
        self.assertEqual(3, len(energy))
        self.assertEqual(20.2, energy.total)
    def test_co2(self):
        co2 = Co2('上海', [22.0, 8])
        self.assertEqual('上海', co2.name)
        self.assertEqual(2, len(co2))
        self.assertEqual(30.0, co2.total)
    def test_production(self):
        pro = Production('江苏', 34)
        self.assertEqual('江苏', pro.name)
        self.assertEqual(34, pro.production)
    def test_turnover(self):
        turnover = Turnover("山东", 54.0)
        self.assertEqual("山东", turnover.name)
        self.assertEqual(54.0, turnover.turn_over)
    def test_dmu(self):
        energy = Energy('北京', [10.2, 0, 10])
        co2 = Co2('北京', [22.0, 8])
        pro = Production('北京', 34)
        turnover = Turnover("北京", 54.0)
        dmu = Dmu(energy,pro,co2,turnover)
        self.assertEqual('北京', dmu.name)
        self.assertEqual(34, dmu.production.production)
        self.assertEqual(54.0, dmu.turn_over.turn_over)
        self.assertEqual([10.2, 0, 10], dmu.energy.energy)
        self.assertEqual([22.0, 8], dmu.co2.co2)
if __name__ == '__main__':
    unittest.main()
