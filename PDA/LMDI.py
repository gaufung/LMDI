# -*- coding:utf8 -*-
'''
The LMDI calculator
'''
from __future__ import unicode_literals
from __future__ import division
import logging
import operator
from math import log, sqrt, exp
from Algorithm import lambda_min, theta_max
#from config import CEF
from Cef_Read import CEF_DIC

def _write_helper(sheet, row, column, values):
    for value in values:
        sheet.write(row, column, label=value)
        row += 1


class Lmdi(object):
    '''
    The class of Lmdi
    '''

    def __init__(self, dmus_t, dmus_t1, name=''):
        '''
        The construction of this class
        Args:
            dmus_t: the t period of Decision Making Units
            dmus_t1: the t+1 period of Decision Making Units
            name: the name for this lmdi, for example: 2006-2007, 2007-2008
        '''
        assert len(dmus_t) == len(dmus_t1)
        self._name = name
        self._dmus_t = dmus_t
        self._dmus_t1 = dmus_t1
        self._cache = {}
        self._init()
        self._init_ll()
        self._init_linear_programming()
        self._init_y_sum()
        

    def _init(self):
        '''
        initial the variables for processing
        '''
        self._province_count = len(self._dmus_t)
        self._energy_count = len(self._dmus_t[0].ene) - 1
        self._province_names = [item.pro.name for item in self._dmus_t]
        # the t and t1 periods sum of co2 emission
        self._co2_sum_t = reduce(
            operator.add, [item.co2.total for item in self._dmus_t])
        self._co2_sum_t1 = reduce(
            operator.add, [item.co2.total for item in self._dmus_t1])
        # the t and t1 periods sum of production
        self._pro_sum_t = reduce(
            operator.add, [item.pro.production for item in self._dmus_t])
        self._pro_sum_t1 = reduce(
            operator.add, [item.pro.production for item in self._dmus_t1])
        # the t and t1 periods sum of energy consumption
        self._energy_sum_t = reduce(
            operator.add, [item.ene.total for item in self._dmus_t])
        self._energy_sum_t1 = reduce(
            operator.add, [item.ene.total for item in self._dmus_t1])
        t_year = self._name.split('-')[0]
        t1_year = self._name.split('-')[1]
        self._t_cef = CEF_DIC[t_year]
        self._t1_cef = CEF_DIC[t1_year]
    @classmethod
    def l_function(cls, item1, item2):
        '''
        L function $\frac{a - b}{ln(a) - ln(b)}$
        '''
        return (item1 - item2) / (log(item1) - log(item2))

    def _init_ll(self):
        '''
        calc the ll value
        '''
        result = 0.0
        for dmu_t, dmu_t1 in zip(self._dmus_t, self._dmus_t1):
            for j in range(self._energy_count):
                if dmu_t.co2[j] != 0.0 and dmu_t1.co2[j] != 0.0:
                    result += Lmdi.l_function(dmu_t1.co2[j] / self.co2_sum_t1,
                                              dmu_t.co2[j] / self.co2_sum_t)
                else:
                    logging.info('zero was found: %f or %f' %
                                 (dmu_t1.co2[j], dmu_t.co2[j]))
        self._ll = result

    def _init_linear_programming(self):
        '''
        calc the linear programming index
        '''
        self._lambda_t_t = lambda_min([self._dmus_t, ], self._dmus_t)
        self._lambda_t_t1 = lambda_min([self._dmus_t, ], self._dmus_t1)
        self._lambda_t1_t = lambda_min([self._dmus_t1, ], self._dmus_t)
        self._lambda_t1_t1 = lambda_min([self._dmus_t1, ], self._dmus_t1)
        self._theta_t_t = theta_max([self._dmus_t, ], self._dmus_t)
        self._theta_t_t1 = theta_max([self._dmus_t, ], self._dmus_t1)
        self._theta_t1_t = theta_max([self._dmus_t1, ], self._dmus_t)
        self._theta_t1_t1 = theta_max([self._dmus_t1, ], self._dmus_t1)

    def _init_y_sum(self):
        '''
        sum up the y * linear_programming value
        '''
        self._y_t1 = reduce(operator.add, [self._dmus_t1[k].pro.production * sqrt(
            self._theta_t1_t1[k] * self._theta_t_t1[k]) for k in range(self._province_count)])
        self._y_t = reduce(operator.add, [self._dmus_t[k].pro.production * sqrt(
            self._theta_t_t[k] * self._theta_t1_t[k]) for k in range(self._province_count)])

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
    def province_count(self):
        '''
        province count
        '''
        return self._province_count

    @property
    def energy_count(self):
        '''
        energy count
        '''
        return self._energy_count

    @property
    def ll(self):
        '''
        ll value
        '''
        return self._ll

    @property
    def lambda_t_t(self):
        '''
        lambda (t t)
        '''
        return self._lambda_t_t

    @property
    def lambda_t_t1(self):
        '''
        lambda (t, t+1)
        '''
        return self._lambda_t_t1

    @property
    def lambda_t1_t(self):
        '''
        lambda (t+1, t)
        '''
        return self._lambda_t1_t

    @property
    def lambda_t1_t1(self):
        '''
        lambda (t+1, t+1)
        '''
        return self._lambda_t1_t1

    @property
    def theta_t_t(self):
        '''
        theta (t, t)
        '''
        return self._theta_t_t

    @property
    def theta_t_t1(self):
        '''
        theta (t, t+1)
        '''
        return self._theta_t_t1

    @property
    def theta_t1_t(self):
        '''
        theta (t1, t)
        '''
        return self._theta_t1_t

    @property
    def theta_t1_t1(self):
        '''
        theta (t+1, t+1)
        '''
        return self._theta_t1_t1

    @property
    def y_t1(self):
        '''
        the t+1 period y sum
        '''
        return self._y_t1

    @property
    def y_t(self):
        '''
        the t period y sum
        '''
        return self._y_t

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
    def energy_sum_t(self):
        '''
        the t period energy sum
        '''
        return self._energy_sum_t

    @property
    def energy_sum_t1(self):
        '''
        the t+1 period energy sum
        '''
        return self._energy_sum_t1
    @property
    def pro_t(self):
        '''
        the production of each dmu during t period
        '''
        return [dmu.pro.production for dmu in self._dmus_t]
    @property
    def pro_t1(self):
        '''
        the production of each dmu during t+1 period
        '''
        return [dmu.pro.production for dmu in self._dmus_t1]
    @property
    def energy_t(self):
        '''
        the energy of each dmu during t period
        '''
        return [dmu.ene.total for dmu in self._dmus_t]
    @property
    def energy_t1(self):
        '''
        the enery of each dmu during t+1 period
        '''
        return [dmu.ene.total for dmu in self._dmus_t1]
    @property
    def co2_t(self):
        '''
        the co2 emission of each dmu during t period
        '''
        return [dmu.co2.total for dmu in self._dmus_t]
    @property
    def co2_t1(self):
        '''
        the co2 emission of each dmu during t+1 period
        '''
        return [dmu.co2.total for dmu in self._dmus_t1]
    @property
    def province_names(self):
        '''
        the provinces' name
        '''
        return self._province_names
    @property
    def name(self):
        '''
        the name of lmdi
        '''
        return self._name

    def _index(self, name, index_function):
        '''
        the index Value
        Args:
            name: the name of index : 'emx','pis' such on
            f: the special function of index
        Returns:
            the value of index
        '''
        if name not in self._cache:
            result = 0.0
            '''
            for dmu_t, dmu_t1 in zip(self._dmus_t, self._dmus_t1):
                for j in range(self._energy_count):
                    result += index_function(dmu_t, dmu_t1, j)
            result = exp(result)
            '''
            for i in range(self._province_count):
                for j in range(self._energy_count):
                    result += index_function(self._dmus_t[i],
                                             self._dmus_t1[i], j, i)
            self._cache[name] = exp(result)
        return self._cache[name]

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
        if dmu_t.ene[j] != 0.0 and dmu_t1.ene[j] != 0.0:
            number1 = dmu_t1.ene[j] / dmu_t1.ene.total
            number2 = dmu_t.ene[j] / dmu_t.ene.total
            numberator1 = log(number1 / number2)
            number3 = dmu_t1.co2[j] / self.co2_sum_t1
            number4 = dmu_t.co2[j] / self.co2_sum_t
            numberator2 = Lmdi.l_function(number3, number4)
            return numberator1 * numberator2 / self.ll
        elif dmu_t.ene[j] == 0.0 and dmu_t1.ene[j] != 0.0:
            return dmu_t1.co2[j] / (self._co2_sum_t1 * self.ll)
        elif dmu_t.ene[j] != 0.0 and dmu_t1.ene[j] == 0.0:
            return -1.0 * dmu_t.co2[j] / (self.co2_sum_t * self.ll)
        else:
            logging.info('%s and %s %d are both zero ' %
                         (dmu_t.name, dmu_t1.name, j))
            return 0.0

    def emx(self):
        '''
        emx factor for every dmu
        '''
        for idx, t_t1 in enumerate(zip(self._dmus_t, self._dmus_t1)):
            result = 0.0
            for j in range(self.energy_count):
                result += self._emx(t_t1[0], t_t1[1], j, idx)
            yield result

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
        if dmu_t.ene[j] != 0.0 and dmu_t1.ene[j] != 0.0:
            number1 = dmu_t1.ene.total / \
                sqrt(self.lambda_t1_t1[
                     i] * self.lambda_t_t1[i]) / dmu_t1.pro.production
            number2 = dmu_t.ene.total / \
                sqrt(self.lambda_t1_t[i] *
                     self.lambda_t_t[i]) / dmu_t.pro.production
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
        for idx, t_t1 in enumerate(zip(self._dmus_t, self._dmus_t1)):
            result = 0.0
            for j in range(self.energy_count):
                result += self._pei(t_t1[0], t_t1[1], j, idx)
            yield result

    def _pis(self, dmu_t, dmu_t1, j, i):
        '''
        calc the pis Index
        Args:
            dmu_t: the t period of dmu
            dmut_t1: the t+1 period of dmu
            j: the j-th energy
            i: the i-th of dmu
        Returns:
            the calc value
        '''
        if dmu_t.ene[j] != 0.0 and dmu_t1.ene[j] != 0.0:
            number1 = dmu_t1.pro.production * \
                sqrt(self.theta_t1_t1[i] * self.theta_t_t1[i]) / self.y_t1
            number2 = dmu_t.pro.production * \
                sqrt(self.theta_t1_t[i] * self.theta_t_t[i]) / self.y_t
            numerator1 = log(number1 / number2)
            number3 = dmu_t1.co2[j] / self.co2_sum_t1
            number4 = dmu_t.co2[j] / self.co2_sum_t
            numerator2 = Lmdi.l_function(number3, number4)
            return numerator1 * numerator2 / self.ll
        else:
            logging.info('%s or %s %d is both zero ' %
                         (dmu_t.name, dmu_t1.name, j))
            return 0.0

    def pis(self):
        '''
        pis factor for each dmu
        '''
        for idx, t_t1 in enumerate(zip(self._dmus_t, self._dmus_t1)):
            result = 0.0
            for j in range(self.energy_count):
                result += self._pis(t_t1[0], t_t1[1], j, idx)
            yield result

    def _isg(self, dmu_t, dmu_t1, j, i):
        '''
        calc the isg Index
        Args:
            dmu_t: the t period of dmu
            dmut_t1: the t+1 period of dmu
            j: the j-th energy
            i: the i-th of dmu
        Returns:
            the calc value
        '''
        if dmu_t.co2[j] != 0.0 and dmu_t1.co2[j] != 0.0:
            number1 = self.y_t1 / self.pro_sum_t1
            number2 = self.y_t / self.pro_sum_t
            numerator1 = log(number1 / number2)
            number3 = dmu_t1.co2[j] / self.co2_sum_t1
            number4 = dmu_t.co2[j] / self.co2_sum_t
            numerator2 = Lmdi.l_function(number3, number4)
            return numerator1 * numerator2 / (self.ll)
        else:
            logging.info('%s or %s %d is both zero ' %
                         (dmu_t.name, dmu_t1.name, j))
            return 0.0

    def isg(self):
        '''
        isg factor for each dmu
        '''
        for idx, t_t1 in enumerate(zip(self._dmus_t, self._dmus_t1)):
            result = 0.0
            for j in range(self.energy_count):
                result += self._isg(t_t1[0], t_t1[1], j, idx)
            yield result

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
            numerator1 = log(self.lambda_t1_t1[i] / self.lambda_t_t[i])
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
        for idx, t_t1 in enumerate(zip(self._dmus_t, self._dmus_t1)):
            result = 0.0
            for j in range(self.energy_count):
                result += self._eue(t_t1[0], t_t1[1], j, idx)
            yield result

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
            number1 = sqrt(self.lambda_t_t1[i] / self.lambda_t1_t1[i])
            number2 = sqrt(self.lambda_t1_t[i] / self.lambda_t_t[i])
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
        for idx, t_t1 in enumerate(zip(self._dmus_t, self._dmus_t1)):
            result = 0.0
            for j in range(self.energy_count):
                result += self._est(t_t1[0], t_t1[1], j, idx)
            yield result

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
            number1 = 1.0 / self.theta_t1_t1[i]
            number2 = 1.0 / self.theta_t_t[i]
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
        for idx, t_t1 in enumerate(zip(self._dmus_t, self._dmus_t1)):
            result = 0.0
            for j in range(self._energy_count):
                result += self._yoe(t_t1[0], t_t1[1], j, idx)
            yield result

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
            number1 = sqrt(self.theta_t1_t1[i] / self.theta_t_t1[i])
            number2 = sqrt(self.theta_t_t[i] / self.theta_t1_t[i])
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
        for idx, t_t1 in enumerate(zip(self._dmus_t, self._dmus_t1)):
            result = 0.0
            for j in range(self.energy_count):
                result += self._yct(t_t1[0], t_t1[1], j, idx)
            yield result
    def _cef(self, dmu_t, dmu_t1, j, i):
        '''
        calc the cef Index
        Args:
            dmu_t: the t period of dmu
            dmut_t1: the t+1 period of dmu
            j: the j-th energy
            i: the i-th of dmu
        Returns:
            the calc value
        '''
        '''
        if dmu_t.co2[j] != 0.0 and dmu_t1.co2[j] != 0.0:
            number1 = dmu_t1.co2[j] / dmu_t1.ene[j]
            number2 = dmu_t.co2[j] / dmu_t.ene[j]
            numberator1 = log(number1 / number2)
            number3 = dmu_t1.co2[j] / self.co2_sum_t1
            number4 = dmu_t.co2[j] / self.co2_sum_t
            numberator2 = Lmdi.l_function(number3, number4)
            return numberator1 * numberator2 / self.ll
        else:
            logging.info('%s or %s %d is both zero ' %
                         (dmu_t.name, dmu_t1.name, j))
            return 0.0
        
        if CEF.has_key(j):
            return 0.0
        else:
            try:
                number1 = dmu_t1.co2[j] / dmu_t1.ene[j]
                number2 = dmu_t.co2[j] / dmu_t.ene[j]
                numberator1 = log(number1 / number2)
                number3 = dmu_t1.co2[j] / self.co2_sum_t1
                number4 = dmu_t.co2[j] / self.co2_sum_t
                numberator2 = Lmdi.l_function(number3, number4)
                return numberator1 * numberator2 / self.ll
            except ZeroDivisionError:
                print i, j
                return 0.0
        '''
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
        for idx, t_t1 in enumerate(zip(self._dmus_t, self._dmus_t1)):
            result = 0.0
            for j in range(self.energy_count):
                result += self._cef(t_t1[0], t_t1[1], j, idx)
            yield result
    def ci(self):
        ci_t = self.co2_sum_t / self.pro_sum_t
        ci_t1 = self.co2_sum_t1 / self.pro_sum_t1
        return ci_t1 / ci_t