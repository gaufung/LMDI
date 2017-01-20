# -*- coding:utf8 -*-
# single period attribute analysis classmethod
'''
1： single-period 对象
2： single-period 工厂对象
'''
from __future__ import division
from math import sqrt, exp
from Model import *
from LMDI import Lmdi, LmdiFactory
from Cef_Read import CEF_DIC


class Spaam(object):
    '''
    Single peroid attribution analysis method
    '''
    def __init__(self, dmus_t, dmus_t1, name=''):
        '''
        the construction of the single period attribute
        analysis method
        Args:
            dmus_t : the t period of Decsion Making Units
            dmus_t1 : the t+1 period of Decsion making units
            name: the name of t and t+1
        '''
        assert len(dmus_t) == len(dmus_t1)
        self._dmus_t = dmus_t
        self._dmus_t1 = dmus_t1
        self._cache = {}
        self._lmdi = LmdiFactory.build(self._dmus_t, self._dmus_t1, name)
        year_t = name.split('-')[0]
        year_t1 = name.split('-')[1]
        self._cef_t = CEF_DIC[year_t]
        self._cef_t1 = CEF_DIC[year_t1]
    @property
    def name(self):
        '''
        the name
        '''
        return self._lmdi.name
    @property
    def province_names(self):
        '''
        the province name
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
        if not self._cache.has_key('pei'):
            self._cache['pei'] = exp(sum(list(self._lmdi.pei())))
        return self._cache['pei']
    @property
    def pei_attributions(self):
        '''
        the pei attributions
        '''
        if not self._cache.has_key('pei_attribition'):
            self._cache['pei_attribition'] = [k * v for k, v in zip(self.rpei(), self.pei_ratio())]
        return self._cache['pei_attribition']
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
        '''
        pis value
        '''
        if not self._cache.has_key('pis'):
            self._cache['pis'] = exp(sum(list(self._lmdi.pis())))
        return self._cache['pis']
    @property
    def pis_attributions(self):
        '''
        pis every province attribution
        '''
        if not self._cache.has_key('pis_attributions'):
            self._cache['pis_attributions'] = [k * v for k, v in zip(self.rpis(), self.pis_ratio())]
        return self._cache['pis_attributions']
    #isg
    def _isg_t_t1(self, dmu, idx, is_t=True):
        if is_t:
            return self._lmdi.y_t / self._lmdi.pro_sum_t
        else:
            return self._lmdi.y_t1 / self._lmdi.pro_sum_t1
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
        if not self._cache.has_key('isg'):
            self._cache['isg'] = exp(sum(list(self._lmdi.isg())))
        return self._cache['isg']
    @property
    def isg_attributions(self):
        '''
        isg each province attribtuion
        '''
        if not self._cache.has_key('isg_attributions'):
            self._cache['isg_attributions'] = [k * v for k, v in zip(self.risg(), self.isg_ratio())]
        return self._cache['isg_attributions']
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
        if not self._cache.has_key('eue'):
            self._cache['eue'] = exp(sum(list(self._lmdi.eue())))
        return self._cache['eue']
    @property
    def eue_attributions(self):
        '''
        eue each province attribution
        '''
        if not self._cache.has_key('eue_attributions'):
            self._cache['eue_attributions'] = [k * v for k, v in zip(self.reue(), self.eue_ratio())]
        return self._cache['eue_attributions']
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
        if not self._cache.has_key('est'):
            self._cache['est'] = exp(sum(list(self._lmdi.est())))
        return self._cache['est']
    @property
    def est_attributions(self):
        '''
        est each province attribution
        '''
        if not self._cache.has_key('est_attributions'):
            self._cache['est_attributions'] = [k * v for k, v in zip(self.rest(), self.est_ratio())]
        return self._cache['est_attributions']
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
        if not self._cache.has_key('yoe'):
            self._cache['yoe'] = exp(sum(list(self._lmdi.yoe())))
        return self._cache['yoe']
    @property
    def yoe_attributions(self):
        '''
        yoe each province attribution
        '''
        if not self._cache.has_key('yoe_attributions'):
            self._cache['yoe_attributions'] = [k * v for k, v in zip(self.ryoe(), self.yoe_ratio())]
        return self._cache['yoe_attributions']
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
        if not self._cache.has_key('yct'):
            self._cache['yct'] = exp(sum(list(self._lmdi.yct())))
        return self._cache['yct']
    @property
    def yct_attributions(self):
        '''
        yct each province attribution
        '''
        if not self._cache.has_key('yct_attributions'):
            self._cache['yct_attributions'] = [k * v for k, v in zip(self.ryct(), self.yct_ratio())]
        return self._cache['yct_attributions']
     #emx
    def _peiij(self, i, j):
        dmu_t = self._dmus_t[i]
        dmu_t1 = self._dmus_t1[i]
        if dmu_t.co2[j] != 0.0  and dmu_t1.co2[j] != 0.0:
            sij_t = dmu_t.ene[j] / dmu_t.ene.total
            sij_t1 = dmu_t1.ene[j] / dmu_t1.ene.total
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
            sij_t = dmu_t.ene[j] / dmu_t.ene.total
            sij_t1 = dmu_t1.ene[j] / dmu_t1.ene.total
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
    def emx(self):
        '''
        the emx value
        '''
        if not self._cache.has_key('emx'):
            self._cache['emx'] = exp(sum(list(self._lmdi.emx())))
        return self._cache['emx']
    @property
    def emx_attributions(self):
        '''
        emx each province attribution
        '''
        if not self._cache.has_key('emx_attributions'):
            self._cache['emx_attributions'] = [k * v for k, v
                                               in zip(self.remx(), self.emx_ratio())]
        return self._cache['emx_attributions']
    @property
    def indexes(self):
        '''
        指数
        '''
        return [self.cef, self.emx, self.pei,
                self.pis, self.isg, self.eue,
                self.est, self.yoe, self.yct]
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

class Spaam_Factory(object):
    '''
    Spaam factory
    '''
    cache = {}
    @classmethod
    def build(cls, dmus_t, dmus_t1, name):
        '''
        创建一个 Spaam 对象
        '''
        if not Spaam_Factory.cache.has_key(name):
            Spaam_Factory.cache[name] = Spaam(dmus_t, dmus_t1, name)
        return Spaam_Factory.cache[name]
