# -*- coding:utf8 -*-

'''
Test module
'''
import unittest
import GlobalVaribales
import DataRead
import Model
import LMDI
import math

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

class Test_Attribute(unittest.TestCase):
    '''
    test emx
    '''
    def setUp(self):
        '''
        初始化条件
        '''
        dmus_2006 = DataRead.read_dmus(GlobalVaribales.PRO_2006_COL, GlobalVaribales.SHEET_2006)
        dmus_2007 = DataRead.read_dmus(GlobalVaribales.PRO_2007_COL, GlobalVaribales.SHEET_2007)
        self.lmdi_2006_2007 = LMDI.Lmdi(dmus_2006, dmus_2007)
    def test_emx(self):
        '''
        emx checked
        '''
        sum_value = sum([k*v for k, v in zip(self.lmdi_2006_2007.remx(),
                                             self.lmdi_2006_2007.emx_ratio())])
        total_value = math.exp(sum(list(self.lmdi_2006_2007.emx()))) - 1
        self.assertAlmostEqual(sum_value, total_value, places=5)
    def test_pis(self):
        '''
        pis checked
        '''
        sum_value = sum([k*v for k, v in zip(self.lmdi_2006_2007.rpis(),
                                             self.lmdi_2006_2007.pis_ratio())])
        total_sum = math.exp(sum(list(self.lmdi_2006_2007.pis()))) - 1
        self.assertAlmostEqual(sum_value, total_sum, places=5)
    def test_pei(self):
        '''
        pei checked
        '''
        sum_value = sum([k*v for k, v in zip(self.lmdi_2006_2007.rpei(), self.lmdi_2006_2007.pei_ratio())])
        total_value = math.exp(sum(list(self.lmdi_2006_2007.pei()))) - 1 
        self.assertAlmostEqual(sum_value, total_value, places=5)
    def test_isg(self):
        '''
        isg checked
        '''
        sum_value = sum([k*v for k,v in zip(self.lmdi_2006_2007.risg(),
                                            self.lmdi_2006_2007.isg_ratio())])
        total_value = math.exp(sum(list(self.lmdi_2006_2007.isg()))) - 1 
        self.assertAlmostEqual(sum_value, total_value, places=5)
    def test_eue(self):
        '''
        eue checked
        '''
        sum_value = sum([k*v for k, v in zip(self.lmdi_2006_2007.reue(), self.lmdi_2006_2007.eue_ratio())])
        total_value = math.exp(sum(list(self.lmdi_2006_2007.eue()))) - 1
        self.assertAlmostEqual(sum_value, total_value, places=5)
    def test_est(self):
        '''
        est checked
        '''
        sum_value = sum([k*v for k, v in zip(self.lmdi_2006_2007.rest(), self.lmdi_2006_2007.est_ratio())])
        total_value = math.exp(sum(list(self.lmdi_2006_2007.est()))) - 1
        self.assertAlmostEqual(sum_value, total_value, places=5)
    def test_yoe(self):
        '''
        yoe checked
        '''
        sum_value = sum([k*v for k, v in zip(self.lmdi_2006_2007.ryoe(), self.lmdi_2006_2007.yoe_ratio())])
        total_value = math.exp(sum(list(self.lmdi_2006_2007.yoe()))) - 1 
        self.assertAlmostEqual(sum_value, total_value, places=5)
    def test_yct(self):
        '''
        yct checked
        '''
        sum_value = sum([k*v for k, v in zip(self.lmdi_2006_2007.ryct(), self.lmdi_2006_2007.yct_ratio())])
        total_value = math.exp(sum(list(self.lmdi_2006_2007.yct()))) - 1
        self.assertAlmostEqual(sum_value, total_value, places=5)
    
if __name__ == '__main__':
    unittest.main()
