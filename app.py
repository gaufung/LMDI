# -*- coding:utf8 -*-
import DataRead
import xlrd
import GlobalVaribales
import LMDI
import logging
from xlwt import *
import math
import operator
import Algorithm
import numpy as np
import pandas as pd 
# 
logging.basicConfig(level=logging.ERROR)
class AppLmdi(object):
    '''
    the lmdi application
    '''
    def __init__(self):
        dmus_2006 = DataRead.read_dmus(GlobalVaribales.PRO_2006_COL, GlobalVaribales.SHEET_2006)
        dmus_2007 = DataRead.read_dmus(GlobalVaribales.PRO_2007_COL, GlobalVaribales.SHEET_2007)
        dmus_2008 = DataRead.read_dmus(GlobalVaribales.PRO_2008_COL, GlobalVaribales.SHEET_2008)
        dmus_2009 = DataRead.read_dmus(GlobalVaribales.PRO_2009_COL, GlobalVaribales.SHEET_2009)
        dmus_2010 = DataRead.read_dmus(GlobalVaribales.PRO_2010_COL, GlobalVaribales.SHEET_2010)
        dmus_2011 = DataRead.read_dmus(GlobalVaribales.PRO_2011_COL, GlobalVaribales.SHEET_2011)
        dmus_2012 = DataRead.read_dmus(GlobalVaribales.PRO_2012_COL, GlobalVaribales.SHEET_2012)
        dmus_2013 = DataRead.read_dmus(GlobalVaribales.PRO_2013_COL, GlobalVaribales.SHEET_2013)
        dmus_2014 = DataRead.read_dmus(GlobalVaribales.PRO_2014_COL, GlobalVaribales.SHEET_2014)
        self.lmdi_2006_2007 = LMDI.Lmdi(dmus_2006, dmus_2007)
        self.lmdi_2007_2008 = LMDI.Lmdi(dmus_2007, dmus_2008)
        self.lmdi_2008_2009 = LMDI.Lmdi(dmus_2008, dmus_2009)
        self.lmdi_2009_2010 = LMDI.Lmdi(dmus_2009, dmus_2010)
        self.lmdi_2010_2011 = LMDI.Lmdi(dmus_2010, dmus_2011)
        self.lmdi_2011_2012 = LMDI.Lmdi(dmus_2011, dmus_2012)
        self.lmdi_2012_2013 = LMDI.Lmdi(dmus_2012, dmus_2013)
        self.lmdi_2013_2014 = LMDI.Lmdi(dmus_2013, dmus_2014)
        self.lmdi_2006_2014 = LMDI.Lmdi(dmus_2006, dmus_2014)

    def write_single_factor(self):
        '''
        write signle factor
        '''
        workbook = Workbook(encoding='utf8')
        self.lmdi_2006_2007.write(workbook, '2006-2007')
        self.lmdi_2007_2008.write(workbook, '2007-2008')
        self.lmdi_2008_2009.write(workbook, '2008-2009')
        self.lmdi_2009_2010.write(workbook, '2009-2010')
        self.lmdi_2010_2011.write(workbook, '2010-2011')
        self.lmdi_2011_2012.write(workbook, '2011-2012')
        self.lmdi_2012_2013.write(workbook, '2012-2013')
        self.lmdi_2013_2014.write(workbook, '2013-2014')
        self.lmdi_2006_2014.write(workbook, '2006-2014')
        workbook.save('factors_complete_checked.xls')

    def _create_value(self, frame):
        '''
        $e^{\sum_{i}^{30}factor}$
        '''
        for _, row in frame.iterrows():
            yield math.exp(row.values.sum())

    def check_factors_multiply(self):
        '''
        build dataframe
        '''
        frame_emx = pd.DataFrame({'2006-2007':list(self.lmdi_2006_2007.emx()),
                                  '2007-2008':list(self.lmdi_2007_2008.emx()),
                                  '2008-2009':list(self.lmdi_2008_2009.emx()),
                                  '2009-2010':list(self.lmdi_2009_2010.emx()),
                                  '2010-2011':list(self.lmdi_2010_2011.emx()),
                                  '2011-2012':list(self.lmdi_2011_2012.emx()),
                                  '2012-2013':list(self.lmdi_2012_2013.emx()),
                                  '2013-2014':list(self.lmdi_2013_2014.emx())})
        frame_pei = pd.DataFrame({'2006-2007':list(self.lmdi_2006_2007.pei()),
                                  '2007-2008':list(self.lmdi_2007_2008.pei()),
                                  '2008-2009':list(self.lmdi_2008_2009.pei()),
                                  '2009-2010':list(self.lmdi_2009_2010.pei()),
                                  '2010-2011':list(self.lmdi_2010_2011.pei()),
                                  '2011-2012':list(self.lmdi_2011_2012.pei()),
                                  '2012-2013':list(self.lmdi_2012_2013.pei()),
                                  '2013-2014':list(self.lmdi_2013_2014.pei())})
        frame_pis = pd.DataFrame({'2006-2007':list(self.lmdi_2006_2007.pis()),
                                  '2007-2008':list(self.lmdi_2007_2008.pis()),
                                  '2008-2009':list(self.lmdi_2008_2009.pis()),
                                  '2009-2010':list(self.lmdi_2009_2010.pis()),
                                  '2010-2011':list(self.lmdi_2010_2011.pis()),
                                  '2011-2012':list(self.lmdi_2011_2012.pis()),
                                  '2012-2013':list(self.lmdi_2012_2013.pis()),
                                  '2013-2014':list(self.lmdi_2013_2014.pis())})
        frame_isg = pd.DataFrame({'2006-2007':list(self.lmdi_2006_2007.isg()),
                                  '2007-2008':list(self.lmdi_2007_2008.isg()),
                                  '2008-2009':list(self.lmdi_2008_2009.isg()),
                                  '2009-2010': list(self.lmdi_2009_2010.isg()),
                                  '2010-2011':list(self.lmdi_2010_2011.isg()),
                                  '2011-2012':list(self.lmdi_2011_2012.isg()),
                                  '2012-2013':list(self.lmdi_2012_2013.isg()),
                                  '2013-2014':list(self.lmdi_2013_2014.isg())})
        frame_eue = pd.DataFrame({'2006-2007':list(self.lmdi_2006_2007.eue()),
                                  '2007-2008':list(self.lmdi_2007_2008.eue()),
                                  '2008-2009':list(self.lmdi_2008_2009.eue()),
                                  '2009-2010': list(self.lmdi_2009_2010.eue()),
                                  '2010-2011':list(self.lmdi_2010_2011.eue()),
                                  '2011-2012':list(self.lmdi_2011_2012.eue()),
                                  '2012-2013':list(self.lmdi_2012_2013.eue()),
                                  '2013-2014':list(self.lmdi_2013_2014.eue())})
        frame_est = pd.DataFrame({'2006-2007':list(self.lmdi_2006_2007.est()),
                                  '2007-2008':list(self.lmdi_2007_2008.est()),
                                  '2008-2009':list(self.lmdi_2008_2009.est()),
                                  '2009-2010': list(self.lmdi_2009_2010.est()),
                                  '2010-2011':list(self.lmdi_2010_2011.est()),
                                  '2011-2012':list(self.lmdi_2011_2012.est()),
                                  '2012-2013':list(self.lmdi_2012_2013.est()),
                                  '2013-2014':list(self.lmdi_2013_2014.est())})
        frame_yoe = pd.DataFrame({'2006-2007':list(self.lmdi_2006_2007.yoe()),
                                  '2007-2008':list(self.lmdi_2007_2008.yoe()),
                                  '2008-2009':list(self.lmdi_2008_2009.yoe()),
                                  '2009-2010': list(self.lmdi_2009_2010.yoe()),
                                  '2010-2011':list(self.lmdi_2010_2011.yoe()),
                                  '2011-2012':list(self.lmdi_2011_2012.yoe()),
                                  '2012-2013':list(self.lmdi_2012_2013.yoe()),
                                  '2013-2014':list(self.lmdi_2013_2014.yoe())})
        frame_yct = pd.DataFrame({'2006-2007':list(self.lmdi_2006_2007.yct()),
                                  '2007-2008':list(self.lmdi_2007_2008.yct()),
                                  '2008-2009':list(self.lmdi_2008_2009.yct()),
                                  '2009-2010': list(self.lmdi_2009_2010.yct()),
                                  '2010-2011':list(self.lmdi_2010_2011.yct()),
                                  '2011-2012':list(self.lmdi_2011_2012.yct()),
                                  '2012-2013':list(self.lmdi_2012_2013.yct()),
                                  '2013-2014':list(self.lmdi_2013_2014.yct())})
        frame_totoal = pd.DataFrame({'emx':list(self._create_value(frame_emx)),
                                     'pei':list(self._create_value(frame_pei)),
                                     'pis':list(self._create_value(frame_pis)),
                                     'isg':list(self._create_value(frame_isg)),
                                     'eue':list(self._create_value(frame_eue)),
                                     'est':list(self._create_value(frame_est)),
                                     'yoe':list(self._create_value(frame_yoe)),
                                     'yct':list(self._create_value(frame_yct))},
                                index=self.lmdi_2006_2007.province_names)                
        frame_totoal.to_excel('factor_multiply.xls', 'result')

class AppAttribute(object):
    def __init__(self):
        dmus_2006 = DataRead.read_dmus(GlobalVaribales.PRO_2006_COL, GlobalVaribales.SHEET_2006)
        dmus_2007 = DataRead.read_dmus(GlobalVaribales.PRO_2007_COL, GlobalVaribales.SHEET_2007)
        self.lmdi_2006_2007 = LMDI.Lmdi(dmus_2006, dmus_2007)
        print sum([k*v for k,v in zip(self.lmdi_2006_2007.rpei(), self.lmdi_2006_2007.peiRatio())])
        print math.exp(sum(list(self.lmdi_2006_2007.pei()))) - 1
if __name__ == '__main__':
    app = AppAttribute()
    #app.check_factors_multiply()