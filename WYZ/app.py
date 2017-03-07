# -*- coding:utf8 -*-
from algorithm import theta_min, eta_max, lambda_min
from config import SHEET_2005, SHEET_2010
from read_xls import read_dmus
import xlwt

def calc_theta_min():
    dmus_2005 = read_dmus(SHEET_2005)
    dmus_2010 = read_dmus(SHEET_2010)
    return theta_min([dmus_2005,], dmus_2010)
def calc_eta_max():
    dmus_2005 = read_dmus(SHEET_2005)
    dmus_2010 = read_dmus(SHEET_2010)
    return eta_max([dmus_2005,], dmus_2005)
def calc_lambda_min():
    dmus_2005 = read_dmus(SHEET_2005)
    dmus_2010 = read_dmus(SHEET_2010)
    return lambda_min([dmus_2005,], dmus_2010)


def write_result():
    dmus_2005 = read_dmus(SHEET_2005)
    dmus_2010 = read_dmus(SHEET_2010)
    province_names = [dmu.name for dmu in dmus_2005]
    theta_0_0 = theta_min([dmus_2005,], dmus_2005)
    theta_0_T = theta_min([dmus_2005,], dmus_2010)
    theta_T_0 = theta_min([dmus_2010,], dmus_2005)
    theta_T_T = theta_min([dmus_2010,], dmus_2010)
    eta_0_0 = eta_max([dmus_2005,], dmus_2005)
    eta_0_T = eta_max([dmus_2005,], dmus_2010)
    eta_T_0 = eta_max([dmus_2010,], dmus_2005)
    eta_T_T = eta_max([dmus_2010,], dmus_2010)
    lambda_0_0 = lambda_min([dmus_2005,], dmus_2005)
    lambda_0_T = lambda_min([dmus_2005,], dmus_2010)
    lambda_T_0 = lambda_min([dmus_2010,], dmus_2005)
    lambda_T_T = lambda_min([dmus_2010,], dmus_2010)
    workbook = xlwt.Workbook(encoding='utf-8')
    sheet = workbook.add_sheet('2007-2008')
    _write_column(sheet, 0, ['省份']+province_names)
    _write_column(sheet, 1, ['theta_0_0']+theta_0_0)
    _write_column(sheet, 2, ['theta_0_T']+theta_0_T)
    _write_column(sheet, 3, ['theta_T_0']+theta_T_0)
    _write_column(sheet, 4, ['theta_T_T']+theta_T_T)
    _write_column(sheet, 5, ['eta_0_0']+eta_0_0)
    _write_column(sheet, 6, ['eta_0_T']+eta_0_T)
    _write_column(sheet, 7, ['eta_T_0']+eta_T_0)
    _write_column(sheet, 8, ['eta_T_T']+eta_T_T)
    _write_column(sheet, 9, ['lambda_0_0']+lambda_0_0)
    _write_column(sheet, 10, ['lambda_0_T']+lambda_0_T)
    _write_column(sheet, 11, ['lambda_T_0']+lambda_T_0)
    _write_column(sheet, 12, ['lambda_T_T']+lambda_T_T)
    workbook.save('result3-test.xls')
def _write_column(sheet, column, values):
    '''
    write a column
    '''
    row = 0
    for value in values:
        sheet.write(row, column, label=value)
        row += 1
if __name__ == '__main__':
    write_result()