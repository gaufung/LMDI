# -*- coding:utf8 -*-
# single period attribute analysis classmethod
from __future__ import division
import logging
import operator
from math import log, sqrt, exp
from Model import *
from LMDI import Lmdi
class Spaam(object):
    '''
    Single peroid attribution analysis method
    '''
    def __init__(self, dmus_t, dmus_t1):
        '''
        the construction of the single period attribute
        analysis method
        Args:
            dmus_t : the t period of Decsion Making Units
            dmus_t1 : the t+1 period of Decsion making units
        '''
        assert len(dmus_t) == len(dmus_t1)
        self._dmus_t = dmus_t
        self._dmus_t1 = dmus_t1
        self._cache = {}
        self._lmdi = Lmdi(self._dmus_t, self._dmus_t1)
    def _wi(self, idx):
        '''
        wi factor
        '''
        result = 0.0
        dmu_t = self._dmus_t[idx]
        dmu_t1 = self._dmus_t1[idx]
        for j in range(self._lmdi.energy_count):
            if dmu_t.co2[j] != 0.0 and dmu_t1.co2[j] != 0.0:
                number1 = dmu_t.co2[j] / self._lmdi.co2_t
                number2 = dmu_t1.co2[j] / self._lmdi.co2_t1
                result += Lmdi.l_function(number1, number2)
        return result / self._lmdi.ll_sum
    # pei
    def _pei_t_t1(self, dmu, idx, is_t=True):
        if is_t:
            return (dmu.ene.total / dmu.pro.production) / \
                    sqrt(self._lmdi.lambda_t_t[idx] * self._lmdi.lambda_t1_t[idx])
        else:
            return (dmu.ene.total / dmu.pro.production) / \
                    sqrt(self._lmdi.lambda_t1_t1[idx] * self._lmdi.lambda_t_t1[idx])
    def rpei(self):
        '''
        r's pei
        '''
        if not self._cache.has_key('rpei'):
            result = []
            __pei = exp(sum(list(self._lmdi.pei())))
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
    @property
    def pei(self):
        '''
        the pei value
        '''
        return exp(sum(list(self._lmdi.pei())))
    #pis
    def _pis_t_t1(self, dmu, idx, is_t=True):
        if is_t:
            return dmu.pro.production * sqrt(self._lmdi.theta_t_t[idx] *
                                             self._lmdi.theta_t1_t[idx]) / self._lmdi.y_t
        else:
            return dmu.pro.production * sqrt(self._lmdi.theta_t1_t1[idx] *
                                             self._lmdi.theta_t_t1[idx]) / self._lmdi.y_t1
    def rpis(self):
        '''
        r's pis
        '''
        if not self._cache.has_key('rpis'):
            result = []
            __pis = exp(sum(list(self._lmdi.pis())))
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
    @property
    def pis(self):
        return exp(sum(list(self._lmdi.pis())))
    #isg
    def _isg_t_t1(self, dmu, idx, is_t=True):
        if is_t:
            return self._lmdi.y_t / self._lmdi.pro_t
        else:
            return self._lmdi.y_t1 / self._lmdi.pro_t1
    def risg(self):
        '''
        r's isg
        '''
        if not self._cache.has_key('risg'):
            result = []
            for idx, _ in enumerate(zip(self._dmus_t, self._dmus_t1)):
                __wi = self._wi(idx)
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
    @property
    def isg(self):
        '''
        the isg value
        '''
        return exp(sum(list(self._lmdi.isg())))
    #eue
    def _eue_t_t1(self, dmu, idx, is_t=True):
        if is_t:
            return self._lmdi.lambda_t_t[idx]
        else:
            return self._lmdi.lambda_t1_t1[idx]
    def reue(self):
        '''
        r's eue
        '''
        if not self._cache.has_key('reue'):
            result = []
            __eue = exp(sum(list(self._lmdi.eue())))
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
    @property
    def eue(self):
        '''
        the eue value
        '''
        return exp(sum(list(self._lmdi.eue())))
    # est
    def _est_t_t1(self, dmu, idx, is_t=True):
        if is_t:
            return sqrt(self._lmdi.lambda_t1_t[idx] / self._lmdi.lambda_t_t[idx])
        else:
            return sqrt(self._lmdi.lambda_t_t1[idx] / self._lmdi.lambda_t1_t1[idx])
    def rest(self):
        '''
        r's est
        '''
        if not self._cache.has_key('rest'):
            result = []
            __est = exp(sum(list(self._lmdi.est())))
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
    @property
    def est(self):
        '''
        the est value
        '''
        return exp(sum(list(self._lmdi.est())))
    #yoe
    def _yoe_t_t1(self, dmu, idx, is_t=True):
        if is_t:
            return 1.0 / self._lmdi.theta_t_t[idx]
        else:
            return 1.0 / self._lmdi.theta_t1_t1[idx]
    def ryoe(self):
        '''
        r's yoe
        '''
        if not self._cache.has_key('ryoe'):
            result = []
            __yoe = exp(sum(list(self._lmdi.yoe())))
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
    @property
    def yoe(self):
        '''
        the yoe value
        '''
        return exp(sum(list(self._lmdi.yoe())))
    # yct
    def _yct_t_t1(self, dmu, idx, is_t=True):
        if is_t:
            return sqrt(self._lmdi.theta_t_t[idx] / self._lmdi.theta_t1_t[idx])
        else:
            return sqrt(self._lmdi.theta_t1_t1[idx] / self._lmdi.theta_t_t1[idx])
    def ryct(self):
        '''
        r yct
        '''
        if not self._cache.has_key('ryct'):
            result = []
            __yct = exp(sum(list(self._lmdi.yct())))
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
    @property
    def yct(self):
        '''
        the yct value
        '''
        return exp(sum(list(self._lmdi.yct())))
     #emx
    def _peiij(self, i, j):
        dmu_t = self._dmus_t[i]
        dmu_t1 = self._dmus_t1[i]
        if dmu_t.co2[j] != 0.0  and dmu_t1.co2[j] != 0.0:
            sij_t = dmu_t.ene[j] / dmu_t.ene.total
            sij_t1 = dmu_t1.ene[j] / dmu_t1.ene.total
            __l = Lmdi.l_function(sij_t1, sij_t * exp(sum(list(self._lmdi.emx()))))
            __L = Lmdi.l_function(dmu_t1.co2[j] / self._lmdi.co2_t1, dmu_t.co2[j] / self._lmdi.co2_t)
            return __L * sij_t / self._lmdi.ll_sum / __l
        elif dmu_t.co2[j] != 0.0 and dmu_t1.co2[j] == 0.0:
            cijt = dmu_t.co2[j] / self._lmdi.co2_t
            return cijt / self._lmdi.ll_sum / exp(sum(list(self._lmdi.emx())))
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
            sij_t = dmu_t.ene[j] / dmu_t.ene.total
            sij_t1 = dmu_t1.ene[j] / dmu_t1.ene.total
            l_upper = Lmdi.l_function(dmu_t1.co2[j] /
                                      self._lmdi.co2_t1, dmu_t.co2[j] / self._lmdi.co2_t)
            l_low = Lmdi.l_function(sij_t1, sij_t * emx)
            return (1.0 / self._LL) * (1.0 / self._lmdi.ll_sum) \
                    *(l_upper / l_low) * (sij_t1 - sij_t)
        elif dmu_t.co2[j] != 0.0 and dmu_t1.co2[j] == 0.0:
            cij_t = dmu_t.co2[j] / self._lmdi.co2_t
            return -1.0 * (1.0 /self._lmdi.ll_sum) * (1.0 / self._LL) * (cij_t / (emx))
        elif dmu_t.co2[j] == 0.0 and dmu_t1.co2[j] != 0.0:
            cij_t = dmu_t1.co2[j] / self._lmdi.co2_t1
            return (1.0 / self._lmdi.ll_sum) * (1.0 / self._LL) * cij_t
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
    def emx(self):
        '''
        the emx value
        '''
        return exp(sum(list(self._lmdi.emx())))
