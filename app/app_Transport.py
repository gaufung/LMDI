# -*- coding:utf8 -*-
import sys
sys.path.append('..')
import math
import operator
import xlrd
import logging
import numpy as np
import  pandas as pd
import xlrd
from xlwt import *
from PDA_Transport.Data_Read import read_dmus
from PDA_Transport.config import *
from PDA_Transport.SinglePeriodAAM import Spaam
from PDA_Transport.MultiPeriodAAM import Mpaam
from PDA_Transport.LMDI import Lmdi

class AppLmdi(object):
    def __init__(self):
        dmus_2006 = read_dmus(DMUS_2006_DATA)
        dmus_2007 = read_dmus(DMUS_2007_DATA)
        dmus_2008 = read_dmus(DMUS_2008_DATA)
        dmus_2009 = read_dmus(DMUS_2009_DATA)
        dmus_2010 = read_dmus(DMUS_2010_DATA)
        dmus_2011 = read_dmus(DMUS_2011_DATA)
        dmus_2012 = read_dmus(DMUS_2012_DATA)
        dmus_2013 = read_dmus(DMUS_2013_DATA)
        dmus_2014 = read_dmus(DMUS_2014_DATA)
        global_dmus = [dmus_2006, dmus_2007, dmus_2008, dmus_2009, dmus_2010,
                       dmus_2011, dmus_2012, dmus_2013, dmus_2014]
        self.lmdi_2006_2007 = Lmdi.build(dmus_2006, dmus_2007, '2006-2007', global_dmus)
        self.lmdi_2007_2008 = Lmdi.build(dmus_2007, dmus_2008, '2007-2008', global_dmus)
        self.lmdi_2008_2009 = Lmdi.build(dmus_2008, dmus_2009, '2008-2009', global_dmus)
        self.lmdi_2009_2010 = Lmdi.build(dmus_2009, dmus_2010, '2009-2010', global_dmus)
        self.lmdi_2010_2011 = Lmdi.build(dmus_2010, dmus_2011, '2010-2011', global_dmus)
        self.lmdi_2011_2012 = Lmdi.build(dmus_2011, dmus_2012, '2011-2012', global_dmus)
        self.lmdi_2012_2013 = Lmdi.build(dmus_2012, dmus_2013, '2012-2013', global_dmus)
        self.lmdi_2013_2014 = Lmdi.build(dmus_2013, dmus_2014, '2013-2014', global_dmus)
        self.spaam_2006_2007 = Spaam(dmus_2006, dmus_2007, '2006-2007', global_dmus)
        self.spaam_2007_2008 = Spaam(dmus_2007, dmus_2008, '2007-2008', global_dmus)
        self.spaam_2008_2009 = Spaam(dmus_2008, dmus_2009, '2008-2009', global_dmus)
        self.spaam_2009_2010 = Spaam(dmus_2009, dmus_2010, '2009-2010', global_dmus)
        self.spaam_2010_2011 = Spaam(dmus_2010, dmus_2011, '2010-2011', global_dmus)
        self.spaam_2011_2012 = Spaam(dmus_2011, dmus_2012, '2011-2012', global_dmus)
        self.spaam_2012_2013 = Spaam(dmus_2012, dmus_2013, '2012-2013', global_dmus)
        self.spaam_2013_2014 = Spaam(dmus_2013, dmus_2014, '2013-2014', global_dmus)

        self.mpaam_2006_2007 = Mpaam([dmus_2006, dmus_2007], '2006-2007',global_dmus)
        self.mpaam_2006_2008 = Mpaam([dmus_2006, dmus_2007, dmus_2008], '2006-2008',global_dmus)
        self.mpaam_2006_2009 = Mpaam([dmus_2006, dmus_2007, dmus_2008, dmus_2009,
                                     ], '2006-2009', global_dmus)
        self.mpaam_2006_2010 = Mpaam([dmus_2006, dmus_2007, dmus_2008, dmus_2009,
                                      dmus_2010], '2006-2010', global_dmus)
        self.mpaam_2006_2011 = Mpaam([dmus_2006, dmus_2007, dmus_2008, dmus_2009,
                                      dmus_2010, dmus_2011], '2006-2011', global_dmus)
        self.mpaam_2006_2012 = Mpaam([dmus_2006, dmus_2007, dmus_2008, dmus_2009,
                                      dmus_2010, dmus_2011, dmus_2012], '2006-2012', global_dmus)
        self.mpaam_2006_2013 = Mpaam([dmus_2006, dmus_2007, dmus_2008, dmus_2009,
                                      dmus_2010, dmus_2011, dmus_2012, dmus_2013], '2006-2013', global_dmus)
        self.mpaam_2006_2014 = Mpaam([dmus_2006, dmus_2007, dmus_2008, dmus_2009,
                                      dmus_2010, dmus_2011, dmus_2012, dmus_2013,
                                      dmus_2014], '2006-2014', global_dmus)
        self.province_names = self.lmdi_2006_2007.province_names
    def _write_row(self, sheet, row, values):
        '''
        write a row
        '''
        column = 0
        for value in values:
            sheet.write(row, column, label=value)
            column += 1
    def _write_column(self, sheet, column, values):
        '''
        write a column
        '''
        row = 0
        for value in values:
            sheet.write(row, column, value)
            row += 1
    def write_lmdi_single(self, sheet):
        '''
        write single period lmdi
        '''
        columns = ['Period', 'Dcef', 'Demx', 'Dpei', 'Dest', 'Deue',
                   'Dpti', 'Dyoe', 'Dyct', 'Drts']
        self._write_row(sheet, 0, columns)
        self._write_row(sheet, 1, [self.spaam_2006_2007.name] + self.spaam_2006_2007.indexes)
        self._write_row(sheet, 2, [self.spaam_2007_2008.name] + self.spaam_2007_2008.indexes)
        self._write_row(sheet, 3, [self.spaam_2008_2009.name] + self.spaam_2008_2009.indexes)
        self._write_row(sheet, 4, [self.spaam_2009_2010.name] + self.spaam_2009_2010.indexes)
        self._write_row(sheet, 5, [self.spaam_2010_2011.name] + self.spaam_2010_2011.indexes)
        self._write_row(sheet, 6, [self.spaam_2011_2012.name] + self.spaam_2011_2012.indexes)
        self._write_row(sheet, 7, [self.spaam_2012_2013.name] + self.spaam_2012_2013.indexes)
        self._write_row(sheet, 8, [self.spaam_2013_2014.name] + self.spaam_2013_2014.indexes)
    def write_lmdi_multi(self, sheet):
        '''
        write multi period lmdi
        '''
        columns = ['Period', 'Dcef', 'Demx', 'Dpei', 'Dest', 'Deue',
                   'Dpti', 'Dyoe', 'Dyct', 'Drts']
        self._write_row(sheet, 0, columns)
        self._write_row(sheet, 1, ['2007'] + self.mpaam_2006_2014.indexes(1))
        self._write_row(sheet, 2, ['2008'] + self.mpaam_2006_2014.indexes(2))
        self._write_row(sheet, 3, ['2009'] + self.mpaam_2006_2014.indexes(3))
        self._write_row(sheet, 4, ['2010'] + self.mpaam_2006_2014.indexes(4))
        self._write_row(sheet, 5, ['2011'] + self.mpaam_2006_2014.indexes(5))
        self._write_row(sheet, 6, ['2012'] + self.mpaam_2006_2014.indexes(6))
        self._write_row(sheet, 7, ['2013'] + self.mpaam_2006_2014.indexes(7))
        self._write_row(sheet, 8, ['2014'] + self.mpaam_2006_2014.indexes(8))
    def write_multi_lmdi(self, save_file_name):
        '''
        write multi lmdi
        '''
        workbook = Workbook(encoding='utf8')
        self._write_lmdi_index(workbook, 'cef', 'emx', 'pei', 'est',
                               'eue', 'pti', 'yoe', 'yct', 'rts')
        workbook.save(save_file_name)
    def _write_lmdi_index(self, workbook, *indexes):
        for index in indexes:
            sheet = workbook.add_sheet(index)
            self._write_column(sheet, 0, ['Province']+self.province_names)
            self._write_column(sheet, 1, ['2007']+list(getattr(self.lmdi_2006_2007, index)()))
            self._write_column(sheet, 2, ['2008']+list(getattr(self.lmdi_2007_2008, index)()))
            self._write_column(sheet, 3, ['2009']+list(getattr(self.lmdi_2008_2009, index)()))
            self._write_column(sheet, 4, ['2010']+list(getattr(self.lmdi_2009_2010, index)()))
            self._write_column(sheet, 5, ['2011']+list(getattr(self.lmdi_2010_2011, index)()))
            self._write_column(sheet, 6, ['2012']+list(getattr(self.lmdi_2011_2012, index)()))
            self._write_column(sheet, 7, ['2013']+list(getattr(self.lmdi_2012_2013, index)()))
            self._write_column(sheet, 8, ['2014']+list(getattr(self.lmdi_2013_2014, index)()))
    def write_linear_program(self, save_file_name):
        '''
        write linear programming result
        '''
        workbook = Workbook(encoding='utf8')
        self._write_lmdi(workbook, self.lmdi_2006_2007)
        self._write_lmdi(workbook, self.lmdi_2007_2008)
        self._write_lmdi(workbook, self.lmdi_2008_2009)
        self._write_lmdi(workbook, self.lmdi_2009_2010)
        self._write_lmdi(workbook, self.lmdi_2010_2011)
        self._write_lmdi(workbook, self.lmdi_2011_2012)
        self._write_lmdi(workbook, self.lmdi_2012_2013)
        self._write_lmdi(workbook, self.lmdi_2013_2014)
        workbook.save(save_file_name)
    def _write_lmdi(self, workbook, lmdi):
        sheet = workbook.add_sheet(lmdi.name)
        self._write_column(sheet, 0, ['省份']+self.province_names)
        self._write_column(sheet, 1, ['psi_t_t']+lmdi.psi_t_t)
        self._write_column(sheet, 2, ['psi_t1_t1']+lmdi.psi_t1_t1)
        self._write_column(sheet, 3, ['psi_global_t']+lmdi.psi_global_t)
        self._write_column(sheet, 4, ['psi_global_t1']+ lmdi.psi_global_t1)
        self._write_column(sheet, 5, ['eta_t_t']+lmdi.eta_t_t)
        self._write_column(sheet, 6, ['eta_t1_t1']+lmdi.eta_t1_t1)
        self._write_column(sheet, 7, ['eta_global_t']+lmdi.eta_global_t)
        self._write_column(sheet, 8, ['eta_global_t1']+ lmdi.eta_global_t1)
    def write_single_attribution(self, save_file_name):
        '''
        single attribution
        '''
        workbook = Workbook(encoding='utf8')
        self._write_single_indexes(workbook, 'cef', 'emx', 'pei', 'est',
                                   'eue', 'pti', 'yoe', 'yct', 'rts')
        workbook.save(save_file_name)
    def _write_single_indexes(self, workbook, *indexes):
        for index in indexes:
            sheet = workbook.add_sheet(index)
            index_attributions = index + '_attributions'
            self._write_column(sheet, 0, ['Province']+self.province_names)
            self._write_column(sheet, 1, ['2007'] + [item * 100 for item
                                                     in getattr(self.spaam_2006_2007,
                                                                index_attributions)])
            self._write_column(sheet, 2, ['2008'] + [item * 100 for item
                                                     in getattr(self.spaam_2007_2008,
                                                                index_attributions)])
            self._write_column(sheet, 3, ['2009'] + [item * 100 for item
                                                     in getattr(self.spaam_2008_2009,
                                                                index_attributions)])
            self._write_column(sheet, 4, ['2010'] + [item * 100 for item
                                                    in getattr(self.spaam_2009_2010,
                                                               index_attributions)])
            self._write_column(sheet, 5, ['2011'] + [item * 100 for item
                                                    in getattr(self.spaam_2010_2011,
                                                               index_attributions)])
            self._write_column(sheet, 6, ['2012'] + [item * 100 for item
                                                    in getattr(self.spaam_2011_2012,
                                                               index_attributions)])
            self._write_column(sheet, 7, ['2013'] + [item * 100 for item
                                                    in getattr(self.spaam_2012_2013,
                                                               index_attributions)])
            self._write_column(sheet, 8, ['2014'] + [item * 100 for item
                                                    in getattr(self.spaam_2013_2014,
                                                               index_attributions)])
    def write_multi_attribution(self, save_file_name):
        '''
        write multi attribution
        '''
        workbook = Workbook(encoding='utf8')
        self._write_multi_index(workbook, 'cef', 'emx', 'pei', 'est',
                                'eue', 'pti', 'yoe', 'yct', 'rts')
        workbook.save(save_file_name)
    def _write_multi_index(self, workbook, *indexes):
        for index in indexes:
            sheet = workbook.add_sheet(index)
            self._write_column(sheet, 0, ['Province']+self.province_names)
            self._write_column(sheet, 1, ['2007'] + [item *100 for item
                                                     in getattr(self.mpaam_2006_2007, index)()])
            self._write_column(sheet, 2, ['2008'] + [item *100 for item
                                                     in getattr(self.mpaam_2006_2008, index)()])                                     
            self._write_column(sheet, 3, ['2009'] + [item *100 for item
                                                 in getattr(self.mpaam_2006_2009, index)()])                                       
            self._write_column(sheet, 4, ['2010'] + [item *100 for item
                                                 in getattr(self.mpaam_2006_2010, index)()])                                     
            self._write_column(sheet, 5, ['2011'] + [item *100 for item
                                                 in getattr(self.mpaam_2006_2011, index)()])                                     
            self._write_column(sheet, 6, ['2012'] + [item *100 for item
                                                 in getattr(self.mpaam_2006_2012, index)()])                                       
            self._write_column(sheet, 7, ['2013'] + [item *100 for item
                                                 in getattr(self.mpaam_2006_2013, index)()])                                   
            self._write_column(sheet, 8, ['2014'] + [item *100 for item
                                                 in getattr(self.mpaam_2006_2014, index)()])
if __name__ == '__main__':
    app = AppLmdi()
    '''
    workbook = Workbook(encoding='utf8')
    app.write_lmdi_single(workbook.add_sheet('单期LMDI'))
    app.write_lmdi_multi(workbook.add_sheet('跨期LMDI'))
    workbook.save('out/LMDI单期和跨期.xls'
    '''
    #app.write_multi_lmdi('out1/省份lmdi明细.xls')
    app.write_single_attribution('out1/单期归因1.xls')
    app.write_multi_attribution('out1/跨期归因1.xls')
    #app.write_linear_program('out/线性规划.xls')