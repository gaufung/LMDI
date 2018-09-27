# -*- encoding:utf-8 -*-
from math import sqrt, exp
from lmdi import Lmdi


class Spaam(object):
    _CACHE = {}

    @classmethod
    def build(cls, dmus_t, dmus_t1, name="", global_dmus=None, cefs=None):
        if name not in Spaam._CACHE:
            Spaam._CACHE[name] = Spaam(dmus_t, dmus_t1, name, global_dmus, cefs)
        return Spaam._CACHE[name]

    def __init__(self, dmus_t, dmus_t1, name, global_dmus, cefs):
        self._dmus_t = dmus_t
        self._dmus_t1 = dmus_t1
        self._cefs = cefs
        self._name = name
        self._format()
        self._cache = {}
        self._lmdi = Lmdi.build(self._dmus_t, self._dmus_t1, self._name, global_dmus, cefs)

    def _format(self):
        self._province_count = len(self._dmus_t)
        self._energy_count = len(self._dmus_t[0].energy)
        year_t = self._name.split('-')[0]
        year_t1 = self._name.split('-')[1]
        self._cef_t = self._cefs[year_t]
        self._cef_t1 = self._cefs[year_t1]
        slat = 0.00001
        for i in range(self._province_count):
            if self._dmus_t[i].energy[-2] == 0.0:
                self._dmus_t[i].energy[-2] = slat
                self._dmus_t[i].co2[-2] = slat * self._cef_t1[i][self._energy_count - 2]
            if self._dmus_t1[i].energy[-2] == 0.0:
                self._dmus_t1[i].energy[-2] = slat
                self._dmus_t1[i].co2[-2] = slat * self._cef_t[i][self._energy_count - 2]

    @property
    def name(self):
        return self._name

    @property
    def province_names(self):
        return self._lmdi.province_names

    def _wi(self, idx):
        result = 0.0
        dmu_t = self._dmus_t[idx]
        dmu_t1 = self._dmus_t1[idx]
        for j in range(self._lmdi.energy_count):
            if dmu_t.co2[j] != 0.0 and dmu_t1.co2[j] != 0.0:
                number1 = dmu_t.co2[j] / self._lmdi.co2_sum_t
                number2 = dmu_t1.co2[j] / self._lmdi.co2_sum_t1
                result += Lmdi.l_function(number1, number2)
        return result / self._lmdi.ll

    @property
    def ci(self):
        return self._lmdi.ci()

    # emx
    @property
    def emx(self):
        if "emx" not in self._cache:
            self._cache['emx'] = exp(sum(list(self._lmdi.emx())))
        return self._cache['emx']

    def _peiij(self, i, j):
        dmu_t = self._dmus_t[i]
        dmu_t1 = self._dmus_t1[i]
        if dmu_t.co2[j] != 0.0 and dmu_t1.co2[j] != 0.0:
            sij_t = dmu_t.energy[j] / dmu_t.energy.total
            sij_t1 = dmu_t1.energy[j] / dmu_t1.energy.total
            __l = Lmdi.l_function(sij_t1, sij_t * exp(sum(list(self._lmdi.emx()))))
            __L = Lmdi.l_function(dmu_t1.co2[j] / self._lmdi.co2_sum_t1,
                                  dmu_t.co2[j] / self._lmdi.co2_sum_t)
            return __L * sij_t / self._lmdi.ll / __l
        elif dmu_t.co2[j] != 0.0 and dmu_t1.co2[j] == 0.0:
            cijt = dmu_t.co2[j] / self._lmdi.co2_sum_t
            return cijt / self._lmdi.ll / exp(sum(list(self._lmdi.emx())))
        else:
            return 0.0

    def _rij_total(self):
        result = 0.0
        for i in range(self._lmdi.province_count):
            for j in range(self._lmdi.energy_count):
                result += self._peiij(i, j)
        return result

    def _rij(self, i, j, emx):
        dmu_t = self._dmus_t[i]
        dmu_t1 = self._dmus_t1[i]
        if dmu_t.co2[j] != 0.0 and dmu_t1.co2[j] != 0.0:
            sij_t = dmu_t.energy[j] / dmu_t.energy.total
            sij_t1 = dmu_t1.energy[j] / dmu_t1.energy.total
            l_upper = Lmdi.l_function(dmu_t1.co2[j] /
                                      self._lmdi.co2_sum_t1, dmu_t.co2[j] / self._lmdi.co2_sum_t)
            l_low = Lmdi.l_function(sij_t1, sij_t * emx)
            return (1.0 / self._LL) * (1.0 / self._lmdi.ll) \
                   * (l_upper / l_low) * (sij_t1 - sij_t)
        elif dmu_t.co2[j] != 0.0 and dmu_t1.co2[j] == 0.0:
            cij_t = dmu_t.co2[j] / self._lmdi.co2_sum_t
            return -1.0 * (1.0 / self._lmdi.ll) * (1.0 / self._LL) * (cij_t / (emx))
        elif dmu_t.co2[j] == 0.0 and dmu_t1.co2[j] != 0.0:
            cij_t = dmu_t1.co2[j] / self._lmdi.co2_sum_t1
            return (1.0 / self._lmdi.ll) * (1.0 / self._LL) * cij_t
        else:
            return 0.0

    def remx(self):
        if "remx" not in self._cache:
            result = []
            self._LL = self._rij_total()
            __emx = exp(sum(list(self._lmdi.emx())))
            for i in range(self._lmdi.province_count):
                value = 0.0
                for j in range(self._lmdi.energy_count):
                    value += self._rij(i, j, __emx)
                result.append(value)
            self._cache['remx'] = result
        return self._cache['remx']

    def emx_ratio(self):
        if "emxRatio" not in self._cache:
            self._cache['emxRatio'] = [1.0 for _ in range(self._lmdi.province_count)]
        return self._cache['emxRatio']

    @property
    def emx_attributions(self):
        if "emx_attributions" not in self._cache:
            self._cache['emx_attributions'] = [k * v for k, v
                                               in zip(self.remx(), self.emx_ratio())]
        return self._cache['emx_attributions']

    # cef
    @property
    def cef(self):
        if "cef" not in self._cache:
            self._cache['cef'] = exp(sum(list(self._lmdi.cef())))
        return self._cache['cef']

    def _cef_piij(self, i, j):
        dmu_t = self._dmus_t[i]
        dmu_t1 = self._dmus_t1[i]
        if dmu_t.co2[j] != 0.0 and dmu_t1.co2[j] != 0.0:
            number1 = dmu_t.co2[j] / self._lmdi.co2_sum_t
            number2 = dmu_t1.co2[j] / self._lmdi.co2_sum_t1
            numerator1 = Lmdi.l_function(number1, number2) / self._lmdi.ll
            cef_i_j_t = self._cef_t[i][j]
            cef_i_j_t1 = self._cef_t1[i][j]
            denumnerator1 = Lmdi.l_function(cef_i_j_t1, cef_i_j_t * self.cef)
            return numerator1 * cef_i_j_t / denumnerator1
        else:
            return 0.0

    def _cef_pij_total(self):
        result = 0.0
        for i in range(self._lmdi.province_count):
            for j in range(self._lmdi.energy_count):
                result += self._cef_piij(i, j)
        return result

    def rcef(self):
        if "rcef" not in self._cache:
            result = []
            cef_total = self._cef_pij_total()
            for i in range(self._lmdi.province_count):
                value = 0.0
                for j in range(self._lmdi.energy_count):
                    value += self._cef_piij(i, j) / cef_total * (
                            self._cef_t1[i][j] / self._cef_t[i][j] - 1)
                result.append(value)
            self._cache['rcef'] = result
        return self._cache['rcef']

    def cef_ratio(self):
        if "cef_ratio" not in self._cache:
            self._cache['cef_ratio'] = [1.0 for _ in range(self._lmdi.province_count)]
        return self._cache['cef_ratio']

    @property
    def cef_attributions(self):
        if "cef_attributions" not in self._cache:
            self._cache['cef_attributions'] = [k * v for k, v
                                               in zip(self.rcef(), self.cef_ratio())]
        return self._cache['cef_attributions']

    # attribution
    def _attribution_r(self, func, index):
        index_key = 'r' + index
        if index_key not in self._cache:
            result = []
            for idx, dmu_t_t1 in enumerate(zip(self._dmus_t, self._dmus_t1)):
                __wi = self._wi(idx)
                value_t = func(dmu_t_t1[0], idx)
                value_t1 = func(dmu_t_t1[1], idx, False)
                pii = __wi / Lmdi.l_function(value_t1, value_t * getattr(self, index))
                result.append(pii * value_t)
            total = sum(result)
            self._cache[index_key] = [item / total for item in result]
        return self._cache[index_key]

    def _attribution_ratio(self, func, index):
        index_key = index + 'ratio'
        if index_key not in self._cache:
            result = []
            for idx, dmu_t_t1 in enumerate(zip(self._dmus_t, self._dmus_t1)):
                value_t = func(dmu_t_t1[0], idx)
                value_t1 = func(dmu_t_t1[1], idx, False)
                result.append(value_t1 / value_t - 1)
            self._cache[index_key] = result
        return self._cache[index_key]

    # pei
    @property
    def pei(self):
        if "pei" not in self._cache:
            self._cache['pei'] = exp(sum(list(self._lmdi.pei())))
        return self._cache['pei']

    def _pei_t_t1(self, dmu, idx, is_t=True):
        if is_t:
            return dmu.energy.total / self._lmdi.psi_global_t[idx] / dmu.turn_over.turn_over
        else:
            return dmu.energy.total / self._lmdi.psi_global_t1[idx] / dmu.turn_over.turn_over

    def rpei(self):
        return self._attribution_r(self._pei_t_t1, 'pei')

    def pei_ratio(self):
        return self._attribution_ratio(self._pei_t_t1, 'pei')

    @property
    def pei_attributions(self):
        if "pei_contribution" not in self._cache:
            self._cache['pei_contribution'] = [k * v for k, v
                                               in zip(self.rpei(), self.pei_ratio())]
        return self._cache['pei_contribution']

    # est
    @property
    def est(self):
        if "est" not in self._cache:
            self._cache['est'] = exp(sum(list(self._lmdi.est())))
        return self._cache['est']

    def _est_t_t1(self, dmu, idx, is_t=True):
        if is_t:
            return self._lmdi.psi_global_t[idx] / self._lmdi.psi_t_t[idx]
        else:
            return self._lmdi.psi_global_t1[idx] / self._lmdi.psi_t1_t1[idx]

    def rest(self):
        return self._attribution_r(self._est_t_t1, 'est')

    def est_ratio(self):
        return self._attribution_ratio(self._est_t_t1, 'est')

    @property
    def est_attributions(self):
        if "est_contribution" not in self._cache:
            self._cache['est_contribution'] = [k * v for k, v
                                               in zip(self.rest(), self.est_ratio())]
        return self._cache['est_contribution']

    # eue
    @property
    def eue(self):
        if "eue" not in self._cache:
            self._cache['eue'] = exp(sum(list(self._lmdi.eue())))
        return self._cache['eue']

    def _eue_t_t1(self, dmu, idx, is_t=True):
        if is_t:
            return self._lmdi.psi_t_t[idx]
        else:
            return self._lmdi.psi_t1_t1[idx]

    def reue(self):
        return self._attribution_r(self._eue_t_t1, 'eue')

    def eue_ratio(self):
        return self._attribution_ratio(self._eue_t_t1, 'eue')

    @property
    def eue_attributions(self):
        return [k * v for k, v in zip(self.reue(), self.eue_ratio())]

    # pti
    @property
    def pti(self):
        if "pti" not in self._cache:
            self._cache['pti'] = exp(sum(list(self._lmdi.pti())))
        return self._cache['pti']

    def _pti_t_t1(self, dmu, idx, is_t=True):
        if is_t:
            return dmu.turn_over.turn_over / (dmu.production.production /
                                              self._lmdi.eta_global_t[idx])
        else:
            return dmu.turn_over.turn_over / (dmu.production.production /
                                              self._lmdi.eta_global_t1[idx])

    def rpti(self):
        return self._attribution_r(self._pti_t_t1, 'pti')

    def pti_ratio(self):
        return self._attribution_ratio(self._pti_t_t1, 'pti')

    @property
    def pti_attributions(self):
        return [k * v for k, v in zip(self.rpti(), self.pti_ratio())]

    # yoe
    @property
    def yoe(self):
        if "yoe" not in self._cache:
            self._cache['yoe'] = exp(sum(list(self._lmdi.yoe())))
        return self._cache['yoe']

    def _yoe_t_t1(self, dmu, idx, is_t=True):
        if is_t:
            return 1.0 / self._lmdi.eta_t_t[idx]
        else:
            return 1.0 / self._lmdi.eta_t1_t1[idx]

    def ryoe(self):
        return self._attribution_r(self._yoe_t_t1, 'yoe')

    def yoe_ratio(self):
        return self._attribution_ratio(self._yoe_t_t1, 'yoe')

    @property
    def yoe_attributions(self):
        return [k * v for k, v in zip(self.yoe_ratio(), self.ryoe())]

    # yct
    @property
    def yct(self):
        if "yct" not in self._cache:
            self._cache['yct'] = exp(sum(list(self._lmdi.yct())))
        return self._cache['yct']

    def _yct_t_t1(self, dmu, idx, is_t=True):
        if is_t:
            return self._lmdi.eta_t_t[idx] / self._lmdi.eta_global_t[idx]
        else:
            return self._lmdi.eta_t1_t1[idx] / self._lmdi.eta_global_t1[idx]

    def ryct(self):
        return self._attribution_r(self._yct_t_t1, 'yct')

    def yct_ratio(self):
        return self._attribution_ratio(self._yct_t_t1, 'yct')

    @property
    def yct_attributions(self):
        return [k * v for k, v in zip(self.ryct(), self.yct_ratio())]

    # rts
    @property
    def rts(self):
        if "rts" not in self._cache:
            self._cache['rts'] = exp(sum(list(self._lmdi.rts())))
        return self._cache['rts']

    def _rts_t_t1(self, dmu, idx, is_t=True):
        if is_t:
            return dmu.production.production / self._lmdi.production_sum_t
        else:
            return dmu.production.production / self._lmdi.production_sum_t1

    def rrts(self):
        return self._attribution_r(self._rts_t_t1, 'rts')

    def rts_ratio(self):
        return self._attribution_ratio(self._rts_t_t1, 'rts')

    @property
    def rts_attributions(self):
        return [k * v for k, v in zip(self.rrts(), self.rts_ratio())]

    @property
    def indexes(self):
        return [self.cef, self.emx, self.pei,
                self.est, self.eue, self.pti,
                self.yoe, self.yct, self.rts]
