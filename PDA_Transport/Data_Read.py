# -*- coding:utf8 -*-
'''
read data from xls
'''
from __future__ import unicode_literals
import xlrd
import config
from Model import Co2, Energy, Production, Turnover, Dmu

def _read_turnover(year):
    '''
    the year turnover
    '''
    workbook = xlrd.open_workbook(config.XLSX_PATH)
    table = workbook.sheets()[config.TURNOVER_SHEET]
    province_names = table.col_values(config.COL_PROVINCE)[config.TRUNOVER_PRO_ROW_START
                                                           : config.TURNOVER_PRO_ROW_END+1]
    turnovers = table.col_values(year)[config.TRUNOVER_PRO_ROW_START
                                       : config.TURNOVER_PRO_ROW_END+1]
    result = []
    for turn_over in zip(province_names, turnovers):
        result.append(Turnover(turn_over[0], float(turn_over[1])))
    return result
def _read_production(year):
    '''
    the year production
    '''
    workbook = xlrd.open_workbook(config.XLSX_PATH)
    table = workbook.sheets()[config.PRODUCTION_SHEET]
    province_names = table.col_values(config.COL_PROVINCE)[config.TRUNOVER_PRO_ROW_START
                                                           : config.TURNOVER_PRO_ROW_END+1]
    producitons = table.col_values(year)[config.TRUNOVER_PRO_ROW_START
                                         : config.TURNOVER_PRO_ROW_END+1]
    result = []
    for producion in zip(province_names, producitons):
        result.append(Production(producion[0], float(producion[1])))
    return result

def _read_energy(year):
    '''
    the year enrgys
    '''
    workbook = xlrd.open_workbook(config.XLSX_PATH)
    table = workbook.sheets()[year]
    result = []
    for row_idx in range(config.ENERGY_START, config.ENERGY_END+1):
        row = table.row_values(row_idx)
        name = row[config.COL_PROVINCE]
        energies = [float(x) for x in row[config.COL_START : config.COL_END+1]]
        result.append(Energy(name, energies))
    return result

def _read_co2(year):
    '''
    the year Co2
    '''
    workbook = xlrd.open_workbook(config.XLSX_PATH)
    table = workbook.sheets()[year]
    result = []
    for row_idx in range(config.CO2_START, config.CO2_END+1):
        row = table.row_values(row_idx)
        name = row[config.COL_PROVINCE]
        co2s = [float(x) for x in row[config.COL_START:config.COL_END+1]]
        result.append(Co2(name, co2s))
    return result

def read_dmus(year_data):
    '''
    the year data is like
    DMUS_2006_DATA = (COL_2006, SHEET_2006)
    '''
    turnovers = _read_turnover(year_data[0])
    producions = _read_production(year_data[0])
    energies = _read_energy(year_data[1])
    co2s = _read_co2(year_data[1])
    result = []
    for dmu in zip(energies, producions, co2s, turnovers):
        result.append(Dmu(dmu[0], dmu[1], dmu[2], dmu[3]))
    return result
