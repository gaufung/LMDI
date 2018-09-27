# -*- encoding:utf-8 -*-
import logging
from math import log, exp
from functools import reduce
import operator

from optimization import global_energy_min, global_production_max


class Lmdi(object):
    _CACHE = {}

    @classmethod
    def build(cls, dmus_t, dmus_t1, name="", dmus_global=None, cefs=None):
        if name not in Lmdi._CACHE:
            Lmdi._CACHE[name] = Lmdi(dmus_t, dmus_t1, name, dmus_global, cefs)
        return Lmdi._CACHE[name]

    @classmethod
    def l_function(cls, item1, item2):
        return (item1 - item2) / (log(item1) - log(item2))

    def __init__(self, dmus_t, dmus_t1, name="", dmus_global=None, cefs=None):
        self._name = name
        self._dmus_t = dmus_t
        self._dmus_t1 = dmus_t1
        self._dmus_global = dmus_global
        self._cefs = cefs
        self._initialize()
        self._initialize_data()
        self._initialize_ll()
        self._initialize_linear_programming()
        self._cache = {}
        self._w_cache = {}

    def _initialize(self):
        self._province_count = len(self._dmus_t)
        self._energy_count = len(self._dmus_t[0].energy)
        self._province_names = [item.name for item in self._dmus_t]
        self._co2_sum_t = reduce(operator.add, [item.co2.total for item in self._dmus_t])
        self._co2_sum_t1 = reduce(operator.add, [item.co2.total for item in self._dmus_t1])
        self._production_sum_t = reduce(operator.add, [item.production.production for item in self._dmus_t])
        self._production_sum_t1 = reduce(operator.add, [item.production.production for item in self._dmus_t1])

    def _initialize_ll(self):
        result = 0.0
        for dmu_t, dmu_t1 in zip(self._dmus_t, self._dmus_t1):
            for j in range(self.energy_count):
                if dmu_t.co2[j] != 0.0 and dmu_t1.co2[j] != 0.0:
                    result += Lmdi.l_function(dmu_t1.co2[j] / self.co2_sum_t1,
                                              dmu_t.co2[j] / self.co2_sum_t)
                else:
                    logging.info("%f or %f may be zero",
                                 dmu_t.co2[j], dmu_t1.co2[j])
        self._ll = result

    def _initialize_linear_programming(self):
        # min
        self._psi_t_t = global_energy_min([self._dmus_t, ], *self._dmus_t)
        self._psi_t1_t1 = global_energy_min([self._dmus_t1, ], *self._dmus_t1)
        self._psi_global_t = global_energy_min(self._dmus_global, *self._dmus_t)
        self._psi_global_t1 = global_energy_min(self._dmus_global, *self._dmus_t1)
        # max
        self._eta_t_t = global_production_max([self._dmus_t, ], *self._dmus_t)
        self._eta_t1_t1 = global_production_max([self._dmus_t1, ], *self._dmus_t1)
        self._eta_global_t = global_production_max(self._dmus_global, *self._dmus_t)
        self._eta_global_t1 = global_production_max(self._dmus_global, *self._dmus_t1)

    def _initialize_data(self):
        year_t = self._name.split("-")[0]
        year_t1 = self._name.split("-")[1]
        self._cef_t = self._cefs[year_t]
        self._cef_t1 = self._cefs[year_t1]
        salt = 0.00001
        for i in range(self.province_count):
            if self._dmus_t[i].energy[-2] == 0.0:
                self._dmus_t[i].energy[-2] = salt
                self._dmus_t[i].co2[-2] = salt * (self._cef_t[i][self.energy_count - 2])
            if self._dmus_t1[i].energy[-2] == 0.0:
                self._dmus_t1[i].energy[-2] = salt
                self._dmus_t1[i].co2[-2] = salt * (self._cef_t1[i][self.energy_count - 2])

    @property
    def name(self):
        return self._name

    @property
    def co2_sum_t(self):
        return self._co2_sum_t

    @property
    def co2_sum_t1(self):
        return self._co2_sum_t1

    @property
    def energy_count(self):
        return self._energy_count

    @property
    def province_count(self):
        return self._province_count

    @property
    def province_names(self):
        return self._province_names

    @property
    def ll(self):
        return self._ll

    @property
    def production_sum_t(self):
        return self._production_sum_t

    @property
    def production_sum_t1(self):
        return self._production_sum_t1

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
        for idx, t_t1 in enumerate(zip(self._dmus_t, self._dmus_t1)):
            result = reduce(operator.add, 
                [func(t_t1[0], t_t1[1], j, idx) for j in range(self.energy_count)])
            yield result

    def _cef(self, dmu_t, dmu_t1, j, i):
        number1 = self._cef_t1[i][j]
        number2 = self._cef_t[i][j]
        if number1 == number2:
            return 0.0
        else:
            numberator1 = log(number1 / number2)
            number3 = dmu_t1.co2[j] / self.co2_sum_t1
            number4 = dmu_t.co2[j] / self.co2_sum_t
            numberator2 = Lmdi.l_function(number3, number4)
            return numberator1 * numberator2 / self.ll

    def cef(self):
        return self._decomposition_index(self._cef)

    def _emx(self, dmu_t, dmu_t1, j, i):
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
        return self._decomposition_index(self._emx)

    def _pei(self, dmu_t, dmu_t1, j, i):
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
        return self._decomposition_index(self._pei)

    def _est(self, dmu_t, dmu_t1, j, i):
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
        return self._decomposition_index(self._est)

    def _eue(self, dmu_t, dmu_t1, j, i):
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
        return self._decomposition_index(self._eue)

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
        return self._decomposition_index(self._pti)

    def _yoe(self, dmu_t, dmu_t1, j, i):
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
        return self._decomposition_index(self._yoe)

    def _yct(self, dmu_t, dmu_t1, j, i):
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
        return self._decomposition_index(self._yct)

    def _rts(self, dmu_t, dmu_t1, j, i):
        if dmu_t.co2[j] != 0.0 and dmu_t1.co2[j] != 0.0:
            number1 = dmu_t1.production.production / self.production_sum_t1
            number2 = dmu_t.production.production / self.production_sum_t
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
        return self._decomposition_index(self._rts)

    def index(self):
        return [exp(sum(list(self.cef()))),
                exp(sum(list(self.emx()))),
                exp(sum(list(self.pei()))),
                exp(sum(list(self.est()))),
                exp(sum(list(self.eue()))),
                exp(sum(list(self.pti()))),
                exp(sum(list(self.yoe()))),
                exp(sum(list(self.yct()))),
                exp(sum(list(self.rts()))),
                ]

    def ci(self):
        ci_t = self.co2_sum_t / self.production_sum_t
        ci_t1 = self.co2_sum_t1 / self.production_sum_t1
        return ci_t1 / ci_t
