# -*- coding:utf8 -*-
from __future__ import unicode_literals
import sys, os
import numpy as np
import xlrd
pwd = sys.path[0]    # 获取当前执行脚本的位置
os.path.abspath(os.path.join(pwd, os.pardir,'Data'))

# data file path
XLSX_PATH = os.path.abspath(os.path.join(pwd, os.pardir,
                                         'Data', 'transport.xlsx'))
CO2_FILE_PATH = os.path.abspath(os.path.join(pwd, os.pardir,
                                             'Data', 'co2_coefficient.xls'))
# sheet1 and sheet2 column
# sheet1 is turnover
# sheet2 is production
COL_PROVINCE = 0
COL_2006 = 1
COL_2007 = 2
COL_2008 = 3
COL_2009 = 4
COL_2010 = 5
COL_2011 = 6
COL_2012 = 7
COL_2013 = 8
COL_2014 = 9

#SHEET 
TURNOVER_SHEET = 0
PRODUCTION_SHEET = 1

#ROW START AND END
TRUNOVER_PRO_ROW_START = 1
TURNOVER_PRO_ROW_END = 30

# sheet 3 and sheet11 
# each year's energy and co2
SHEET_2006 = 2
SHEET_2007 = 3
SHEET_2008 = 4
SHEET_2009 = 5
SHEET_2010 = 6
SHEET_2011 = 7
SHEET_2012 = 8
SHEET_2013 = 9
SHEET_2014 = 10


#energy consumpation row number range
ENERGY_START = 41
ENERGY_END = 70

#CO2 EMISSION ROW NUMBER RANGE
CO2_START = 73
CO2_END = 102

# columns number of individual enery consumption and co2 emission
COL_START = 1
COL_END = 13

DMUS_2006_DATA = (COL_2006, SHEET_2006)
DMUS_2007_DATA = (COL_2007, SHEET_2007)
DMUS_2008_DATA = (COL_2008, SHEET_2008)
DMUS_2009_DATA = (COL_2009, SHEET_2009)
DMUS_2010_DATA = (COL_2010, SHEET_2010)
DMUS_2011_DATA = (COL_2011, SHEET_2011)
DMUS_2012_DATA = (COL_2012, SHEET_2012)
DMUS_2013_DATA = (COL_2013, SHEET_2013)
DMUS_2014_DATA = (COL_2014, SHEET_2014)


'''
标准煤炭转换系数
二氧化碳转换系数
能源序号
'''
STATND_COAL_COEFFICIENT = {
    u'原煤' : 0.7143,
    u'洗精煤' : 0.900,
    u'其他洗煤' : 0.2857,
    u'型煤' : 0.5000,
    u'焦炭' : 0.9714,
    u'焦炉煤气' : 5.714,
    u'其他煤气' : 5.571,
    u'原油' : 1.4286,
    u'汽油' : 1.4714,
    u'煤油' : 1.4714,
    u'柴油' : 1.4571,
    u'燃料油' : 1.4286,
    u'液化石油气' : 1.7143,
    u'炼厂干气' : 1.5714,
    u'天然气' : 13.30,
    u'热力' : 0.0341,
    u'电力' : 1.2290
}

CO2_COEFFICIENT = {
    u'原煤' : 1.9779,
    u'洗精煤' : 2.4921424,
    u'其他洗煤' : 0.79114,
    u'型煤' : 2.03853,
    u'焦炭' : 0.3043,
    u'焦炉煤气' : 7.426,
    u'其他煤气' : 17.450,
    u'原油' : 3.0651,
    u'汽油' : 3.0149,
    u'煤油' : 3.0795,
    u'柴油' : 3.1605,
    u'燃料油' : 3.2366,
    u'液化石油气' : 3.1663,
    u'炼厂干气' : 2.6495,
    u'天然气' : 18.086
}
ENERGY_TYPE_INDEX = {
    u'原煤' : 0,
    u'洗精煤' : 1,
    u'其他洗煤' : 2,
    u'型煤' : 3,
    u'焦炭' : 4,
    u'汽油' : 5,
    u'煤油' : 6,
    u'柴油' : 7,
    u'燃料油' : 8,
    u'液化石油气' : 9,
    u'天然气' : 10,
}
CEF = {}
for k, v in ENERGY_TYPE_INDEX.iteritems():
    CEF[v] = CO2_COEFFICIENT[k] / STATND_COAL_COEFFICIENT[k]


_row_start = 1
_row_end = 30
_total_province = 30
def _read_sheet(sheet):
    data = []
    for row in range(_row_start, _row_end+1):
        values = map(float, sheet.row_values(row)[1:3])
        value1 = values[0] / STATND_COAL_COEFFICIENT[u'热力']
        value2 = values[1] / STATND_COAL_COEFFICIENT[u'电力']
        data.append([value1, value2])
    return np.array(data)
_cef_other = []
for i in range(_total_province):
    row = []
    for j in range(11):
        row.append(CEF[j])
    _cef_other.append(row)
_cef = np.array(_cef_other)

_workbook = xlrd.open_workbook(CO2_FILE_PATH)
CEF_DIC = {}
CEF_DIC['2006'] = np.hstack((_cef, _read_sheet(_workbook.sheets()[0])))
CEF_DIC['2007'] = np.hstack((_cef, _read_sheet(_workbook.sheets()[1])))
CEF_DIC['2008'] = np.hstack((_cef, _read_sheet(_workbook.sheets()[2])))
CEF_DIC['2009'] = np.hstack((_cef, _read_sheet(_workbook.sheets()[3])))
CEF_DIC['2010'] = np.hstack((_cef, _read_sheet(_workbook.sheets()[4])))
CEF_DIC['2011'] = np.hstack((_cef, _read_sheet(_workbook.sheets()[5])))
CEF_DIC['2012'] = np.hstack((_cef, _read_sheet(_workbook.sheets()[6])))
CEF_DIC['2013'] = np.hstack((_cef, _read_sheet(_workbook.sheets()[7])))
CEF_DIC['2014'] = np.hstack((_cef, _read_sheet(_workbook.sheets()[8])))

