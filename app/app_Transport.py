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
        self._write_lmid_cef(workbook.add_sheet('cef'))
        self._write_lmid_emx(workbook.add_sheet('emx'))
        self._write_lmid_pei(workbook.add_sheet('pei'))
        self._write_lmid_est(workbook.add_sheet('est'))
        self._write_lmid_eue(workbook.add_sheet('eue'))
        self._write_lmid_pti(workbook.add_sheet('pti'))
        self._write_lmid_yoe(workbook.add_sheet('yoe'))
        self._write_lmid_yct(workbook.add_sheet('yct'))
        self._write_lmid_rts(workbook.add_sheet('rts'))
        workbook.save(save_file_name)
    def _write_lmid_cef(self, sheet):
        self._write_column(sheet, 0, ['Province']+self.province_names)
        self._write_column(sheet, 1, ['2007']+list(self.lmdi_2006_2007.cef()))
        self._write_column(sheet, 2, ['2008']+list(self.lmdi_2007_2008.cef()))
        self._write_column(sheet, 3, ['2009']+list(self.lmdi_2008_2009.cef()))
        self._write_column(sheet, 4, ['2010']+list(self.lmdi_2009_2010.cef()))
        self._write_column(sheet, 5, ['2011']+list(self.lmdi_2010_2011.cef()))
        self._write_column(sheet, 6, ['2012']+list(self.lmdi_2011_2012.cef()))
        self._write_column(sheet, 7, ['2013']+list(self.lmdi_2012_2013.cef()))
        self._write_column(sheet, 8, ['2014']+list(self.lmdi_2013_2014.cef()))
    def _write_lmid_emx(self, sheet):
        self._write_column(sheet, 0, ['Province']+self.province_names)
        self._write_column(sheet, 1, ['2007']+list(self.lmdi_2006_2007.emx()))
        self._write_column(sheet, 2, ['2008']+list(self.lmdi_2007_2008.emx()))
        self._write_column(sheet, 3, ['2009']+list(self.lmdi_2008_2009.emx()))
        self._write_column(sheet, 4, ['2010']+list(self.lmdi_2009_2010.emx()))
        self._write_column(sheet, 5, ['2011']+list(self.lmdi_2010_2011.emx()))
        self._write_column(sheet, 6, ['2012']+list(self.lmdi_2011_2012.emx()))
        self._write_column(sheet, 7, ['2013']+list(self.lmdi_2012_2013.emx()))
        self._write_column(sheet, 8, ['2014']+list(self.lmdi_2013_2014.emx()))
    def _write_lmid_pei(self, sheet):
        self._write_column(sheet, 0, ['Province']+self.province_names)
        self._write_column(sheet, 1, ['2007']+list(self.lmdi_2006_2007.pei()))
        self._write_column(sheet, 2, ['2008']+list(self.lmdi_2007_2008.pei()))
        self._write_column(sheet, 3, ['2009']+list(self.lmdi_2008_2009.pei()))
        self._write_column(sheet, 4, ['2010']+list(self.lmdi_2009_2010.pei()))
        self._write_column(sheet, 5, ['2011']+list(self.lmdi_2010_2011.pei()))
        self._write_column(sheet, 6, ['2012']+list(self.lmdi_2011_2012.pei()))
        self._write_column(sheet, 7, ['2013']+list(self.lmdi_2012_2013.pei()))
        self._write_column(sheet, 8, ['2014']+list(self.lmdi_2013_2014.pei()))
    def _write_lmid_est(self, sheet):
        self._write_column(sheet, 0, ['Province']+self.province_names)
        self._write_column(sheet, 1, ['2007']+list(self.lmdi_2006_2007.est()))
        self._write_column(sheet, 2, ['2008']+list(self.lmdi_2007_2008.est()))
        self._write_column(sheet, 3, ['2009']+list(self.lmdi_2008_2009.est()))
        self._write_column(sheet, 4, ['2010']+list(self.lmdi_2009_2010.est()))
        self._write_column(sheet, 5, ['2011']+list(self.lmdi_2010_2011.est()))
        self._write_column(sheet, 6, ['2012']+list(self.lmdi_2011_2012.est()))
        self._write_column(sheet, 7, ['2013']+list(self.lmdi_2012_2013.est()))
        self._write_column(sheet, 8, ['2014']+list(self.lmdi_2013_2014.est()))
    def _write_lmid_pti(self, sheet):
        self._write_column(sheet, 0, ['Province']+self.province_names)
        self._write_column(sheet, 1, ['2007']+list(self.lmdi_2006_2007.pti()))
        self._write_column(sheet, 2, ['2008']+list(self.lmdi_2007_2008.pti()))
        self._write_column(sheet, 3, ['2009']+list(self.lmdi_2008_2009.pti()))
        self._write_column(sheet, 4, ['2010']+list(self.lmdi_2009_2010.pti()))
        self._write_column(sheet, 5, ['2011']+list(self.lmdi_2010_2011.pti()))
        self._write_column(sheet, 6, ['2012']+list(self.lmdi_2011_2012.pti()))
        self._write_column(sheet, 7, ['2013']+list(self.lmdi_2012_2013.pti()))
        self._write_column(sheet, 8, ['2014']+list(self.lmdi_2013_2014.pti()))
    def _write_lmid_eue(self, sheet):
        self._write_column(sheet, 0, ['Province']+self.province_names)
        self._write_column(sheet, 1, ['2007']+list(self.lmdi_2006_2007.eue()))
        self._write_column(sheet, 2, ['2008']+list(self.lmdi_2007_2008.eue()))
        self._write_column(sheet, 3, ['2009']+list(self.lmdi_2008_2009.eue()))
        self._write_column(sheet, 4, ['2010']+list(self.lmdi_2009_2010.eue()))
        self._write_column(sheet, 5, ['2011']+list(self.lmdi_2010_2011.eue()))
        self._write_column(sheet, 6, ['2012']+list(self.lmdi_2011_2012.eue()))
        self._write_column(sheet, 7, ['2013']+list(self.lmdi_2012_2013.eue()))
        self._write_column(sheet, 8, ['2014']+list(self.lmdi_2013_2014.eue()))
    def _write_lmid_rts(self, sheet):
        self._write_column(sheet, 0, ['Province']+self.province_names)
        self._write_column(sheet, 1, ['2007']+list(self.lmdi_2006_2007.rts()))
        self._write_column(sheet, 2, ['2008']+list(self.lmdi_2007_2008.rts()))
        self._write_column(sheet, 3, ['2009']+list(self.lmdi_2008_2009.rts()))
        self._write_column(sheet, 4, ['2010']+list(self.lmdi_2009_2010.rts()))
        self._write_column(sheet, 5, ['2011']+list(self.lmdi_2010_2011.rts()))
        self._write_column(sheet, 6, ['2012']+list(self.lmdi_2011_2012.rts()))
        self._write_column(sheet, 7, ['2013']+list(self.lmdi_2012_2013.rts()))
        self._write_column(sheet, 8, ['2014']+list(self.lmdi_2013_2014.rts()))
    def _write_lmid_yoe(self, sheet):
        self._write_column(sheet, 0, ['Province']+self.province_names)
        self._write_column(sheet, 1, ['2007']+list(self.lmdi_2006_2007.yoe()))
        self._write_column(sheet, 2, ['2008']+list(self.lmdi_2007_2008.yoe()))
        self._write_column(sheet, 3, ['2009']+list(self.lmdi_2008_2009.yoe()))
        self._write_column(sheet, 4, ['2010']+list(self.lmdi_2009_2010.yoe()))
        self._write_column(sheet, 5, ['2011']+list(self.lmdi_2010_2011.yoe()))
        self._write_column(sheet, 6, ['2012']+list(self.lmdi_2011_2012.yoe()))
        self._write_column(sheet, 7, ['2013']+list(self.lmdi_2012_2013.yoe()))
        self._write_column(sheet, 8, ['2014']+list(self.lmdi_2013_2014.yoe()))
    def _write_lmid_yct(self, sheet):
        self._write_column(sheet, 0, ['Province']+self.province_names)
        self._write_column(sheet, 1, ['2007']+list(self.lmdi_2006_2007.yct()))
        self._write_column(sheet, 2, ['2008']+list(self.lmdi_2007_2008.yct()))
        self._write_column(sheet, 3, ['2009']+list(self.lmdi_2008_2009.yct()))
        self._write_column(sheet, 4, ['2010']+list(self.lmdi_2009_2010.yct()))
        self._write_column(sheet, 5, ['2011']+list(self.lmdi_2010_2011.yct()))
        self._write_column(sheet, 6, ['2012']+list(self.lmdi_2011_2012.yct()))
        self._write_column(sheet, 7, ['2013']+list(self.lmdi_2012_2013.yct()))
        self._write_column(sheet, 8, ['2014']+list(self.lmdi_2013_2014.yct()))
    
    def write_single_attribution(self, save_file_name):
        workbook = Workbook(encoding='utf8')
        self._write_single_cef(workbook.add_sheet('cef'))
        self._write_single_emx(workbook.add_sheet('emx'))
        self._write_single_pei(workbook.add_sheet('pei'))
        self._write_single_est(workbook.add_sheet('est'))
        self._write_single_eue(workbook.add_sheet('eue'))
        self._write_single_pti(workbook.add_sheet('pti'))
        self._write_single_yoe(workbook.add_sheet('yoe'))
        self._write_single_yct(workbook.add_sheet('yct'))
        self._write_single_rts(workbook.add_sheet('rts'))
        workbook.save(save_file_name)
    def _write_single_cef(self, sheet):
        '''
        write single cef
        '''
        self._write_column(sheet, 0, ['Province']+self.province_names)
        self._write_column(sheet, 1, ['2007'] + [item * 100 for item
                                                 in self.spaam_2006_2007.cef_attributions])
        self._write_column(sheet, 2, ['2008'] + [item * 100 for item
                                                 in self.spaam_2007_2008.cef_attributions])
        self._write_column(sheet, 3, ['2009'] + [item * 100 for item
                                                 in self.spaam_2008_2009.cef_attributions])
        self._write_column(sheet, 4, ['2010'] + [item * 100 for item
                                                 in self.spaam_2009_2010.cef_attributions])
        self._write_column(sheet, 5, ['2011'] + [item * 100 for item
                                                 in self.spaam_2010_2011.cef_attributions])
        self._write_column(sheet, 6, ['2012'] + [item * 100 for item
                                                 in self.spaam_2011_2012.cef_attributions])
        self._write_column(sheet, 7, ['2013'] + [item * 100 for item
                                                 in self.spaam_2012_2013.cef_attributions])
        self._write_column(sheet, 8, ['2014'] + [item * 100 for item
                                                 in self.spaam_2013_2014.cef_attributions])
    def _write_single_emx(self, sheet):
        '''
        write single emx
        '''
        self._write_column(sheet, 0, ['Province']+self.province_names)
        self._write_column(sheet, 1, ['2007'] + [item * 100 for item
                                                 in self.spaam_2006_2007.emx_attributions])
        self._write_column(sheet, 2, ['2008'] + [item * 100 for item
                                                 in self.spaam_2007_2008.emx_attributions])
        self._write_column(sheet, 3, ['2009'] + [item * 100 for item
                                                 in self.spaam_2008_2009.emx_attributions])
        self._write_column(sheet, 4, ['2010'] + [item * 100 for item
                                                 in self.spaam_2009_2010.emx_attributions])
        self._write_column(sheet, 5, ['2011'] + [item * 100 for item
                                                 in self.spaam_2010_2011.emx_attributions])
        self._write_column(sheet, 6, ['2012'] + [item * 100 for item
                                                 in self.spaam_2011_2012.emx_attributions])
        self._write_column(sheet, 7, ['2013'] + [item * 100 for item
                                                 in self.spaam_2012_2013.emx_attributions])
        self._write_column(sheet, 8, ['2014'] + [item * 100 for item
                                                 in self.spaam_2013_2014.emx_attributions])
    def _write_single_pei(self, sheet):
        '''
        write single emx
        '''
        self._write_column(sheet, 0, ['Province']+self.province_names)
        self._write_column(sheet, 1, ['2007'] + [item * 100 for item
                                                 in self.spaam_2006_2007.pei_attributions])
        self._write_column(sheet, 2, ['2008'] + [item * 100 for item
                                                 in self.spaam_2007_2008.pei_attributions])
        self._write_column(sheet, 3, ['2009'] + [item * 100 for item
                                                 in self.spaam_2008_2009.pei_attributions])
        self._write_column(sheet, 4, ['2010'] + [item * 100 for item
                                                 in self.spaam_2009_2010.pei_attributions])
        self._write_column(sheet, 5, ['2011'] + [item * 100 for item
                                                 in self.spaam_2010_2011.pei_attributions])
        self._write_column(sheet, 6, ['2012'] + [item * 100 for item
                                                 in self.spaam_2011_2012.pei_attributions])
        self._write_column(sheet, 7, ['2013'] + [item * 100 for item
                                                 in self.spaam_2012_2013.pei_attributions])
        self._write_column(sheet, 8, ['2014'] + [item * 100 for item
                                                 in self.spaam_2013_2014.pei_attributions])
    def _write_single_rts(self, sheet):
        '''
        write single emx
        '''
        self._write_column(sheet, 0, ['Province']+self.province_names)
        self._write_column(sheet, 1, ['2007'] + [item * 100 for item
                                                 in self.spaam_2006_2007.rts_attributions])
        self._write_column(sheet, 2, ['2008'] + [item * 100 for item
                                                 in self.spaam_2007_2008.rts_attributions])
        self._write_column(sheet, 3, ['2009'] + [item * 100 for item
                                                 in self.spaam_2008_2009.rts_attributions])
        self._write_column(sheet, 4, ['2010'] + [item * 100 for item
                                                 in self.spaam_2009_2010.rts_attributions])
        self._write_column(sheet, 5, ['2011'] + [item * 100 for item
                                                 in self.spaam_2010_2011.rts_attributions])
        self._write_column(sheet, 6, ['2012'] + [item * 100 for item
                                                 in self.spaam_2011_2012.rts_attributions])
        self._write_column(sheet, 7, ['2013'] + [item * 100 for item
                                                 in self.spaam_2012_2013.rts_attributions])
        self._write_column(sheet, 8, ['2014'] + [item * 100 for item
                                                 in self.spaam_2013_2014.rts_attributions])
        
    def _write_single_pti(self, sheet):
        '''
        write single emx
        '''
        self._write_column(sheet, 0, ['Province']+self.province_names)
        self._write_column(sheet, 1, ['2007'] + [item * 100 for item
                                                 in self.spaam_2006_2007.pti_attributions])
        self._write_column(sheet, 2, ['2008'] + [item * 100 for item
                                                 in self.spaam_2007_2008.pti_attributions])
        self._write_column(sheet, 3, ['2009'] + [item * 100 for item
                                                 in self.spaam_2008_2009.pti_attributions])
        self._write_column(sheet, 4, ['2010'] + [item * 100 for item
                                                 in self.spaam_2009_2010.pti_attributions])
        self._write_column(sheet, 5, ['2011'] + [item * 100 for item
                                                 in self.spaam_2010_2011.pti_attributions])
        self._write_column(sheet, 6, ['2012'] + [item * 100 for item
                                                 in self.spaam_2011_2012.pti_attributions])
        self._write_column(sheet, 7, ['2013'] + [item * 100 for item
                                                 in self.spaam_2012_2013.pti_attributions])
        self._write_column(sheet, 8, ['2014'] + [item * 100 for item
                                                 in self.spaam_2013_2014.pti_attributions])
    def _write_single_eue(self, sheet):
        '''
        write single emx
        '''
        self._write_column(sheet, 0, ['Province']+self.province_names)
        self._write_column(sheet, 1, ['2007'] + [item * 100 for item
                                                 in self.spaam_2006_2007.eue_attributions])
        self._write_column(sheet, 2, ['2008'] + [item * 100 for item
                                                 in self.spaam_2007_2008.eue_attributions])
        self._write_column(sheet, 3, ['2009'] + [item * 100 for item
                                                 in self.spaam_2008_2009.eue_attributions])
        self._write_column(sheet, 4, ['2010'] + [item * 100 for item
                                                 in self.spaam_2009_2010.eue_attributions])
        self._write_column(sheet, 5, ['2011'] + [item * 100 for item
                                                 in self.spaam_2010_2011.eue_attributions])
        self._write_column(sheet, 6, ['2012'] + [item * 100 for item
                                                 in self.spaam_2011_2012.eue_attributions])
        self._write_column(sheet, 7, ['2013'] + [item * 100 for item
                                                 in self.spaam_2012_2013.eue_attributions])
        self._write_column(sheet, 8, ['2014'] + [item * 100 for item
                                                 in self.spaam_2013_2014.eue_attributions])
    def _write_single_est(self, sheet):
        '''
        write single emx
        '''
        self._write_column(sheet, 0, ['Province']+self.province_names)
        self._write_column(sheet, 1, ['2007'] + [item * 100 for item
                                                 in self.spaam_2006_2007.est_attributions])
        self._write_column(sheet, 2, ['2008'] + [item * 100 for item
                                                 in self.spaam_2007_2008.est_attributions])
        self._write_column(sheet, 3, ['2009'] + [item * 100 for item
                                                 in self.spaam_2008_2009.est_attributions])
        self._write_column(sheet, 4, ['2010'] + [item * 100 for item
                                                 in self.spaam_2009_2010.est_attributions])
        self._write_column(sheet, 5, ['2011'] + [item * 100 for item
                                                 in self.spaam_2010_2011.est_attributions])
        self._write_column(sheet, 6, ['2012'] + [item * 100 for item
                                                 in self.spaam_2011_2012.est_attributions])
        self._write_column(sheet, 7, ['2013'] + [item * 100 for item
                                                 in self.spaam_2012_2013.est_attributions])
        self._write_column(sheet, 8, ['2014'] + [item * 100 for item
                                                 in self.spaam_2013_2014.est_attributions])
    def _write_single_yoe(self, sheet):
        '''
        write single emx
        '''
        self._write_column(sheet, 0, ['Province']+self.province_names)
        self._write_column(sheet, 1, ['2007'] + [item * 100 for item
                                                 in self.spaam_2006_2007.yoe_attributions])
        self._write_column(sheet, 2, ['2008'] + [item * 100 for item
                                                 in self.spaam_2007_2008.yoe_attributions])
        self._write_column(sheet, 3, ['2009'] + [item * 100 for item
                                                 in self.spaam_2008_2009.yoe_attributions])
        self._write_column(sheet, 4, ['2010'] + [item * 100 for item
                                                 in self.spaam_2009_2010.yoe_attributions])
        self._write_column(sheet, 5, ['2011'] + [item * 100 for item
                                                 in self.spaam_2010_2011.yoe_attributions])
        self._write_column(sheet, 6, ['2012'] + [item * 100 for item
                                                 in self.spaam_2011_2012.yoe_attributions])
        self._write_column(sheet, 7, ['2013'] + [item * 100 for item
                                                 in self.spaam_2012_2013.yoe_attributions])
        self._write_column(sheet, 8, ['2014'] + [item * 100 for item
                                                 in self.spaam_2013_2014.yoe_attributions])
    def _write_single_yct(self, sheet):
        '''
        write single emx
        '''
        self._write_column(sheet, 0, ['Province']+self.province_names)
        self._write_column(sheet, 1, ['2007'] + [item * 100 for item
                                                 in self.spaam_2006_2007.yct_attributions])
        self._write_column(sheet, 2, ['2008'] + [item * 100 for item
                                                 in self.spaam_2007_2008.yct_attributions])
        self._write_column(sheet, 3, ['2009'] + [item * 100 for item
                                                 in self.spaam_2008_2009.yct_attributions])
        self._write_column(sheet, 4, ['2010'] + [item * 100 for item
                                                 in self.spaam_2009_2010.yct_attributions])
        self._write_column(sheet, 5, ['2011'] + [item * 100 for item
                                                 in self.spaam_2010_2011.yct_attributions])
        self._write_column(sheet, 6, ['2012'] + [item * 100 for item
                                                 in self.spaam_2011_2012.yct_attributions])
        self._write_column(sheet, 7, ['2013'] + [item * 100 for item
                                                 in self.spaam_2012_2013.yct_attributions])
        self._write_column(sheet, 8, ['2014'] + [item * 100 for item
                                                 in self.spaam_2013_2014.yct_attributions])
    
    def write_multi_attribution(self, save_file_name):
        '''
        write multi attribution
        '''
        workbook = Workbook(encoding='utf8')
        self._write_multi_cef(workbook.add_sheet('cef'))
        self._write_multi_emx(workbook.add_sheet('emx'))
        self._write_multi_pei(workbook.add_sheet('pei'))
        self._write_multi_est(workbook.add_sheet('est'))
        self._write_multi_eue(workbook.add_sheet('eue'))
        self._write_multi_pti(workbook.add_sheet('pti'))
        self._write_multi_yoe(workbook.add_sheet('yoe'))
        self._write_multi_yct(workbook.add_sheet('yct'))
        self._write_multi_rts(workbook.add_sheet('rts'))
        workbook.save(save_file_name)
    def _write_multi_cef(self, sheet):
        '''
        write multi cef
        '''
        self._write_column(sheet, 0, ['Province']+self.province_names)
        self._write_column(sheet, 1, ['2007'] + [item *100 for item
                                                 in self.mpaam_2006_2007.cef()])
        self._write_column(sheet, 2, ['2008'] + [item *100 for item
                                                 in self.mpaam_2006_2008.cef()])                                     
        self._write_column(sheet, 3, ['2009'] + [item *100 for item
                                                 in self.mpaam_2006_2009.cef()])                                       
        self._write_column(sheet, 4, ['2010'] + [item *100 for item
                                                 in self.mpaam_2006_2010.cef()])                                     
        self._write_column(sheet, 5, ['2011'] + [item *100 for item
                                                 in self.mpaam_2006_2011.cef()])                                     
        self._write_column(sheet, 6, ['2012'] + [item *100 for item
                                                 in self.mpaam_2006_2012.cef()])                                       
        self._write_column(sheet, 7, ['2013'] + [item *100 for item
                                                 in self.mpaam_2006_2013.cef()])                                   
        self._write_column(sheet, 8, ['2014'] + [item *100 for item
                                                 in self.mpaam_2006_2014.cef()])
    def _write_multi_emx(self, sheet):
        '''
        write multi emx
        '''
        self._write_column(sheet, 0, ['Province']+self.province_names)
        self._write_column(sheet, 1, ['2007'] + [item *100 for item
                                                 in self.mpaam_2006_2007.emx()])
        self._write_column(sheet, 2, ['2008'] + [item *100 for item
                                                 in self.mpaam_2006_2008.emx()])
        self._write_column(sheet, 3, ['2009'] + [item *100 for item
                                                 in self.mpaam_2006_2009.emx()])
        self._write_column(sheet, 4, ['2010'] + [item *100 for item
                                                 in self.mpaam_2006_2010.emx()])
        self._write_column(sheet, 5, ['2011'] + [item *100 for item
                                                 in self.mpaam_2006_2011.emx()])
        self._write_column(sheet, 6, ['2012'] + [item *100 for item
                                                 in self.mpaam_2006_2012.emx()])
        self._write_column(sheet, 7, ['2013'] + [item *100 for item
                                                 in self.mpaam_2006_2013.emx()])
        self._write_column(sheet, 8, ['2014'] + [item *100 for item
                                                 in self.mpaam_2006_2014.emx()])
    def _write_multi_pei(self, sheet):
        '''
        write multi emx
        '''
        self._write_column(sheet, 0, ['Province']+self.province_names)
        self._write_column(sheet, 1, ['2007'] + [item *100 for item
                                                 in self.mpaam_2006_2007.pei()])
        self._write_column(sheet, 2, ['2008'] + [item *100 for item
                                                 in self.mpaam_2006_2008.pei()])
        self._write_column(sheet, 3, ['2009'] + [item *100 for item
                                                 in self.mpaam_2006_2009.pei()])
        self._write_column(sheet, 4, ['2010'] + [item *100 for item
                                                 in self.mpaam_2006_2010.pei()])
        self._write_column(sheet, 5, ['2011'] + [item *100 for item
                                                 in self.mpaam_2006_2011.pei()])
        self._write_column(sheet, 6, ['2012'] + [item *100 for item
                                                 in self.mpaam_2006_2012.pei()])
        self._write_column(sheet, 7, ['2013'] + [item *100 for item
                                                 in self.mpaam_2006_2013.pei()])
        self._write_column(sheet, 8, ['2014'] + [item *100 for item
                                                 in self.mpaam_2006_2014.pei()])
    def _write_multi_pti(self, sheet):
        '''
        write multi emx
        '''
        self._write_column(sheet, 0, ['Province']+self.province_names)
        self._write_column(sheet, 1, ['2007'] + [item *100 for item
                                                 in self.mpaam_2006_2007.pti()])
        self._write_column(sheet, 2, ['2008'] + [item *100 for item
                                                 in self.mpaam_2006_2008.pti()])
        self._write_column(sheet, 3, ['2009'] + [item *100 for item
                                                 in self.mpaam_2006_2009.pti()])
        self._write_column(sheet, 4, ['2010'] + [item *100 for item
                                                 in self.mpaam_2006_2010.pti()])
        self._write_column(sheet, 5, ['2011'] + [item *100 for item
                                                 in self.mpaam_2006_2011.pti()])
        self._write_column(sheet, 6, ['2012'] + [item *100 for item
                                                 in self.mpaam_2006_2012.pti()])
        self._write_column(sheet, 7, ['2013'] + [item *100 for item
                                                 in self.mpaam_2006_2013.pti()])
        self._write_column(sheet, 8, ['2014'] + [item *100 for item
                                                 in self.mpaam_2006_2014.pti()])
    def _write_multi_rts(self, sheet):
        '''
        write multi emx
        '''
        self._write_column(sheet, 0, ['Province']+self.province_names)
        self._write_column(sheet, 1, ['2007'] + [item *100 for item
                                                 in self.mpaam_2006_2007.rts()])
        self._write_column(sheet, 2, ['2008'] + [item *100 for item
                                                 in self.mpaam_2006_2008.rts()])
        self._write_column(sheet, 3, ['2009'] + [item *100 for item
                                                 in self.mpaam_2006_2009.rts()])
        self._write_column(sheet, 4, ['2010'] + [item *100 for item
                                                 in self.mpaam_2006_2010.rts()])
        self._write_column(sheet, 5, ['2011'] + [item *100 for item
                                                 in self.mpaam_2006_2011.rts()])
        self._write_column(sheet, 6, ['2012'] + [item *100 for item
                                                 in self.mpaam_2006_2012.rts()])
        self._write_column(sheet, 7, ['2013'] + [item *100 for item
                                                 in self.mpaam_2006_2013.rts()])
        self._write_column(sheet, 8, ['2014'] + [item *100 for item
                                                 in self.mpaam_2006_2014.rts()])
    def _write_multi_eue(self, sheet):
        '''
        write multi emx
        '''
        self._write_column(sheet, 0, ['Province']+self.province_names)
        self._write_column(sheet, 1, ['2007'] + [item *100 for item
                                                 in self.mpaam_2006_2007.eue()])
        self._write_column(sheet, 2, ['2008'] + [item *100 for item
                                                 in self.mpaam_2006_2008.eue()])
        self._write_column(sheet, 3, ['2009'] + [item *100 for item
                                                 in self.mpaam_2006_2009.eue()])
        self._write_column(sheet, 4, ['2010'] + [item *100 for item
                                                 in self.mpaam_2006_2010.eue()])
        self._write_column(sheet, 5, ['2011'] + [item *100 for item
                                                 in self.mpaam_2006_2011.eue()])
        self._write_column(sheet, 6, ['2012'] + [item *100 for item
                                                 in self.mpaam_2006_2012.eue()])
        self._write_column(sheet, 7, ['2013'] + [item *100 for item
                                                 in self.mpaam_2006_2013.eue()])
        self._write_column(sheet, 8, ['2014'] + [item *100 for item
                                                 in self.mpaam_2006_2014.eue()])
    def _write_multi_est(self, sheet):
        '''
        write multi emx
        '''
        self._write_column(sheet, 0, ['Province']+self.province_names)
        self._write_column(sheet, 1, ['2007'] + [item *100 for item
                                                 in self.mpaam_2006_2007.est()])
        self._write_column(sheet, 2, ['2008'] + [item *100 for item
                                                 in self.mpaam_2006_2008.est()])
        self._write_column(sheet, 3, ['2009'] + [item *100 for item
                                                 in self.mpaam_2006_2009.est()])
        self._write_column(sheet, 4, ['2010'] + [item *100 for item
                                                 in self.mpaam_2006_2010.est()])
        self._write_column(sheet, 5, ['2011'] + [item *100 for item
                                                 in self.mpaam_2006_2011.est()])
        self._write_column(sheet, 6, ['2012'] + [item *100 for item
                                                 in self.mpaam_2006_2012.est()])
        self._write_column(sheet, 7, ['2013'] + [item *100 for item
                                                 in self.mpaam_2006_2013.est()])
        self._write_column(sheet, 8, ['2014'] + [item *100 for item
                                                 in self.mpaam_2006_2014.est()])
    def _write_multi_yoe(self, sheet):
        '''
        write multi emx
        '''
        self._write_column(sheet, 0, ['Province']+self.province_names)
        self._write_column(sheet, 1, ['2007'] + [item *100 for item
                                                 in self.mpaam_2006_2007.yoe()])
        self._write_column(sheet, 2, ['2008'] + [item *100 for item
                                                 in self.mpaam_2006_2008.yoe()])
        self._write_column(sheet, 3, ['2009'] + [item *100 for item
                                                 in self.mpaam_2006_2009.yoe()])
        self._write_column(sheet, 4, ['2010'] + [item *100 for item
                                                 in self.mpaam_2006_2010.yoe()])
        self._write_column(sheet, 5, ['2011'] + [item *100 for item
                                                 in self.mpaam_2006_2011.yoe()])
        self._write_column(sheet, 6, ['2012'] + [item *100 for item
                                                 in self.mpaam_2006_2012.yoe()])
        self._write_column(sheet, 7, ['2013'] + [item *100 for item
                                                 in self.mpaam_2006_2013.yoe()])
        self._write_column(sheet, 8, ['2014'] + [item *100 for item
                                                 in self.mpaam_2006_2014.yoe()])
    def _write_multi_yct(self, sheet):
        '''
        write multi emx
        '''
        self._write_column(sheet, 0, ['Province']+self.province_names)
        self._write_column(sheet, 1, ['2007'] + [item *100 for item
                                                 in self.mpaam_2006_2007.yct()])
        self._write_column(sheet, 2, ['2008'] + [item *100 for item
                                                 in self.mpaam_2006_2008.yct()])
        self._write_column(sheet, 3, ['2009'] + [item *100 for item
                                                 in self.mpaam_2006_2009.yct()])
        self._write_column(sheet, 4, ['2010'] + [item *100 for item
                                                 in self.mpaam_2006_2010.yct()])
        self._write_column(sheet, 5, ['2011'] + [item *100 for item
                                                 in self.mpaam_2006_2011.yct()])
        self._write_column(sheet, 6, ['2012'] + [item *100 for item
                                                 in self.mpaam_2006_2012.yct()])
        self._write_column(sheet, 7, ['2013'] + [item *100 for item
                                                 in self.mpaam_2006_2013.yct()])
        self._write_column(sheet, 8, ['2014'] + [item *100 for item
                                                 in self.mpaam_2006_2014.yct()])
if __name__ == '__main__':
    app = AppLmdi()
    '''
    workbook = Workbook(encoding='utf8')
    app.write_lmdi_single(workbook.add_sheet('单期LMDI'))
    app.write_lmdi_multi(workbook.add_sheet('跨期LMDI'))
    workbook.save('out/LMDI单期和跨期.xls'
    '''
    app.write_multi_lmdi('out/省份lmdi明细.xls')
    app.write_single_attribution('out/单期归因.xls')
    app.write_multi_attribution('out/跨期归因.xls')                                               