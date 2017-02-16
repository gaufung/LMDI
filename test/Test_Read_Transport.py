# -*- coding:utf8 -*-
from __future__ import unicode_literals
import sys
sys.path.append('..')
import unittest
from PDA_Transport.config import DMUS_2006_DATA
from PDA_Transport.Data_Read import read_dmus

class Test_Read(unittest.TestCase):
    '''
    test read
    '''
    def test_dmus(self):
        dmus_2006 = read_dmus(DMUS_2006_DATA)
        self.assertEqual(30, len(dmus_2006))
        dmu_beijing = dmus_2006[0]
        print type(dmu_beijing)
        self.assertEqual(758.09796, dmu_beijing.turn_over.turn_over)
        self.assertEqual('北京', dmu_beijing.name)
        self.assertEqual(458.29, dmu_beijing.production.production)
        energies_except = [18.693231,0,0,0,0,81.868696,
                    343.174622,118.214523,0, 2.777166,20.216,10.0654,28.62341]
        energies_true = dmu_beijing.energy.energy
        self.assertEqual(len(energies_except), len(energies_true))
        for tu in zip(energies_except, energies_true):
            self.assertAlmostEqual(tu[0], tu[1])
        #co2s_except = [18.693231,0,0,0,0,81.868696,343.174622,118.214523,0,2.777166,20.216,10.0654,28.62341]
        co2_except = [51.76155926,0,0,0,0,167.749036,718.2329512,256.4124359,0,5.129397738,27.49072,31.55248237,
        226.9854136]
        co2s_true = dmu_beijing.co2.co2
        self.assertEqual(len(co2_except), len(co2s_true))
        for tu in zip(co2_except, co2s_true):
            self.assertAlmostEqual(tu[0], tu[1])


if __name__ == '__main__':
    unittest.main()