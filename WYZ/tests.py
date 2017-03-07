# -*- coding:utf-8 -*-
import unittest
from model import Dmu
from config import SHEET_2005, SHEET_2010
from read_xls import read_dmus

class TestModel(unittest.TestCase):
    def setUp(self):
        self.dmu = Dmu('beijing', 100.0, 89.1, 22.3, 45.2, 32.9)
    def test_name(self):
        self.assertEqual(self.dmu.name, 'beijing')
    def test_energy(self):
        self.assertAlmostEqual(self.dmu.energy, 100.0)
    def test_capital(self):
        self.assertAlmostEqual(self.dmu.capital, 89.1)
    def test_labour(self):
        self.assertAlmostEqual(self.dmu.labour, 22.3)
    def test_production(self):
        self.assertAlmostEqual(self.dmu.production, 45.2)
    def test_co2(self):
        self.assertAlmostEqual(self.dmu.co2, 32.9)

class TestRead(unittest.TestCase):
    def setUp(self):
        self.dmus = read_dmus(SHEET_2005)
    def test_dmus(self):
        self.assertEqual(30, len(self.dmus))
        beijing_dmu = self.dmus[0]
        self.assertEqual('北京', beijing_dmu.name)
        self.assertAlmostEqual(7150.005, beijing_dmu.energy, places=3)
        self.assertAlmostEqual(16315.52973, beijing_dmu.capital, places=3)
        self.assertAlmostEqual(920.4, beijing_dmu.labour, places=3)
        self.assertAlmostEqual(6969.52, beijing_dmu.produciton, places=3)
        self.assertAlmostEqual(20637.504, beijing_dmu.co2, places=3)
if __name__ == '__main__':
    unittest.main()