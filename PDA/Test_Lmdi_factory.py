# -*- coding:utf8 -*-
'''
测试 lmdi 工厂单元对象
'''
import unittest
import GlobalVaribales
from Lmdi_Factory import LmdiFactory
import DataRead
from LMDI import Lmdi
class Test_lmdi_factory(unittest.TestCase):
    '''
    test lmdi factory
    '''
    def setUp(self):
        '''
        初始化条件
        '''
        self.dmus_2006 = DataRead.read_dmus(GlobalVaribales.PRO_2006_COL,
                                            GlobalVaribales.SHEET_2006)
        self.dmus_2007 = DataRead.read_dmus(GlobalVaribales.PRO_2007_COL,
                                            GlobalVaribales.SHEET_2007)
    def test_factory(self):
        '''
        test factory
        '''
        lmdi_1_0 = Lmdi(self.dmus_2006, self.dmus_2007, '2006-2007')
        lmdi_1_1 = Lmdi(self.dmus_2006, self.dmus_2007, '2006-2007')
        self.assertNotEqual(id(lmdi_1_0), id(lmdi_1_1))
        lmdi_2_0 = LmdiFactory.build(self.dmus_2006, self.dmus_2007, '2006-2007')
        lmdi_2_1 = LmdiFactory.build(self.dmus_2006, self.dmus_2007, '2006-2007')
        self.assertEqual(id(lmdi_2_0), id(lmdi_2_1))

if __name__ == '__main__':
    unittest.main()
