# -*- coding:utf8 -*-
'''
single peroid
'''
from __future__ import division
from math import sqrt, exp
from Model import *
from LMDI import Lmdi
from config import CEF_DIC

class Spaam(object):
    '''
    single peroid attribution analysis class
    '''
    cache = {}
    @classmethod
    def build(cls, dmus_t, dmus_t1, name='', global_dmus=None):
        '''
        build a single period attribution
        '''
        if not Spaam.cache.has_key(name):
            Spaam.cache[name] = Spaam(dmus_t, dmus_t1, name, global_dmus)
        return Spaam.cache[name]
    def __init__(self, dmus_t, dmus_t1, name='', global_dmus=None):
        self._dmus_t = dmus_t
        self._dmus_t1 = dmus_t1
        self._name = name
        self._format()
        self._cache = {}
        self._lmdi = Lmdi.build(self._dmus_t, self._dmus_t1, self._name, global_dmus)
    def _format(self):
        '''
        format the data
        '''
        self._province_count = len(self._dmus_t)
        self._energy_count = len(self._dmus_t[0].energy)
        t_year = self._name.split('-')[0]
        t1_year = self._name.split('-')[1]
        self._cef_t = CEF_DIC[t_year]
        self._cef_t1 = CEF_DIC[t1_year]
        magic_number = 0.00001
        for i in range(self._province_count):
            if self._dmus_t[i].energy[-2] == 0.0:
                self._dmus_t[i].energy[-2] = magic_number
                self._dmus_t[i].co2[-2] = magic_number*self._cef_t1[i, self._energy_count-2]
            if self._dmus_t1[i].energy[-2] == 0.0:
                self._dmus_t1[i].energy[-2] = magic_number
                self._dmus_t1[i].co2[-2] = magic_number* self._cef_t[i, self._energy_count-2]

    @property
    def name(self):
        '''
        the name
        '''
        return self._name
    @property
    def province_names(self):
        '''
        the province names
        '''
        return self._lmdi.province_names
    
    def _wi(self, idx):
        '''
        wi factor
        '''
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
        '''
        ci
        '''
        return self._lmdi.ci()
    #emx
    @property
    def emx(self):
        '''
        the emx value
        '''
        if not self._cache.has_key('emx'):
            self._cache['emx'] = exp(sum(list(self._lmdi.emx())))
        return self._cache['emx']
    def _peiij(self, i, j):
        dmu_t = self._dmus_t[i]
        dmu_t1 = self._dmus_t1[i]
        if dmu_t.co2[j] != 0.0  and dmu_t1.co2[j] != 0.0:
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
                    *(l_upper / l_low) * (sij_t1 - sij_t)
        elif dmu_t.co2[j] != 0.0 and dmu_t1.co2[j] == 0.0:
            cij_t = dmu_t.co2[j] / self._lmdi.co2_sum_t
            return -1.0 * (1.0 /self._lmdi.ll) * (1.0 / self._LL) * (cij_t / (emx))
        elif dmu_t.co2[j] == 0.0 and dmu_t1.co2[j] != 0.0:
            cij_t = dmu_t1.co2[j] / self._lmdi.co2_sum_t1
            return (1.0 / self._lmdi.ll) * (1.0 / self._LL) * cij_t
        else:
            return 0.0
    def remx(self):
        '''
        r's emx
        '''
        if not self._cache.has_key('remx'):
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
        '''
        emx ratio
        '''
        if not self._cache.has_key('emxRatio'):
            self._cache['emxRatio'] = [1.0 for _ in range(self._lmdi.province_count)]
        return self._cache['emxRatio']
    @property
    def emx_attributions(self):
        '''
        emx each province attribution
        '''
        if not self._cache.has_key('emx_attributions'):
            self._cache['emx_attributions'] = [k * v for k, v
                                               in zip(self.remx(), self.emx_ratio())]
        return self._cache['emx_attributions']
    #cef
    @property
    def cef(self):
        '''
        the cef value
        '''
        if not self._cache.has_key('cef'):
            self._cache['cef'] = exp(sum(list(self._lmdi.cef())))
        return self._cache['cef']
    def _cef_piij(self, i, j):
        dmu_t = self._dmus_t[i]
        dmu_t1 = self._dmus_t1[i]
        if dmu_t.co2[j] != 0.0  and dmu_t1.co2[j] != 0.0:
            number1 = dmu_t.co2[j] / self._lmdi.co2_sum_t
            number2 = dmu_t1.co2[j] / self._lmdi.co2_sum_t1
            numerator1 = Lmdi.l_function(number1, number2) / self._lmdi.ll
            cef_i_j_t = self._cef_t[i, j]
            cef_i_j_t1 = self._cef_t1[i, j]
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
        if not self._cache.has_key('rcef'):
            result = []
            cef_total = self._cef_pij_total()
            for i in range(self._lmdi.province_count):
                value = 0.0
                for j in range(self._lmdi.energy_count):
                    value += self._cef_piij(i, j) / cef_total * (
                        self._cef_t1[i, j] / self._cef_t[i, j] - 1)
                result.append(value)
            self._cache['rcef'] = result
        return self._cache['rcef']
    def cef_ratio(self):
        if not self._cache.has_key('cef_ratio'):
            self._cache['cef_ratio'] = [1.0 for _ in range(self._lmdi.province_count)]
        return self._cache['cef_ratio']
    @property
    def cef_attributions(self):
        if not self._cache.has_key('cef_attributions'):
            self._cache['cef_attributions'] = [k * v for k, v
                                               in zip(self.rcef(), self.cef_ratio())]
        return self._cache['cef_attributions']
    #pei
    @property
    def pei(self):
        '''
        pei the value
        '''
        if not self._cache.has_key('pei'):
            self._cache['pei'] = exp(sum(list(self._lmdi.pei())))
        return self._cache['pei']
    def _pei_t_t1(self, dmu, idx, is_t=True):
        if is_t:
            return dmu.energy.total / self._lmdi.psi_global_t[idx] / dmu.turn_over.turn_over
        else:
            return dmu.energy.total / self._lmdi.psi_global_t1[idx] / dmu.turn_over.turn_over
    def rpei(self):
        '''
        r pei
        '''
        if not self._cache.has_key('rpei'):
            result = []
            for idx, dmu_t_t1 in enumerate(zip(self._dmus_t, self._dmus_t1)):
                __wi = self._wi(idx)
                pei_t = self._pei_t_t1(dmu_t_t1[0], idx)
                pei_t1 = self._pei_t_t1(dmu_t_t1[1], idx, False)
                pii = __wi / Lmdi.l_function(pei_t1, pei_t*self.pei)
                result.append(pii * pei_t)
            total = sum(result)
            self._cache['rpei'] = [item/total for item in result]
        return self._cache['rpei']
    def pei_ratio(self):
        '''
        yct ratio
        '''
        if not self._cache.has_key('peiRatio'):
            result = []
            for idx, dmu_t_t1 in enumerate(zip(self._dmus_t, self._dmus_t1)):
                pei_t = self._pei_t_t1(dmu_t_t1[0], idx)
                pei_t1 = self._pei_t_t1(dmu_t_t1[1], idx, False)
                result.append(pei_t1 / pei_t - 1)
            self._cache['peiRatio'] = result
        return self._cache['peiRatio']
    @property
    def pei_attributions(self):
        if not self._cache.has_key('pei_contribution'):
            self._cache['pei_contribution'] = [k * v for k, v
                                               in zip(self.rpei(), self.pei_ratio())]
        return self._cache['pei_contribution']
    #est
    @property
    def est(self):
        '''
        est value
        '''
        if not self._cache.has_key('est'):
            self._cache['est'] = exp(sum(list(self._lmdi.est())))
        return self._cache['est']
    
    def _est_t_t1(self, dmu, idx, is_t=True):
        if is_t:
            return self._lmdi.psi_global_t[idx] / self._lmdi.psi_t_t[idx]
        else:
            return self._lmdi.psi_global_t1[idx] / self._lmdi.psi_t1_t1[idx]
    def rest(self):
        '''
        rest
        '''
        if not self._cache.has_key('rest'):
            result = []
            for idx, dmu_t_t1 in enumerate(zip(self._dmus_t, self._dmus_t1)):
                __wi = self._wi(idx)
                est_t = self._est_t_t1(dmu_t_t1[0], idx)
                est_t1 = self._est_t_t1(dmu_t_t1[1], idx, False)
                pii = __wi / Lmdi.l_function(est_t1, est_t * self.est)
                result.append(pii * est_t)
            total = sum(result)
            self._cache['rest'] = [item/total for item in result]
        return self._cache['rest']
    def est_ratio(self):
        if not self._cache.has_key('est_ratio'):
            result = []
            for idx, dmu_t_t1 in enumerate(zip(self._dmus_t, self._dmus_t1)):
                est_t = self._est_t_t1(dmu_t_t1[0], idx)
                est_t1 = self._est_t_t1(dmu_t_t1[1], idx, False)
                result.append(est_t1/est_t - 1)
            self._cache['est_ratio'] = result
        return self._cache['est_ratio']   
    @property
    def est_attributions(self):
        if not self._cache.has_key('est_contribution'):
            self._cache['est_contribution'] = [k * v for k, v
                                               in zip(self.rest(), self.est_ratio())]
        return self._cache['est_contribution']
    #eue
    @property
    def eue(self):
        if not self._cache.has_key('eue'):
            self._cache['eue'] = exp(sum(list(self._lmdi.eue())))
        return self._cache['eue']
    def _eue_t_t1(self, dmu, idx, is_t=True):
        if is_t:
            return self._lmdi.psi_t_t[idx]
        else:
            return self._lmdi.psi_t1_t1[idx]
    def reue(self):
        if not self._cache.has_key('reue'):
            result = []
            for idx, dmu_t_t1 in enumerate(zip(self._dmus_t, self._dmus_t1)):
                __wi = self._wi(idx)
                eue_t = self._eue_t_t1(dmu_t_t1[0], idx)
                eue_t1 = self._eue_t_t1(dmu_t_t1[1], idx, False)
                pii = __wi/ Lmdi.l_function(eue_t1, eue_t*self.eue)
                result.append(pii * eue_t)
            total = sum(result)
            self._cache['reue'] = [item/total for item in result]
        return self._cache['reue']
    def eue_ratio(self):
        if not self._cache.has_key('eue_ratio'):
            result = []
            for idx, dmu_t_t1 in enumerate(zip(self._dmus_t, self._dmus_t1)):
                eue_t = self._eue_t_t1(dmu_t_t1[0], idx)
                eue_t1 = self._eue_t_t1(dmu_t_t1[1], idx, False)
                result.append(eue_t1/eue_t - 1)
            self._cache['eue_ratio'] = result
        return self._cache['eue_ratio']
    @property
    def eue_attributions(self):
        return [k*v for k, v in zip(self.reue(), self.eue_ratio())]
    #pti
    @property
    def pti(self):
        if not self._cache.has_key('pti'):
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
        if not self._cache.has_key('rpti'):
            result = []
            for idx, dmu_t_t1 in enumerate(zip(self._dmus_t, self._dmus_t1)):
                __wi = self._wi(idx)
                pti_t = self._pti_t_t1(dmu_t_t1[0], idx)
                pti_t1 = self._pti_t_t1(dmu_t_t1[1], idx, False)
                pii = __wi / Lmdi.l_function(pti_t1, pti_t*self.pti)
                result.append(pii*pti_t)
            total = sum(result)
            self._cache['rpti'] = [item/total for item in result]
        return self._cache['rpti']
    def pti_ratio(self):
        if not self._cache.has_key('pti_ratio'):
            result =[]
            for idx, dmu_t_t1 in enumerate(zip(self._dmus_t, self._dmus_t1)):
                pti_t = self._pti_t_t1(dmu_t_t1[0], idx)
                pti_t1 = self._pti_t_t1(dmu_t_t1[1], idx, False)
                result.append(pti_t1/pti_t - 1)
            self._cache['pti_ratio'] = result
        return self._cache['pti_ratio']
    @property
    def pti_attributions(self):
        return [k*v for k, v in zip(self.rpti(), self.pti_ratio())]
    #yoe
    @property
    def yoe(self):
        if not self._cache.has_key('yoe'):
            self._cache['yoe'] = exp(sum(list(self._lmdi.yoe())))
        return self._cache['yoe']
    def _yoe_t_t1(self, dmu, idx, is_t=True):
        if is_t:
            return 1.0 / self._lmdi.eta_t_t[idx]
        else:
            return 1.0 / self._lmdi.eta_t1_t1[idx]
    def ryoe(self):
        if not self._cache.has_key('ryoe'):
            result = []
            for idx, dmu_t_t1 in enumerate(zip(self._dmus_t, self._dmus_t1)):
                __wi = self._wi(idx)
                yoe_t = self._yoe_t_t1(dmu_t_t1[0], idx)
                yoe_t1 = self._yoe_t_t1(dmu_t_t1[1], idx, False)
                pii = __wi / Lmdi.l_function(yoe_t1, yoe_t*self.yoe)
                result.append(pii*yoe_t)
            total = sum(result)
            self._cache['ryoe'] = [item/total for item in result]
        return self._cache['ryoe']
    def yoe_ratio(self):
        if not self._cache.has_key('yoe_ratio'):
            result = []
            for idx, dmu_t_t1 in enumerate(zip(self._dmus_t, self._dmus_t1)):
                yoe_t = self._yoe_t_t1(dmu_t_t1[0], idx)
                yoe_t1 = self._yoe_t_t1(dmu_t_t1[1], idx, False)
                result.append(yoe_t1/yoe_t - 1)
            self._cache['yoe_ratio'] = result
        return self._cache['yoe_ratio']
    @property
    def yoe_attributions(self):
        return [k*v for k, v in zip(self.yoe_ratio(), self.ryoe())]
    #yct
    @property
    def yct(self):
        if not self._cache.has_key('yct'):
            self._cache['yct'] = exp(sum(list(self._lmdi.yct())))
        return self._cache['yct']
    def _yct_t_t1(self, dmu, idx, is_t=True):
        if is_t:
            return self._lmdi.eta_t_t[idx] / self._lmdi.eta_global_t[idx]
        else:
            return self._lmdi.eta_t1_t1[idx] / self._lmdi.eta_global_t1[idx]
    def ryct(self):
        if not self._cache.has_key('ryct'):
            result = []
            for idx, dmu_t_t1 in enumerate(zip(self._dmus_t, self._dmus_t1)):
                __wi = self._wi(idx)
                yct_t = self._yct_t_t1(dmu_t_t1[0], idx)
                yct_t1 = self._yct_t_t1(dmu_t_t1[1], idx, False)
                pii = __wi / Lmdi.l_function(yct_t1, yct_t*self.yct)
                result.append(pii*yct_t)
            total = sum(result)
            self._cache['ryct'] = [item/total for item in result]
        return self._cache['ryct']
    def yct_ratio(self):
        if not self._cache.has_key('yct_ratio'):
            result = []
            for idx, dmu_t_t1 in enumerate(zip(self._dmus_t, self._dmus_t1)):
                yct_t = self._yct_t_t1(dmu_t_t1[0], idx)
                yct_t1 = self._yct_t_t1(dmu_t_t1[1], idx, False)
                result.append(yct_t1/yct_t - 1)
            self._cache['yct_ratio'] = result
        return self._cache['yct_ratio']
    @property
    def yct_attributions(self):
        return [k*v for k, v in zip(self.ryct(), self.yct_ratio())]
    #rts
    @property
    def rts(self):
        if not self._cache.has_key('rts'):
            self._cache['rts'] = exp(sum(list(self._lmdi.rts())))
        return self._cache['rts']
    def _rts_t_t1(self, dmu, idx, is_t=True):
        if is_t:
            return dmu.production.production / self._lmdi.pro_sum_t
        else:
            return dmu.production.production / self._lmdi.pro_sum_t1
    def rrts(self):
        if not self._cache.has_key('rrts'):
            result = []
            for idx, dmu_t_t1 in enumerate(zip(self._dmus_t, self._dmus_t1)):
                __wi = self._wi(idx)
                rts_t = self._rts_t_t1(dmu_t_t1[0], idx)
                rts_t1 = self._rts_t_t1(dmu_t_t1[1], idx, False)
                pii = __wi / Lmdi.l_function(rts_t1, rts_t*self.rts)
                result.append(pii*rts_t)
            total = sum(result)
            self._cache['rrts'] = [item/total for item in result]
        return self._cache['rrts']
    def rts_ratio(self):
        if not self._cache.has_key('rts_ratio'):
            result = []
            for idx, dmu_t_t1 in enumerate(zip(self._dmus_t, self._dmus_t1)):
                rst_t = self._rts_t_t1(dmu_t_t1[0], idx)
                rst_t1 = self._rts_t_t1(dmu_t_t1[1], idx, False)
                result.append(rst_t1/rst_t - 1)
            self._cache['rts_ratio'] = result
        return self._cache['rts_ratio']
    @property
    def rts_attributions(self):
        '''
        rts contributon
        '''
        return [k*v for k, v in zip(self.rrts(), self.rts_ratio())]

    @property
    def indexes(self):
        '''
        指数
        '''
        return [self.cef, self.emx, self.pei,
                self.est, self.eue, self.pti,
                self.yoe, self.yct, self.rts]