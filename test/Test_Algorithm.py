# -*- coding:utf8 -*-
import sys
sys.path.append('..')

from PDA_Transport.config import DMUS_2006_DATA, DMUS_2007_DATA,DMUS_2008_DATA,DMUS_2009_DATA
from PDA_Transport.config import DMUS_2010_DATA, DMUS_2011_DATA, DMUS_2012_DATA, DMUS_2013_DATA, DMUS_2014_DATA
from PDA_Transport.Algorithm import psi_min, eta_max
from PDA_Transport.Data_Read import read_dmus

def check_pis_min():
    dmus_2006 = read_dmus(DMUS_2006_DATA)
    dmus_2007 = read_dmus(DMUS_2007_DATA)
    dmus_2008 = read_dmus(DMUS_2008_DATA)
    dmus_2009 = read_dmus(DMUS_2009_DATA)
    dmus_2010 = read_dmus(DMUS_2010_DATA)
    dmus_2011 = read_dmus(DMUS_2011_DATA)
    dmus_2012 = read_dmus(DMUS_2012_DATA)
    dmus_2013 = read_dmus(DMUS_2013_DATA)
    dmus_2014 = read_dmus(DMUS_2014_DATA)
    print psi_min([dmus_2006,dmus_2007,dmus_2008, dmus_2009, dmus_2010
                   ,dmus_2011, dmus_2012, dmus_2013, dmus_2014], dmus_2014)

def check_eta_max():
    dmus_2006 = read_dmus(DMUS_2006_DATA)
    dmus_2007 = read_dmus(DMUS_2007_DATA)
    dmus_2008 = read_dmus(DMUS_2008_DATA)
    dmus_2009 = read_dmus(DMUS_2009_DATA)
    dmus_2010 = read_dmus(DMUS_2010_DATA)
    dmus_2011 = read_dmus(DMUS_2011_DATA)
    dmus_2012 = read_dmus(DMUS_2012_DATA)
    dmus_2013 = read_dmus(DMUS_2013_DATA)
    dmus_2014 = read_dmus(DMUS_2014_DATA)
    print eta_max([dmus_2006,dmus_2007,dmus_2008, dmus_2009, dmus_2010
                   ,dmus_2011, dmus_2012, dmus_2013, dmus_2014], dmus_2007)

if __name__ == '__main__':
    check_eta_max()