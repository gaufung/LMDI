# -*- coding:utf-8 -*-
'''
the module of read data from xls
'''
import re
import xlrd
from model import Dmu
from config import ROW_START, ROW_END, COLUMN_END, COLUMN_START, XLS_FILE

def read_dmus(year):
    '''
    read t period of dums
    '''
    workbook = xlrd.open_workbook(XLS_FILE)
    sheet = workbook.sheets()[year]
    dmus = list()
    for row_idx in range(ROW_START, ROW_END):
        row = sheet.row_values(row_idx)[COLUMN_START:COLUMN_END+1]
        dmus.append(Dmu(name=_format_province_name(row[0]),
                        energy=float(row[1]),
                        capital=float(row[2]),
                        labour=float(row[3]),
                        production=float(row[4]),
                        co2=float(row[5])))
    return dmus

def _format_province_name(name):
    '''
    remove the tab or space in province name
    such as  新 疆  => 新疆
    '''
    pattern = r'\s+'
    return re.sub(pattern, '', name)
