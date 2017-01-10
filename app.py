# -*- coding:utf8 -*-
import DataRead
import xlrd
import GlobalVaribales
import LMDI
import logging
from xlwt import *
# 
logging.basicConfig(level=logging.INFO)
dmus_2006 = DataRead.read_dmus(GlobalVaribales.PRO_2006_COL, GlobalVaribales.SHEET_2006)
dmus_2007 = DataRead.read_dmus(GlobalVaribales.PRO_2007_COL, GlobalVaribales.SHEET_2007)
dmus_2008 = DataRead.read_dmus(GlobalVaribales.PRO_2008_COL, GlobalVaribales.SHEET_2008)
dmus_2009 = DataRead.read_dmus(GlobalVaribales.PRO_2009_COL, GlobalVaribales.SHEET_2009)
dmus_2010 = DataRead.read_dmus(GlobalVaribales.PRO_2010_COL, GlobalVaribales.SHEET_2010)
dmus_2011 = DataRead.read_dmus(GlobalVaribales.PRO_2011_COL, GlobalVaribales.SHEET_2011)
dmus_2012 = DataRead.read_dmus(GlobalVaribales.PRO_2012_COL, GlobalVaribales.SHEET_2012)
dmus_2013 = DataRead.read_dmus(GlobalVaribales.PRO_2013_COL, GlobalVaribales.SHEET_2013)
dmus_2014 = DataRead.read_dmus(GlobalVaribales.PRO_2014_COL, GlobalVaribales.SHEET_2014)
lmdi_2006_2007 = LMDI.Lmdi(dmus_2006, dmus_2007)
lmdi_2007_2008 = LMDI.Lmdi(dmus_2007, dmus_2008)
lmdi_2008_2009 = LMDI.Lmdi(dmus_2008, dmus_2009)
lmdi_2009_2010 = LMDI.Lmdi(dmus_2009, dmus_2010)
lmdi_2010_2011 = LMDI.Lmdi(dmus_2010, dmus_2011)
lmdi_2011_2012 = LMDI.Lmdi(dmus_2011, dmus_2012)
lmdi_2012_2013 = LMDI.Lmdi(dmus_2012, dmus_2013)
lmdi_2013_2014 = LMDI.Lmdi(dmus_2013, dmus_2014)
lmdi_2006_2014 = LMDI.Lmdi(dmus_2006, dmus_2014)
workbook = Workbook(encoding='utf8')
lmdi_2006_2007.write(workbook,'2006-2007')
lmdi_2007_2008.write(workbook,'2007-2008')
lmdi_2008_2009.write(workbook,'2008-2009')
lmdi_2009_2010.write(workbook,'2009-2010')
lmdi_2010_2011.write(workbook,'2010-2011')
lmdi_2011_2012.write(workbook,'2011-2012')
lmdi_2012_2013.write(workbook,'2012-2013')
lmdi_2013_2014.write(workbook,'2013-2014')
lmdi_2006_2014.write(workbook,'2006-2014')
workbook.save('test.xls')