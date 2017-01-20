# -*- coding:utf-8 -*-
# 转换系数
from __future__ import unicode_literals

# -*- coding:utf-8 -*-

'''
global variables
'''
XLXS_FILE_PATH = 'New_Industry.xlsx'
CO2_FILE_PATH = 'co2_coefficient.xls'
PRODUCTION_SHEET = 0
SHEET_2006 = 1
SHEET_2007 = 2
SHEET_2008 = 3
SHEET_2009 = 4
SHEET_2010 = 5
SHEET_2011 = 6
SHEET_2012 = 7
SHEET_2013 = 8
SHEET_2014 = 9

PROVINCE_COLUMN = 0
ENE_CO2_START_COLUMN = 1
ENE_CO2_END_COLUMN = 18
CO2_START_ROW = 2
CO2_END_ROW = 31
ENE_START_ROW = 35
ENE_END_ROW = 64

PRO_START_ROW = 3
PRO_END_ROW = 32

PRO_2006_COL = 1
PRO_2007_COL = 2
PRO_2008_COL = 3
PRO_2009_COL = 4
PRO_2010_COL = 5
PRO_2011_COL = 6
PRO_2012_COL = 7
PRO_2013_COL = 8
PRO_2014_COL = 9


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
    u'焦炉煤气' : 5,
    u'其他煤气' : 6,
    u'原油' : 7,
    u'汽油' : 8,
    u'煤油' : 9,
    u'柴油' : 10,
    u'燃料油' : 11,
    u'液化石油气' : 12,
    u'炼厂干气' : 13,
    u'天然气' : 14,
}
CEF = {}
for k, v in ENERGY_TYPE_INDEX.iteritems():
    CEF[v] = CO2_COEFFICIENT[k] / STATND_COAL_COEFFICIENT[k]
