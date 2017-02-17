# -*- coding:utf8 -*-
from __future__ import unicode_literals
from __future__ import division
import logging
import operator
from math import log, exp
from Algorithm import psi_min, eta_max
from config import CEF_DIC

class Lmdi(object):
    '''
    the lmdi object
    '''
    cache = {}
    @classmethod
    def build(cls, dmus_t, dmus_t1, name='', dmus_global=None):
        '''
        build a lmdi object
        '''
        if not Lmdi.cache.has_key(name):
            Lmdi.cache[name] = Lmdi(dmus_t, dmus_t1, name, dmus_global)
        return Lmdi.cache[name]
    @classmethod
    def l_function(cls, item1, item2):
        '''
        L function $\frac{a - b}{ln(a) - ln(b)}$
        '''
        return (item1 - item2) / (log(item1) - log(item2))
    def __init__(self, dmus_t, dmus_t1, name='', dmus_global=None):
        '''
        The construction of this class
        Args:
            dmus_t: the t peroid of dmus_s
            dmus_t1: the t+1 peroid of dmus
            name: the name for this lmdi,2006-2007,2007-2008
        '''
        assert dmus_global is not None
        self._name = name
        self._dmus_t = dmus_t
        self._dmus_t1 = dmus_t1
        self._dmus_global = dmus_global
        self._init_data()
        self._cache = {}
        self._w_cache = {}
        self._init()
        self._init_ll()
        self._init_linear_programming()
    def _init(self):
        self._province_count = len(self._dmus_t)
        self._energy_count = len(self._dmus_t[0].energy)
        self._province_names = [item.name for item in self._dmus_t]
        self._co2_sum_t = reduce(
            operator.add, [item.co2.total for item in self._dmus_t])
        self._co2_sum_t1 = reduce(
            operator.add, [item.co2.total for item in self._dmus_t1])
        # the t and t1 periods sum of production
        self._pro_sum_t = reduce(
            operator.add, [item.production.production for item in self._dmus_t])
        self._pro_sum_t1 = reduce(
            operator.add, [item.production.production for item in self._dmus_t1])
    def _init_ll(self):
        '''
        calc the ll value
        '''
        result = 0.0
        for dmu_t, dmu_t1 in zip(self._dmus_t, self._dmus_t1):
            for j in range(self.energy_count):
                if dmu_t.co2[j] != 0.0 and dmu_t1.co2[j] != 0.0:
                    result += Lmdi.l_function(dmu_t1.co2[j] / self.co2_sum_t1,
                                              dmu_t.co2[j] / self.co2_sum_t)
                else:
                    logging.info('zero was found: %f or %f' %
                                 (dmu_t1.co2[j], dmu_t.co2[j]))
        self._ll = result
    def _init_linear_programming(self):
        # min
        self._psi_t_t = psi_min([self._dmus_t,], self._dmus_t)
        self._psi_t1_t1 = psi_min([self._dmus_t1,], self._dmus_t1)
        self._psi_global_t = psi_min(self._dmus_global, self._dmus_t)
        self._psi_global_t1 = psi_min(self._dmus_global, self._dmus_t1)
        # max
        self._eta_t_t = eta_max([self._dmus_t, ], self._dmus_t)
        self._eta_t1_t1 = eta_max([self._dmus_t1,], self._dmus_t1)
        self._eta_global_t = eta_max(self._dmus_global, self._dmus_t)
        self._eta_global_t1 = eta_max(self._dmus_global, self._dmus_t1)
    def _init_data(self):
        '''
        change the value into a very small number
        '''
        self._province_count = len(self._dmus_t)
        self._energy_count = len(self._dmus_t[0].energy)
        t_year = self._name.split('-')[0]
        t1_year = self._name.split('-')[1]
        self._t_cef = CEF_DIC[t_year]
        self._t1_cef = CEF_DIC[t1_year]
        magic_number = 0.00001
        for i in range(self._province_count):
            if self._dmus_t[i].energy[-2] == 0.0:
                self._dmus_t[i].energy[-2] = magic_number
                self._dmus_t[i].co2[-2] = magic_number*self._t1_cef[i, self.energy_count-2]
            if self._dmus_t1[i].energy[-2] == 0.0:
                self._dmus_t1[i].energy[-2] = magic_number
                self._dmus_t1[i].co2[-2] = magic_number* self._t1_cef[i, self.energy_count-2]
    @property
    def name(self):
        '''
        the name of this lmdi, such as 206-2007, 2007-2008
        '''
        return self._name
    @property
    def co2_sum_t(self):
        '''
        t period co2 emission
        '''
        return self._co2_sum_t

    @property
    def co2_sum_t1(self):
        '''
        t+1 period co2 emission
        '''
        return self._co2_sum_t1
    @property
    def energy_count(self):
        '''
        the energy count
        '''
        return self._energy_count
    @property
    def province_count(self):
        '''
        province count
        '''
        return self._province_count
    @property
    def province_names(self):
        '''
        the list of province names
        '''
        return self._province_names
    @property
    def ll(self):
        '''
        ll value
        '''
        return self._ll
    @property
    def pro_sum_t(self):
        '''
        the t period production sum
        '''
        return self._pro_sum_t

    @property
    def pro_sum_t1(self):
        '''
        the t+1 period production sum
        '''
        return self._pro_sum_t1
    @property
    def psi_t_t(self):
        return self._psi_t_t
    @property
    def psi_t1_t1(self):
        return self._psi_t1_t1
    @property
    def psi_global_t(self):
        return self._psi_global_t
    @property
    def psi_global_t1(self):
        return self._psi_global_t1
    @property
    def eta_t_t(self):
        return self._eta_t_t
    @property
    def eta_t1_t1(self):
        return self._eta_t1_t1
    @property
    def eta_global_t(self):
        return self._eta_global_t
    @property
    def eta_global_t1(self):
        return self._eta_global_t1

    def _decomposition_index(self, func):
        '''
        the template function of this
        '''
        for idx, t_t1 in enumerate(zip(self._dmus_t, self._dmus_t1)):
            result = 0.0
            for j in range(self.energy_count):
                result += func(t_t1[0], t_t1[1], j, idx)
            yield result
    # calculate the Index
    # cef
    def _cef(self, dmu_t, dmu_t1, j, i):
        number1 = self._t1_cef[i, j]
        number2 = self._t_cef[i, j]
        if number1 == number2:
            return 0.0
        else:
            numberator1 = log(number1 / number2)
            number3 = dmu_t1.co2[j] / self.co2_sum_t1
            number4 = dmu_t.co2[j] / self.co2_sum_t
            numberator2 = Lmdi.l_function(number3, number4)
            return numberator1 * numberator2 / self.ll
    def cef(self):
        '''
        cef factor for every dmu
        '''
        return self._decomposition_index(self._cef)

    # emx
    def _emx(self, dmu_t, dmu_t1, j, i):
        '''
        calc the emx Index
        Args:
            dmu_t: the t period of dmu
            dmut_t1: the t+1 period of dmu
            j: the j-th energy
            i: the i-th of dmu
        Returns:
            the calc value
        '''
        if dmu_t.co2[j] != 0.0 and dmu_t1.co2[j] != 0.0:
            number1 = dmu_t1.energy[j] / dmu_t1.energy.total
            number2 = dmu_t.energy[j] / dmu_t.energy.total
            numberator1 = log(number1 / number2)
            number3 = dmu_t1.co2[j] / self.co2_sum_t1
            number4 = dmu_t.co2[j] / self.co2_sum_t
            numberator2 = Lmdi.l_function(number3, number4)
            return numberator1 * numberator2 / self.ll
        elif dmu_t.co2[j] == 0.0 and dmu_t1.co2[j] != 0.0:
            return dmu_t1.co2[j] / (self._co2_sum_t1 * self.ll)
        elif dmu_t.co2[j] != 0.0 and dmu_t1.co2[j] == 0.0:
            return -1.0 * dmu_t.co2[j] / (self.co2_sum_t * self.ll)
        else:
            logging.info('%s and %s %d are both zero ' %
                         (dmu_t.name, dmu_t1.name, j))
            return 0.0

    def emx(self):
        '''
        emx factor for every dmu
        '''
        return self._decomposition_index(self._emx)
    #pei
    def _pei(self, dmu_t, dmu_t1, j, i):
        '''
        calc the pei Index
        Args:
            dmu_t: the t period of dmu
            dmut_t1: the t+1 period of dmu
            j: the j-th energy
            i: the i-th of dmu
        Returns:
            the calc value
        '''
        if dmu_t.co2[j] != 0.0 and dmu_t1.co2[j] != 0.0:
            number1 = dmu_t1.energy.total / self.psi_global_t1[i] / dmu_t1.turn_over.turn_over
            number2 = dmu_t.energy.total / self.psi_global_t[i] / dmu_t.turn_over.turn_over
            numerator1 = log(number1 / number2)
            number3 = dmu_t1.co2[j] / self.co2_sum_t1
            number4 = dmu_t.co2[j] / self.co2_sum_t
            numberator2 = Lmdi.l_function(number3, number4)
            return numerator1 * numberator2 / self.ll
        else:
            logging.info('%s or %s %d is both zero ' %
                         (dmu_t.name, dmu_t1.name, j))
            return 0.0
    def pei(self):
        '''
        pei factor each dmu
        '''
        return self._decomposition_index(self._pei)
    #est
    def _est(self, dmu_t, dmu_t1, j, i):
        '''
        calc the est Index
        Args:
            dmu_t: the t period of dmu
            dmut_t1: the t+1 period of dmu
            j: the j-th energy
            i: the i-th of dmu
        Returns:
            the calc value
        '''
        if dmu_t.co2[j] != 0.0 and dmu_t1.co2[j] != 0.0:
            number1 = self.psi_global_t1[i] / self.psi_t1_t1[i]
            number2 = self.psi_global_t[i] / self.psi_t_t[i]
            numerator1 = log(number1 / number2)
            number3 = dmu_t1.co2[j] / self.co2_sum_t1
            number4 = dmu_t.co2[j] / self.co2_sum_t
            numerator2 = Lmdi.l_function(number3, number4)
            return (numerator1 * numerator2) / (self.ll)
        else:
            logging.info('%s or %s %d is both zero ' %
                         (dmu_t.name, dmu_t1.name, j))
            return 0.0

    def est(self):
        '''
        est for each dmu
        '''
        return self._decomposition_index(self._est)
    #eue
    def _eue(self, dmu_t, dmu_t1, j, i):
        '''
        calc the eue Index
        Args:
            dmu_t: the t period of dmu
            dmut_t1: the t+1 period of dmu
            j: the j-th energy
            i: the i-th of dmu
        Returns:
            the calc value
        '''
        if dmu_t.co2[j] != 0.0 and dmu_t1.co2[j] != 0.0:
            number1 = self.psi_t1_t1[i]
            number2 = self.psi_t_t[i]
            numerator1 = log(number1 / number2)
            number3 = dmu_t1.co2[j] / self.co2_sum_t1
            number4 = dmu_t.co2[j] / self.co2_sum_t
            numerator2 = Lmdi.l_function(number3, number4)
            return numerator1 * numerator2 / (self.ll)
        else:
            logging.info('%s or %s %d is both zero ' %
                         (dmu_t.name, dmu_t1.name, j))
            return 0.0

    def eue(self):
        '''
        eue factor for each dmu
        '''
        return self._decomposition_index(self._eue)
    # pti
    def _pti(self, dmu_t, dmu_t1, j, i):
        if dmu_t.co2[j] != 0.0 and dmu_t1.co2[j] != 0.0:
            number1 = dmu_t1.turn_over.turn_over / (dmu_t1.production.production /
                                                    self.eta_global_t1[i])
            number2 = dmu_t.turn_over.turn_over / (dmu_t.production.production /
                                                   self.eta_global_t[i])
            numerator1 = log(number1 / number2)
            number3 = dmu_t1.co2[j] / self.co2_sum_t1
            number4 = dmu_t.co2[j] / self.co2_sum_t
            numerator2 = Lmdi.l_function(number3, number4)
            return numerator1 * numerator2 / (self.ll)
        else:
            logging.info('%s or %s %d is both zero ' %
                         (dmu_t.name, dmu_t1.name, j))
            return 0.0
    def pti(self):
        '''
        pti factor for each dmu
        '''
        return self._decomposition_index(self._pti)
    # yoe
    def _yoe(self, dmu_t, dmu_t1, j, i):
        '''
        calc the yoe Index
        Args:
            dmu_t: the t period of dmu
            dmut_t1: the t+1 period of dmu
            j: the j-th energy
            i: the i-th of dmu
        Returns:
            the calc value
        '''
        if dmu_t.co2[j] != 0.0 and dmu_t1.co2[j] != 0.0:
            number1 = 1.0 / self.eta_t1_t1[i]
            number2 = 1.0 / self.eta_t_t[i]
            numerator1 = log(number1 / number2)
            number3 = dmu_t1.co2[j] / self.co2_sum_t1
            number4 = dmu_t.co2[j] / self.co2_sum_t
            numerator2 = Lmdi.l_function(number3, number4)
            return numerator1 * numerator2 / (self.ll)
        else:
            logging.info('%s or %s %d is both zero ' %
                         (dmu_t.name, dmu_t1.name, j))
            return 0.0

    def yoe(self):
        '''
        yoe factor for each dmu
        '''
        return self._decomposition_index(self._yoe)
    # yct 
    def _yct(self, dmu_t, dmu_t1, j, i):
        '''
        calc the yct Index
        Args:
            dmu_t: the t period of dmu
            dmut_t1: the t+1 period of dmu
            j: the j-th energy
            i: the i-th of dmu
        Returns:
            the calc value
        '''
        if dmu_t.co2[j] != 0.0 and dmu_t1.co2[j] != 0.0:
            number1 = self.eta_t1_t1[i] / self.eta_global_t1[i]
            number2 = self.eta_t_t[i] / self.eta_global_t[i]
            numerator1 = log(number1 / number2)
            number3 = dmu_t1.co2[j] / self.co2_sum_t1
            number4 = dmu_t.co2[j] / self.co2_sum_t
            numerator2 = Lmdi.l_function(number3, number4)
            return numerator1 * numerator2 / (self.ll)
        else:
            logging.info('%s or %s %d is both zero ' %
                         (dmu_t.name, dmu_t1.name, j))
            return 0.0
    def yct(self):
        '''
        yct factor for each dmu
        '''
        return self._decomposition_index(self._yct)
    def _rts(self, dmu_t, dmu_t1, j, i):
        '''
        calc the rts Index
        Args:
            dmu_t: the t period of dmu
            dmut_t1: the t+1 period of dmu
            j: the j-th energy
            i: the i-th of dmu
        Returns:
            the calc value
        '''
        if dmu_t.co2[j] != 0.0 and dmu_t1.co2[j] != 0.0:
            number1 = dmu_t1.production.production / self.pro_sum_t1
            number2 = dmu_t.production.production / self.pro_sum_t
            numerator1 = log(number1 / number2)
            number3 = dmu_t1.co2[j] / self.co2_sum_t1
            number4 = dmu_t.co2[j] / self.co2_sum_t
            numerator2 = Lmdi.l_function(number3, number4)
            return numerator1 * numerator2 / (self.ll)
        else:
            logging.info('%s or %s %d is both zero ' %
                         (dmu_t.name, dmu_t1.name, j))
            return 0.0
    def rts(self):
        '''
        rts factor for each dmu
        '''
        return self._decomposition_index(self._rts)
    def index(self):
        '''
        the index list
        '''
        return [exp(sum(list(self.cef()))),
                exp(sum(list(self.emx()))),
                exp(sum(list(self.pei()))),
                exp(sum(list(self.est()))),
                exp(sum(list(self.eue()))),
                exp(sum(list(self.pti()))),
                exp(sum(list(self.yoe()))),
                exp(sum(list(self.yct()))),
                exp(sum(list(self.rts())))
               ]
    # ci
    def ci(self):
        '''
        the total index
        '''
        ci_t = self.co2_sum_t / self.pro_sum_t
        ci_t1 = self.co2_sum_t1 / self.pro_sum_t1
        return ci_t1 / ci_t
