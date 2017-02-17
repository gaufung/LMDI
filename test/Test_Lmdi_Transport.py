#-*- coding:utf8 -*-
import sys
sys.path.append('..')
import unittest
import operator
from PDA_Transport.config import DMUS_2006_DATA, DMUS_2007_DATA,DMUS_2008_DATA,DMUS_2009_DATA
from PDA_Transport.config import DMUS_2010_DATA, DMUS_2011_DATA, DMUS_2012_DATA, DMUS_2013_DATA, DMUS_2014_DATA
from PDA_Transport.Data_Read import read_dmus
from PDA_Transport.LMDI import Lmdi
class Test_Lmdi(unittest.TestCase):
    
    def test_index(self):
        dmus_2006 = read_dmus(DMUS_2006_DATA)
        dmus_2007 = read_dmus(DMUS_2007_DATA)
        dmus_2008 = read_dmus(DMUS_2008_DATA)
        dmus_2009 = read_dmus(DMUS_2009_DATA)
        dmus_2010 = read_dmus(DMUS_2010_DATA)
        dmus_2011 = read_dmus(DMUS_2011_DATA)
        dmus_2012 = read_dmus(DMUS_2012_DATA)
        dmus_2013 = read_dmus(DMUS_2013_DATA)
        dmus_2014 = read_dmus(DMUS_2014_DATA)
        global_dmus = [dmus_2006, dmus_2007, dmus_2008, dmus_2009, dmus_2010,
                       dmus_2011, dmus_2012, dmus_2013, dmus_2014]
        lmdi = Lmdi.build(dmus_2006, dmus_2007, '2006-2007', global_dmus)
        ci_except = reduce(operator.mul, lmdi.index())
        ci_calc = lmdi.ci()
        self.assertAlmostEqual(ci_calc, ci_except)
    '''
    def test_lmdi_multiperiod(self):
        dmus_2006 = read_dmus(DMUS_2006_DATA)
        dmus_2007 = read_dmus(DMUS_2007_DATA)
        dmus_2008 = read_dmus(DMUS_2008_DATA)
        dmus_2009 = read_dmus(DMUS_2009_DATA)
        dmus_2010 = read_dmus(DMUS_2010_DATA)
        dmus_2011 = read_dmus(DMUS_2011_DATA)
        dmus_2012 = read_dmus(DMUS_2012_DATA)
        dmus_2013 = read_dmus(DMUS_2013_DATA)
        dmus_2014 = read_dmus(DMUS_2014_DATA)
        global_dmus = [dmus_2006, dmus_2007, dmus_2008, dmus_2009, dmus_2010,
                       dmus_2011, dmus_2012, dmus_2013, dmus_2014]
        lmdi_2007 = Lmdi.build(dmus_2006, dmus_2007, '2006-2007', global_dmus).index()
        lmdi_2008 = Lmdi.build(dmus_2007, dmus_2008, '2007-2008', global_dmus).index()
        lmdi_2009 = Lmdi.build(dmus_2008, dmus_2009, '2008-2009', global_dmus).index()
        lmdi_2010 = Lmdi.build(dmus_2009, dmus_2010, '2009-2010', global_dmus).index()
        lmdi_2011 = Lmdi.build(dmus_2010, dmus_2011, '2010-2011', global_dmus).index()
        lmdi_2012 = Lmdi.build(dmus_2011, dmus_2012, '2011-2012', global_dmus).index()
        lmdi_2013 = Lmdi.build(dmus_2012, dmus_2013, '2012-2013', global_dmus).index()
        lmdi_2014 = Lmdi.build(dmus_2013, dmus_2014, '2013-2014', global_dmus).index()
        index = 0
        print 'cef', lmdi_2007[index] * lmdi_2008[index] * lmdi_2009[index] * lmdi_2010[index] \
              * lmdi_2011[index] * lmdi_2012[index] * lmdi_2013[index] * lmdi_2014[index]
        index = 1
        print 'emx', lmdi_2007[index] * lmdi_2008[index] * lmdi_2009[index] * lmdi_2010[index] \
              * lmdi_2011[index] * lmdi_2012[index] * lmdi_2013[index] * lmdi_2014[index]
        index = 2
        print 'pei', lmdi_2007[index] * lmdi_2008[index] * lmdi_2009[index] * lmdi_2010[index] \
              * lmdi_2011[index] * lmdi_2012[index] * lmdi_2013[index] * lmdi_2014[index]
        index = 3
        print 'est', lmdi_2007[index] * lmdi_2008[index] * lmdi_2009[index] * lmdi_2010[index] \
              * lmdi_2011[index] * lmdi_2012[index] * lmdi_2013[index] * lmdi_2014[index]
        index = 4
        print 'eue', lmdi_2007[index] * lmdi_2008[index] * lmdi_2009[index] * lmdi_2010[index] \
              * lmdi_2011[index] * lmdi_2012[index] * lmdi_2013[index] * lmdi_2014[index]
        index = 5
        print 'pti', lmdi_2007[index] * lmdi_2008[index] * lmdi_2009[index] * lmdi_2010[index] \
              * lmdi_2011[index] * lmdi_2012[index] * lmdi_2013[index] * lmdi_2014[index]
        index = 6
        print 'yoe', lmdi_2007[index] * lmdi_2008[index] * lmdi_2009[index] * lmdi_2010[index] \
              * lmdi_2011[index] * lmdi_2012[index] * lmdi_2013[index] * lmdi_2014[index]
        index = 7
        print 'yct', lmdi_2007[index] * lmdi_2008[index] * lmdi_2009[index] * lmdi_2010[index] \
              * lmdi_2011[index] * lmdi_2012[index] * lmdi_2013[index] * lmdi_2014[index]
        index = 8
        print 'rts', lmdi_2007[index] * lmdi_2008[index] * lmdi_2009[index] * lmdi_2010[index] \
              * lmdi_2011[index] * lmdi_2012[index] * lmdi_2013[index] * lmdi_2014[index]
      '''
if __name__ == '__main__':
    unittest.main()