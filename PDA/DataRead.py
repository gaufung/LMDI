# -*- coding:utf8 -*-
'''
read data from xls
using xlrd library
'''
import xlrd
from Model import Co2, Energy, Production, Dmu
from GlobalVaribales import PRO_START_ROW, PRO_END_ROW, XLXS_FILE_PATH
from GlobalVaribales import PRODUCTION_SHEET, PROVINCE_COLUMN
from GlobalVaribales import ENE_START_ROW, ENE_END_ROW
from GlobalVaribales import ENE_CO2_START_COLUMN, ENE_CO2_END_COLUMN
from GlobalVaribales import CO2_START_ROW, CO2_END_ROW


def read_produciton(year):
    '''
    read from industry.xlxs Production
    '''
    workbook = xlrd.open_workbook(XLXS_FILE_PATH)
    table = workbook.sheets()[PRODUCTION_SHEET]
    name_column = table.col_values(PROVINCE_COLUMN)
    production_column = table.col_values(year)
    result = []
    for i in range(PRO_START_ROW, PRO_END_ROW + 1):
        name = name_column[i]
        pro = (float(production_column[i]))
        result.append(Production(name, pro))
    return result


def read_energy(year):
    '''
    read from industry.xlxs energy
    '''
    workbook = xlrd.open_workbook(XLXS_FILE_PATH)
    table = workbook.sheets()[year]
    name_column = table.col_values(PROVINCE_COLUMN)
    result = []
    for i in range(ENE_START_ROW, ENE_END_ROW + 1):
        name = name_column[i]
        energy = map(float, table.row_values(
            i)[ENE_CO2_START_COLUMN: ENE_CO2_END_COLUMN + 1])
        result.append(Energy(name, energy))
    return result



def read_co2(year):
    '''
    read co2
    '''
    workbook = xlrd.open_workbook(XLXS_FILE_PATH)
    table = workbook.sheets()[year]
    name_column = table.col_values(PROVINCE_COLUMN)
    result = []
    for i in range(CO2_START_ROW, CO2_END_ROW + 1):
        name = name_column[i]
        co2 = map(float, table.row_values(
            i)[ENE_CO2_START_COLUMN: ENE_CO2_END_COLUMN + 1])
        result.append(Co2(name, co2))
    return result

def read_dmus(pro_col, sheet_year):
    '''
    read particular year
    '''
    pros = read_produciton(pro_col)
    co2s = read_co2(sheet_year)
    enes = read_energy(sheet_year)
    dmus = []
    for idx, _ in enumerate(pros):
        dmus.append(Dmu(enes[idx], pros[idx], co2s[idx]))
    return dmus
