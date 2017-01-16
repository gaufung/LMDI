# -*- coding:utf8 -*-
'''
export data
'''

import logging
import xlwt
from LMDI import Lmdi
from SinglePeriodAAM import Spaam
from MultiPeriodAAM import Mpaam
class WriteLmdiData(object):
    '''
    write data using with surrounding
    '''
    def __init__(self, xls_file_name, *lmdis):
        '''
        construction
        Args:
            xls_file_name: to save excel file name
            lmdis: the total lmdis to write
        '''
        self._xls_file_name = xls_file_name
        self._lmdis = lmdis
    def __enter__(self):
        self._workbook = xlwt.Workbook(encoding='utf8')
        return self
    def write(self):
        '''
        write the excel
        '''
        for lmdi in self._lmdis:
            if lmdi.name == '':
                raise Exception(Lmdi.__name__+' should initialize by name. ')
            sheet = self._workbook.add_sheet(lmdi.name)
            self._write_columns_names(sheet)
            self._write_column(sheet, 0, lmdi.province_names)
            self._write_column(sheet, 1, lmdi.pro_t)
            self._write_column(sheet, 2, lmdi.pro_t1)
            self._write_column(sheet, 3, lmdi.energy_t)
            self._write_column(sheet, 4, lmdi.energy_t1)
            self._write_column(sheet, 5, lmdi.co2_t)
            self._write_column(sheet, 6, lmdi.co2_t1)
            self._write_column(sheet, 7, lmdi.lambda_t_t)
            self._write_column(sheet, 8, lmdi.lambda_t_t1)
            self._write_column(sheet, 9, lmdi.lambda_t1_t)
            self._write_column(sheet, 10, lmdi.lambda_t1_t1)
            self._write_column(sheet, 11, lmdi.theta_t_t)
            self._write_column(sheet, 12, lmdi.theta_t_t1)
            self._write_column(sheet, 13, lmdi.theta_t1_t)
            self._write_column(sheet, 14, lmdi.theta_t1_t1)
            self._write_column(sheet, 15, lmdi.emx())
            self._write_column(sheet, 16, lmdi.pei())
            self._write_column(sheet, 17, lmdi.isg())
            self._write_column(sheet, 18, lmdi.pis())
            self._write_column(sheet, 19, lmdi.eue())
            self._write_column(sheet, 20, lmdi.est())
            self._write_column(sheet, 21, lmdi.yct())
            self._write_column(sheet, 22, lmdi.yoe())
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self._workbook.save(self._xls_file_name)
        elif exc_type is Exception:
            logging.error(exc_val)
        else:
            pass
    def _write_columns_names(self, sheet):
        sheet.write(0, 0, label=u'省份')
        sheet.write(0, 1, label=u'T 期产出')
        sheet.write(0, 2, label=u'T+1 期产出')
        sheet.write(0, 3, label=u'T 期能源消耗')
        sheet.write(0, 4, label=u'T+1 期能源消耗')
        sheet.write(0, 5, label=u'T 期Co2排放')
        sheet.write(0, 6, label=u'T+1 期Co2排放')
        sheet.write(0, 7, label=u'lambda_t_t')
        sheet.write(0, 8, label=u'lambda_t_t1')
        sheet.write(0, 9, label=u'lambda_t1_t')
        sheet.write(0, 10, label=u'lambda_t1_t1')
        sheet.write(0, 11, label=u'theta_t_t')
        sheet.write(0, 12, label=u'theta_t_t1')
        sheet.write(0, 13, label=u'theta_t1_t')
        sheet.write(0, 14, label=u'theta_t1_t1')
        sheet.write(0, 15, label=u'emx')
        sheet.write(0, 16, label=u'pei')
        sheet.write(0, 17, label=u'isg')
        sheet.write(0, 18, label=u'pis')
        sheet.write(0, 19, label=u'eue')
        sheet.write(0, 20, label=u'est')
        sheet.write(0, 21, label=u'yct')
        sheet.write(0, 22, label=u'yoe')
    def _write_column(self, sheet, column, values):
        '''
        Args:
            sheet: the sheet
            column: the column to WriteData
            values: the values to write
        '''
        try:
            row = 1
            for value in values:
                sheet.write(row, column, label=value)
                row += 1
        except TypeError:
            logging.error('the type error in '+str(column)+ ' column')
            raise

