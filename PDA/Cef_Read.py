# -*- coding:utf8 -*- 
# read co2 to energy factors
from __future__ import division
from __future__ import unicode_literals
from config import *
from GlobalVaribales import CO2_FILE_PATH
import numpy as np
import xlrd
row_start = 1
row_end = 30
total_province = 30
def read_sheet(sheet):
    data = []
    for row in range(row_start, row_end+1):
        values = map(float, sheet.row_values(row)[1:3])
        value1 = values[0] / STATND_COAL_COEFFICIENT[u'热力']
        value2 = values[1] / STATND_COAL_COEFFICIENT[u'电力']
        data.append([value1, value2])
    return np.array(data)
cef_other = []
for i in range(total_province):
    row =[]
    for j in range(15):
        row.append(CEF[j])
    cef_other.append(row)
cef = np.array(cef_other)

workbook = xlrd.open_workbook(CO2_FILE_PATH)
CEF_DIC = {}
CEF_DIC['2006'] = np.hstack((cef, read_sheet(workbook.sheets()[0])))
CEF_DIC['2007'] = np.hstack((cef, read_sheet(workbook.sheets()[1])))
CEF_DIC['2008'] = np.hstack((cef, read_sheet(workbook.sheets()[2])))
CEF_DIC['2009'] = np.hstack((cef, read_sheet(workbook.sheets()[3])))
CEF_DIC['2010'] = np.hstack((cef, read_sheet(workbook.sheets()[4])))
CEF_DIC['2011'] = np.hstack((cef, read_sheet(workbook.sheets()[5])))
CEF_DIC['2012'] = np.hstack((cef, read_sheet(workbook.sheets()[6])))
CEF_DIC['2013'] = np.hstack((cef, read_sheet(workbook.sheets()[7])))
CEF_DIC['2014'] = np.hstack((cef, read_sheet(workbook.sheets()[8])))

