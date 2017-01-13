# -*- coding:utf8 -*-
'''
The LMDI calculator
'''
from __future__ import division
import logging
import operator
from math import log, sqrt, exp
from Algorithm import lambda_min, theta_max


def _write_helper(sheet, row, column, values):
    for value in values:
        sheet.write(row, column, label=value)
        row += 1


class Lmdi(object):
    '''
    The class of Lmdi
    '''
    def __init__(self, dmus_t, dmus_t1):
        '''
        The construction of this class
        Args:
            dmus_t: the t period of Decision Making Units
            dmus_t1: the t+1 period of Decision Making Units
        '''
        assert len(dmus_t) == len(dmus_t1)
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
        self._co2_t = reduce(
            operator.add, [item.co2.total for item in self._dmus_t])
        self._co2_t1 = reduce(
            operator.add, [item.co2.total for item in self._dmus_t1])
        # the t and t1 periods sum of production
        self._pro_t = reduce(
            operator.add, [item.pro.production for item in self._dmus_t])
        self._pro_t1 = reduce(
            operator.add, [item.pro.production for item in self._dmus_t1])
        # the t and t1 periods sum of energy consumption
        self._energy_t = reduce(
            operator.add, [item.ene.total for item in self._dmus_t])
        self._energy_t1 = reduce(
            operator.add, [item.ene.total for item in self._dmus_t1])
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
                    result += Lmdi.l_function(dmu_t1.co2[j] / self.co2_t1,
                                              dmu_t.co2[j] / self.co2_t)
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
    def co2_t(self):
        '''
        t period co2 emission
        '''
        return self._co2_t

    @property
    def co2_t1(self):
        '''
        t+1 period co2 emission
        '''
        return self._co2_t1

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
    def ll_sum(self):
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
    def pro_t(self):
        '''
        the t period production sum
        '''
        return self._pro_t

    @property
    def pro_t1(self):
        '''
        the t+1 period production sum
        '''
        return self._pro_t1

    @property
    def energy_t(self):
        '''
        the t period energy sum
        '''
        return self._energy_t

    @property
    def energy_t1(self):
        '''
        the t+1 period energy sum
        '''
        return self._energy_t1

    @property
    def province_names(self):
        '''
        the provinces' name
        '''
        return self._province_names

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
            number3 = dmu_t1.co2[j] / self.co2_t1
            number4 = dmu_t.co2[j] / self.co2_t
            numberator2 = Lmdi.l_function(number3, number4)
            return numberator1 * numberator2 / self.ll_sum
        elif dmu_t.ene[j] == 0.0 and dmu_t1.ene[j] != 0.0:
            return dmu_t1.co2[j] / (self._co2_t1 * self.ll_sum)
        elif dmu_t.ene[j] != 0.0 and dmu_t1.ene[j] == 0.0:
            return -1.0 * dmu_t.co2[j] / (self.co2_t * self.ll_sum)
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
                sqrt(self.lambda_t1_t1[i] * self.lambda_t_t1[i]) / dmu_t1.pro.production
            number2 = dmu_t.ene.total / \
                sqrt(self.lambda_t1_t[i] *
                     self.lambda_t_t[i]) / dmu_t.pro.production
            numerator1 = log(number1 / number2)
            number3 = dmu_t1.co2[j] / self.co2_t1
            number4 = dmu_t.co2[j] / self.co2_t
            numberator2 = Lmdi.l_function(number3, number4)
            return numerator1 * numberator2 / self.ll_sum
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
            number3 = dmu_t1.co2[j] / self.co2_t1
            number4 = dmu_t.co2[j] / self.co2_t
            numerator2 = Lmdi.l_function(number3, number4)
            return numerator1 * numerator2 / self.ll_sum
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
            number1 = self.y_t1 / self.pro_t1
            number2 = self.y_t / self.pro_t
            numerator1 = log(number1 / number2)
            number3 = dmu_t1.co2[j] / self.co2_t1
            number4 = dmu_t.co2[j] / self.co2_t
            numerator2 = Lmdi.l_function(number3, number4)
            return numerator1 * numerator2 / (self.ll_sum)
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
            number3 = dmu_t1.co2[j] / self.co2_t1
            number4 = dmu_t.co2[j] / self.co2_t
            numerator2 = Lmdi.l_function(number3, number4)
            return numerator1 * numerator2 / (self.ll_sum)
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
            number3 = dmu_t1.co2[j] / self.co2_t1
            number4 = dmu_t.co2[j] / self.co2_t
            numerator2 = Lmdi.l_function(number3, number4)
            return (numerator1 * numerator2) / (self.ll_sum)
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
            number3 = dmu_t1.co2[j] / self.co2_t1
            number4 = dmu_t.co2[j] / self.co2_t
            numerator2 = Lmdi.l_function(number3, number4)
            return numerator1 * numerator2 / (self.ll_sum)
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
            number3 = dmu_t1.co2[j] / self.co2_t1
            number4 = dmu_t.co2[j] / self.co2_t
            numerator2 = Lmdi.l_function(number3, number4)
            return numerator1 * numerator2 / (self.ll_sum)
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
    #wi
    def _wi(self, idx):
        '''
        wi factor
        '''
        result = 0.0
        dmu_t = self._dmus_t[idx]
        dmu_t1 = self._dmus_t1[idx]
        for j in range(self._energy_count):
            if dmu_t.co2[j] != 0.0 and dmu_t1.co2[j] != 0.0:
                number1 = dmu_t.co2[j] / self.co2_t
                number2 = dmu_t1.co2[j] / self.co2_t1
                result += Lmdi.l_function(number1, number2)
        return result / self._ll

    # pei
    def _pei_t_t1(self, dmu, idx, is_t=True):
        if is_t:
            return (dmu.ene.total / dmu.pro.production) / \
                    sqrt(self._lambda_t_t[idx] * self._lambda_t1_t[idx])
        else:
            return (dmu.ene.total / dmu.pro.production) / \
                    sqrt(self._lambda_t1_t1[idx] * self._lambda_t_t1[idx])

    def rpei(self):
        '''
        r's pei
        '''
        if not self._cache.has_key('rpei'):
            result = []
            __pei = exp(sum(list(self.pei())))
            for idx, dmu_t_t1 in enumerate(zip(self._dmus_t, self._dmus_t1)):
                __wi = self._wi(idx)
                pei_t = self._pei_t_t1(dmu_t_t1[0], idx)
                pei_t1 = self._pei_t_t1(dmu_t_t1[1], idx, False)
                pii = __wi / (Lmdi.l_function(pei_t1, pei_t * __pei))
                result.append(pii * pei_t)
            total = sum(result)
            self._cache['rpei'] = [item / total for item in result]
        return self._cache['rpei']

    def pei_ratio(self):
        '''
        pei ratio
        '''
        if not self._cache.has_key('peiRatio'):
            result = []
            for idx, dmu_t_t1 in enumerate(zip(self._dmus_t, self._dmus_t1)):
                pei_t = self._pei_t_t1(dmu_t_t1[0], idx)
                pei_t1 = self._pei_t_t1(dmu_t_t1[1], idx, False)
                result.append(pei_t1 / pei_t - 1)
            self._cache['peiRatio'] = result
        return self._cache['peiRatio']
    #pis
    def _pis_t_t1(self, dmu, idx, is_t=True):
        if is_t:
            return dmu.pro.production * sqrt(self._theta_t_t[idx] *
                                             self._theta_t1_t[idx]) / self._y_t
        else:
            return dmu.pro.production * sqrt(self._theta_t1_t1[idx] *
                                             self._theta_t_t1[idx]) / self._y_t1
    def rpis(self):
        '''
        r's pis
        '''
        if not self._cache.has_key('rpis'):
            result = []
            __pis = exp(sum(list(self.pis())))
            for idx, dmu_t_t1 in enumerate(zip(self._dmus_t, self._dmus_t1)):
                __wi = self._wi(idx)
                pis_t = self._pis_t_t1(dmu_t_t1[0], idx)
                pis_t1 = self._pis_t_t1(dmu_t_t1[1], idx, False)
                pii = __wi / Lmdi.l_function(pis_t1, pis_t * __pis)
                result.append(pii * pis_t)
            total = sum(result)
            self._cache['rpis'] = [item / total for item in result]
        return self._cache['rpis']
    def pis_ratio(self):
        '''
        pis ratio
        '''
        if not self._cache.has_key('pisRatio'):
            result = []
            for idx, dmu_t_t1 in enumerate(zip(self._dmus_t, self._dmus_t1)):
                pis_t = self._pis_t_t1(dmu_t_t1[0], idx)
                pis_t1 = self._pis_t_t1(dmu_t_t1[1], idx, False)
                result.append(pis_t1 / pis_t - 1)
            self._cache['pisRatio'] = result
        return self._cache['pisRatio']
    #isg
    def _isg_t_t1(self, dmu, idx, is_t=True):
        if is_t:
            return self._y_t / self._pro_t
        else:
            return self._y_t1 / self._pro_t1
    def risg(self):
        '''
        r's isg
        '''
        if not self._cache.has_key('risg'):
            result = []
            for idx, _ in enumerate(zip(self._dmus_t, self._dmus_t1)):
                __wi = self._wi(idx)
                #isg_t = self._isg_t_t1(dmu_t_t1[0], idx)
                #isg_t1 = self._isg_t_t1(dmu_t_t1[1], idx, False)
                result.append(__wi)
            total = sum(result)
            self._cache['risg'] = [item / total for item in result]
        return self._cache['risg']
    def isg_ratio(self):
        '''
        isg ratio
        '''
        if not self._cache.has_key('isgRatio'):
            result = []
            for idx, dmu_t_t1 in enumerate(zip(self._dmus_t, self._dmus_t1)):
                isg_t = self._isg_t_t1(dmu_t_t1[0], idx)
                isg_t1 = self._isg_t_t1(dmu_t_t1[1], idx, False)
                result.append(isg_t1 / isg_t - 1)
            self._cache['isgRatio'] = result
        return self._cache['isgRatio']
    #eue
    def _eue_t_t1(self, dmu, idx, is_t=True):
        if is_t:
            return self._lambda_t_t[idx]
        else:
            return self._lambda_t1_t1[idx]
    def reue(self):
        '''
        r's eue
        '''
        if not self._cache.has_key('reue'):
            result = []
            __eue = exp(sum(list(self.eue())))
            for idx, dmu_t_t1 in enumerate(zip(self._dmus_t, self._dmus_t1)):
                __wi = self._wi(idx)
                eue_t = self._eue_t_t1(dmu_t_t1[0], idx)
                eue_t1 = self._eue_t_t1(dmu_t_t1[1], idx, False)
                pii = __wi / Lmdi.l_function(eue_t1, eue_t * __eue)
                result.append(pii * eue_t)
            total = sum(result)
            self._cache['reue'] = [item / total for item in result]
        return self._cache['reue']
    def eue_ratio(self):
        '''
        eue ratio
        '''
        if not self._cache.has_key('eueRatio'):
            result = []
            for idx, dmu_t_t1 in enumerate(zip(self._dmus_t, self._dmus_t1)):
                eue_t = self._eue_t_t1(dmu_t_t1[0], idx)
                eue_t1 = self._eue_t_t1(dmu_t_t1[1], idx, False)
                result.append(eue_t1 / eue_t - 1)
            self._cache['eueRatio'] = result
        return self._cache['eueRatio']
    # est
    def _est_t_t1(self, dmu, idx, is_t=True):
        if is_t:
            return sqrt(self._lambda_t1_t[idx] / self._lambda_t_t[idx])
        else:
            return sqrt(self._lambda_t_t1[idx] / self._lambda_t1_t1[idx])
    def rest(self):
        '''
        r's est
        '''
        if not self._cache.has_key('rest'):
            result = []
            __est = exp(sum(list(self.est())))
            for idx, dmu_t_t1 in enumerate(zip(self._dmus_t, self._dmus_t1)):
                __wi = self._wi(idx)
                est_t = self._est_t_t1(dmu_t_t1[0], idx)
                est_t1 = self._est_t_t1(dmu_t_t1[1], idx, False)
                pii = __wi / Lmdi.l_function(est_t1, est_t * __est)
                result.append(pii * est_t)
            total = sum(result)
            self._cache['rest'] = [item / total for item in result]
        return self._cache['rest']
    def est_ratio(self):
        '''
        est ratio
        '''
        if not self._cache.has_key('estRatio'):
            result = []
            for idx, dmu_t_t1 in enumerate(zip(self._dmus_t, self._dmus_t1)):
                est_t = self._est_t_t1(dmu_t_t1[0], idx)
                est_t1 = self._est_t_t1(dmu_t_t1[1], idx, False)
                result.append(est_t1 / est_t - 1)
            self._cache['estRatio'] = result
        return self._cache['estRatio']
    #yoe
    def _yoe_t_t1(self, dmu, idx, is_t=True):
        if is_t:
            return 1.0 / self._theta_t_t[idx]
        else:
            return 1.0 / self._theta_t1_t1[idx]
    def ryoe(self):
        '''
        r's yoe
        '''
        if not self._cache.has_key('ryoe'):
            result = []
            __yoe = exp(sum(list(self.yoe())))
            for idx, dmu_t_t1 in enumerate(zip(self._dmus_t, self._dmus_t1)):
                __wi = self._wi(idx)
                yoe_t = self._yoe_t_t1(dmu_t_t1[0], idx)
                yoe_t1 = self._yoe_t_t1(dmu_t_t1[1], idx, False)
                pii = __wi / Lmdi.l_function(yoe_t1, yoe_t * __yoe)
                result.append(pii * yoe_t)
            total = sum(result)
            self._cache['ryoe'] = [item / total for item in result]
        return self._cache['ryoe']
    def yoe_ratio(self):
        '''
        yoe ratio
        '''
        if not self._cache.has_key('yoeRatio'):
            result = []
            for idx, dmu_t_t1 in enumerate(zip(self._dmus_t, self._dmus_t1)):
                yoe_t = self._yoe_t_t1(dmu_t_t1[0], idx)
                yoe_t1 = self._yoe_t_t1(dmu_t_t1[1], idx, False)
                result.append(yoe_t1/yoe_t - 1)
            self._cache['yoeRatio'] = result
        return self._cache['yoeRatio']
    # yct
    def _yct_t_t1(self, dmu, idx, is_t=True):
        if is_t:
            return sqrt(self._theta_t_t[idx] / self._theta_t1_t[idx])
        else:
            return sqrt(self._theta_t1_t1[idx] / self._theta_t_t1[idx])
    def ryct(self):
        '''
        r yct
        '''
        if not self._cache.has_key('ryct'):
            result = []
            __yct = exp(sum(list(self.yct())))
            for idx, dmu_t_t1 in enumerate(zip(self._dmus_t, self._dmus_t1)):
                __wi = self._wi(idx)
                yct_t = self._yct_t_t1(dmu_t_t1[0], idx)
                yct_t1 = self._yct_t_t1(dmu_t_t1[1], idx, False)
                pii = __wi / Lmdi.l_function(yct_t1, yct_t * __yct)
                result.append(pii * yct_t)
            total = sum(result)
            self._cache['ryct'] = [item / total for item in result]
        return self._cache['ryct']
    def yct_ratio(self):
        '''
        yct ratio
        '''
        if not self._cache.has_key('yctRatio'):
            result = []
            for idx, dmu_t_t1 in enumerate(zip(self._dmus_t, self._dmus_t1)):
                yct_t = self._yct_t_t1(dmu_t_t1[0], idx)
                yct_t1 = self._yct_t_t1(dmu_t_t1[1], idx, False)
                result.append(yct_t1 / yct_t -1)
            self._cache['yctRatio'] = result
        return self._cache['yctRatio']
    #emx
    def _peiij(self, i, j):
        dmu_t = self._dmus_t[i]
        dmu_t1 = self._dmus_t1[i]
        if dmu_t.co2[j] != 0.0  and dmu_t1.co2[j] != 0.0:
            sij_t = dmu_t.ene[j] / dmu_t.ene.total
            sij_t1 = dmu_t1.ene[j] / dmu_t1.ene.total
            __l = Lmdi.l_function(sij_t1, sij_t * exp(sum(list(self.emx()))))
            __L = Lmdi.l_function(dmu_t1.co2[j] / self._co2_t1, dmu_t.co2[j] / self._co2_t)
            return __L * sij_t / self.ll_sum / __l
        elif dmu_t.co2[j] != 0.0 and dmu_t1.co2[j] == 0.0:
            cijt = dmu_t.co2[j] / self.co2_t
            return cijt / self.ll_sum / exp(sum(list(self.emx())))
        else:
            return 0.0
    def _rij_total(self):
        result = 0.0
        for i in range(self.province_count):
            for j in range(self.energy_count):
                result += self._peiij(i, j)
        return result
    def _rij(self, i, j, emx):
        dmu_t = self._dmus_t[i]
        dmu_t1 = self._dmus_t1[i]
        if dmu_t.co2[j] != 0.0 and dmu_t1.co2[j] != 0.0:
            sij_t = dmu_t.ene[j] / dmu_t.ene.total
            sij_t1 = dmu_t1.ene[j] / dmu_t1.ene.total
            l_upper = Lmdi.l_function(dmu_t1.co2[j] /self._co2_t1, dmu_t.co2[j] / self._co2_t)
            l_low = Lmdi.l_function(sij_t1, sij_t * emx)
            return (1.0 / self._LL) * (1.0 / self._ll) *(l_upper / l_low) * (sij_t1 - sij_t)
        elif dmu_t.co2[j] != 0.0 and dmu_t1.co2[j] == 0.0:
            cij_t = dmu_t.co2[j] / self.co2_t
            return -1.0 * (1.0 /self._ll) * (1.0 / self._LL) * (cij_t / (emx))
        elif dmu_t.co2[j] == 0.0 and dmu_t1.co2[j] != 0.0:
            cij_t = dmu_t1.co2[j] / self.co2_t1
            return (1.0 / self._ll) * (1.0 / self._LL) * cij_t
        else:
            return 0.0
    def remx(self):
        '''
        r's emx
        '''
        if not self._cache.has_key('remx'):
            result = []
            self._LL = self._rij_total()
            __emx = exp(sum(list(self.emx())))
            for i in range(self.province_count):
                value = 0.0
                for j in range(self.energy_count):
                    value += self._rij(i, j, __emx)
                result.append(value)
            self._cache['remx'] = result
        return self._cache['remx']
    def emx_ratio(self):
        '''
        emx ratio
        '''
        if not self._cache.has_key('emxRatio'):
            self._cache['emxRatio'] = [1.0 for i in range(self.province_count)]
        return self._cache['emxRatio']
    def write(self, workbook, name):

        '''
        write LMDI into one sheet
        '''
        sheet = workbook.add_sheet(name)
        sheet.write(0, 0, label=u'省份')
        sheet.write(0, 1, label='T 期产出')
        sheet.write(0, 2, label='T+1 期产出')
        sheet.write(0, 3, label='T 期能源消耗')
        sheet.write(0, 4, label='T+1 期能源消耗')
        sheet.write(0, 5, label='T 期Co2排放')
        sheet.write(0, 6, label='T+1 期Co2排放')
        for i, dmu_t_t1 in enumerate(zip(self._dmus_t, self._dmus_t1)):
            dmu_t = dmu_t_t1[0]
            dmu_t1 = dmu_t_t1[1]
            sheet.write(i + 1, 0, dmu_t.name)
            sheet.write(i + 1, 1, dmu_t.pro.production)
            sheet.write(i + 1, 2, dmu_t1.pro.production)
            sheet.write(i + 1, 3, dmu_t.ene.total)
            sheet.write(i + 1, 4, dmu_t1.ene.total)
            sheet.write(i + 1, 5, dmu_t.co2.total)
            sheet.write(i + 1, 6, dmu_t1.co2.total)
        sheet.write(0, 7, label=u'lambda_t_t')
        sheet.write(0, 8, label=u'lambda_t_t1')
        sheet.write(0, 9, label=u'lambda_t1_t')
        sheet.write(0, 10, label=u'lambda_t1_t1')
        sheet.write(0, 11, label=u'theta_t_t')
        sheet.write(0, 12, label=u'theta_t_t1')
        sheet.write(0, 13, label=u'theta_t1_t')
        sheet.write(0, 14, label=u'theta_t1_t1')
        for i in range(self._province_count):
            sheet.write(i + 1, 7, label=self._lambda_t_t[i])
            sheet.write(i + 1, 8, label=self._lambda_t_t1[i])
            sheet.write(i + 1, 9, label=self._lambda_t1_t[i])
            sheet.write(i + 1, 10, label=self._lambda_t1_t1[i])
            sheet.write(i + 1, 11, label=self._theta_t_t[i])
            sheet.write(i + 1, 12, label=self._theta_t_t1[i])
            sheet.write(i + 1, 13, label=self._theta_t1_t[i])
            sheet.write(i + 1, 14, label=self._theta_t1_t1[i])
        sheet.write(0, 15, label=u'emx')
        _write_helper(sheet, 1, 15, self.emx())
        sheet.write(0, 16, label=u'pei')
        _write_helper(sheet, 1, 16, self.pei())
        sheet.write(0, 17, label=u'isg')
        _write_helper(sheet, 1, 17, self.isg())
        sheet.write(0, 18, label=u'pis')
        _write_helper(sheet, 1, 18, self.pis())
        sheet.write(0, 19, label=u'eue')
        _write_helper(sheet, 1, 19, self.eue())
        sheet.write(0, 20, label=u'est')
        _write_helper(sheet, 1, 20, self.est())
        sheet.write(0, 21, label=u'yct')
        _write_helper(sheet, 1, 21, self.yct())
        sheet.write(0, 22, label=u'yoe')
        _write_helper(sheet, 1, 22, self.yoe())


    