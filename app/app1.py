# -*- coding:utf8 -*-

xls_file_path = '/Users/gaufung/Desktop/LMDA/Data/data3.xlsx'
row_start = 1
row_end = 31
import sys
sys.path.append('..')
import xlrd
import xlwt
from PDA.Model import *
from PDA.Algorithm import linear_program

def format_dmu(row):
    name = row[0]
    ene = [float(row[1]), float(row[1])]
    prodcution = float(row[2])
    co2 = [float(row[3]), float(row[3])]
    return Dmu(Energy(name, ene),
               Production(name, prodcution),
               Co2(name, co2))
def read_dmus(sheet):
    dmus = []
    workbook = xlrd.open_workbook(xls_file_path)
    table = workbook.sheets()[sheet]
    for idx in range(row_start, row_end):
        row = table.row_values(idx)
        dmus.append(format_dmu(row))
    return dmus
def format_dmu1(row):
    print row
    name = row[7]
    ene1 = [float(row[0]), float(row[0])]
    ene2 = [float(row[4]), float(row[4])]
    pro1 = float(row[1])
    pro2 = float(row[5])
    co21 = [float(row[2]), float(row[2])]
    co22 = [float(row[6]), float(row[6])]
    return Dmu(Energy(name,ene1), Production(name, pro1), Co2(name,co21)), \
           Dmu(Energy(name,ene2), Production(name, pro2), Co2(name,co22))
def read_dmus1():
    dmus_t = []
    dmus_t1 = []
    workbook = xlrd.open_workbook(xls_file_path)
    table =workbook.sheets()[0]
    for idx in range(1,31):
        dmus = format_dmu1(table.row_values(idx))
        dmus_t.append(dmus[0])
        dmus_t1.append(dmus[1])
    return dmus_t, dmus_t1
def write():
    #dmus_t = read_dmus(0)
    #dmus_t1 = read_dmus(1)
    dmus_t, dmus_t1 = read_dmus1()
    result_t_t = linear_program(dmus_t, dmus_t)
    result_t_t1 = linear_program(dmus_t, dmus_t1)
    result_t1_t = linear_program(dmus_t1, dmus_t)
    result_t1_t1 = linear_program(dmus_t1, dmus_t1)
    workbook = xlwt.Workbook(encoding='utf8')
    sheet = workbook.add_sheet('线性规划')
    sheet.write(0,0,label='nation')
    sheet.write(0,1,label='t-t')
    sheet.write(0,4,label='t-t1')
    sheet.write(0,7,label='t1-t')
    sheet.write(0,10,label='t1-t1')
    sheet.write(1,1,label='alpha')
    sheet.write(1,2,label='beta')
    sheet.write(1,3,label='omega')
    sheet.write(1,4,label='alpha')
    sheet.write(1,5,label='beta')
    sheet.write(1,6,label='omega')
    sheet.write(1,7,label='alpha')
    sheet.write(1,8,label='beta')
    sheet.write(1,9,label='omega')
    sheet.write(1,10,label='alpha')
    sheet.write(1,11,label='beta')
    sheet.write(1,12,label='omega')
    for idx, value in enumerate(zip(dmus_t,result_t_t,result_t_t1,
                                    result_t1_t, result_t1_t1)):
        sheet.write(idx+2, 0, label=value[0].name)
        sheet.write(idx+2, 1, label=value[1][0])
        sheet.write(idx+2, 2, label=value[1][1])
        sheet.write(idx+2, 3, label=value[1][2])     
        sheet.write(idx+2, 4, label=value[2][0])
        sheet.write(idx+2, 5, label=value[2][1])
        sheet.write(idx+2, 6, label=value[2][2])       
        sheet.write(idx+2, 7, label=value[3][0])
        sheet.write(idx+2, 8, label=value[3][1])
        sheet.write(idx+2, 9, label=value[3][2])        
        sheet.write(idx+2, 10, label=value[4][0])
        sheet.write(idx+2, 11, label=value[4][1])
        sheet.write(idx+2, 12, label=value[4][2])        
    workbook.save('lp2.xls')                
if __name__ == '__main__':
    write()