class WriteSpaamData(object):
    '''
    write the spaam data
    '''
    def __init__(self, xls_file_name, *spaams):
        '''
        construction
        Args:
            xls_file_name: to save excel file name
            spaams: the total spaam to write
        '''
        self._xls_file_name = xls_file_name
        self._spaams = spaams
    def __enter__(self):
        self._workbook = xlwt.Workbook(encoding='utf8')
        return self
    def write(self):
        '''
        write value
        '''
        for spaam in self._spaams:
            if spaam.name == '':
                raise Exception(Spaam.__name__ + ' should be initialized by name')
            sheet = self._workbook.add_sheet(spaam.name)
            self._write_columns_names(sheet)
            self._write_column(sheet, 0, spaam.province_names)
            self._write_column(sheet, 1, spaam.emx_attributions)
            self._write_column(sheet, 2, spaam.pei_attributions)
            self._write_column(sheet, 3, spaam.pis_attributions)
            self._write_column(sheet, 4, spaam.isg_attributions)
            self._write_column(sheet, 5, spaam.eue_attributions)
            self._write_column(sheet, 6, spaam.est_attributions)
            self._write_column(sheet, 7, spaam.yoe_attributions)
            self._write_column(sheet, 8, spaam.yct_attributions)
    def _write_columns_names(self, sheet):
        sheet.write(0, 0, label=u'省份')
        sheet.write(0, 1, label=u'emx')
        sheet.write(0, 2, label=u'pei')
        sheet.write(0, 3, label=u'pis')
        sheet.write(0, 4, label=u'isg')
        sheet.write(0, 5, label=u'eue')
        sheet.write(0, 6, label=u'est')
        sheet.write(0, 7, label=u'yoe')
        sheet.write(0, 8, label=u'yct')
    def _write_column(self, sheet, column, values):
        '''
        write values to a perticular column
        '''
        row = 1
        for value in values:
            sheet.write(row, column, label=value)
            row += 1

    def __exit__(self, exc_type, exc_val, ect_tb):
        if exc_type is None:
            self._workbook.save(self._xls_file_name)
        elif exc_type is Exception:
            logging.error(exc_val)
        else:
            pass

class WriteMpaamData(object):
    '''
    write the mpaam data
    '''
    def __init__(self, xls_file_name, *mpaams):
        '''
        construction
        Args：
            xls_file_name: to save excel file name 
            mpaams: the total mpaam to write
        '''
        self._xls_file_name = xls_file_name
        self._mpaams = mpaams
    def __enter__(self):
        self._workbook = xlwt.Workbook(encoding='utf8')
        return self
    def write(self):
        '''
        write value
        '''
        for mpaam in self._mpaams:
            if mpaam.name == '':
                raise Exception(Mpaam.__name__ + ' should be initialized by name')
            sheet = self._workbook.add_sheet(mpaam.name)
            self._write_columns_names(sheet)
            self._write_column(sheet, 0, mpaam.province_name)
            self._write_column(sheet, 1, mpaam.emx())
            self._write_column(sheet, 2, mpaam.pei())
            self._write_column(sheet, 3, mpaam.pis())
            self._write_column(sheet, 4, mpaam.isg())
            self._write_column(sheet, 5, mpaam.eue())
            self._write_column(sheet, 6, mpaam.est())
            self._write_column(sheet, 7, mpaam.yoe())
            self._write_column(sheet, 8, mpaam.yct())
    def _write_columns_names(self, sheet):
        sheet.write(0, 0, label=u'省份')
        sheet.write(0, 1, label=u'emx')
        sheet.write(0, 2, label=u'pei')
        sheet.write(0, 3, label=u'pis')
        sheet.write(0, 4, label=u'isg')
        sheet.write(0, 5, label=u'eue')
        sheet.write(0, 6, label=u'est')
        sheet.write(0, 7, label=u'yoe')
        sheet.write(0, 8, label=u'yct')
    def _write_column(self, sheet, column, values):
        '''
        write the values to perticualar column
        '''
        row = 1
        for value in values:
            sheet.write(row, column, label=value)
            row += 1
    def __exit__(self, exc_type, exc_val, ect_tb):
        if exc_type is None:
            self._workbook.save(self._xls_file_name)
        elif  exc_type is Exception:
            logging.error(exc_val)
        else:
            pass