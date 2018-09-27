import os


class Config(object):

    STAND_COAL_COEFFICIENT = {
        u'原煤': 0.7143,
        u'洗精煤': 0.900,
        u'其他洗煤': 0.2857,
        u'型煤': 0.5000,
        u'焦炭': 0.9714,
        u'焦炉煤气': 5.714,
        u'其他煤气': 5.571,
        u'原油': 1.4286,
        u'汽油': 1.4714,
        u'煤油': 1.4714,
        u'柴油': 1.4571,
        u'燃料油': 1.4286,
        u'液化石油气': 1.7143,
        u'炼厂干气': 1.5714,
        u'天然气': 13.30,
        u'热力': 0.0341,
        u'电力': 1.2290
    }

    CO2_COEFFICIENT = {
        u'原煤': 1.9779,
        u'洗精煤': 2.4921424,
        u'其他洗煤': 0.79114,
        u'型煤': 2.03853,
        u'焦炭': 0.3043,
        u'焦炉煤气': 7.426,
        u'其他煤气': 17.450,
        u'原油': 3.0651,
        u'汽油': 3.0149,
        u'煤油': 3.0795,
        u'柴油': 3.1605,
        u'燃料油': 3.2366,
        u'液化石油气': 3.1663,
        u'炼厂干气': 2.6495,
        u'天然气': 18.086
    }

    ENERGY_TYPE_INDEX = {
        u'原煤': 0,
        u'洗精煤': 1,
        u'其他洗煤': 2,
        u'型煤': 3,
        u'焦炭': 4,
        u'汽油': 5,
        u'煤油': 6,
        u'柴油': 7,
        u'燃料油': 8,
        u'液化石油气': 9,
        u'天然气': 10,
    }

    XLSX_PATH = ""

    HEAT_COEFFICIENT = 0
    ELECTRICITY_COEFFICIENT = 1
    CAPITAL_SHEET = 2
    TURN_OVER_SHEET = 3
    PRODUCTION_SHEET = 4

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

    HEA_ELE_CAP_TURN_PRO_ROW_START = 1
    HEA_ELE_CAP_TURN_PRO_ROW_END = 30

    SHEET_2006 = 5
    SHEET_2007 = 6
    SHEET_2008 = 7
    SHEET_2009 = 8
    SHEET_2010 = 9
    SHEET_2011 = 10
    SHEET_2012 = 11
    SHEET_2013 = 12
    SHEET_2014 = 13

    ENERGY_ROW_START = 41
    ENERGY_ROW_END = 70

    CO2_ROW_START = 73
    CO2_ROW_END = 102

    COL_START = 1
    COL_END = 13


class K1Config(Config):
    XLSX_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "data-1.xlsx")


class K2Config(Config):
    XLSX_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "data-2.xlsx")


class K3Config(Config):
    XLSX_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "data-3.xlsx")
