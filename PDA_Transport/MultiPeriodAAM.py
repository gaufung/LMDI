# -*- coding:utf8 -*-
'''
multi period for attibution
'''
from SinglePeriodAAM import Spaam
class Mpaam(object):
    '''
    multi  period
    '''
    def __init__(self, dmus_s, name, dmus_global):
        self._period_count = len(dmus_s)
        self._dmus_s = dmus_s
        self._province_count = len(dmus_s[0])
        self._province_names = [item.name for item in dmus_s[0]]
        self._name = name
        self._cache = {}
        self._dmus_global = dmus_global
        self._year = {
            0 : '2006',
            1 : '2007',
            2 : '2008',
            3 : '2009',
            4 : '2010',
            5 : '2011',
            6 : '2012',
            7 : '2013',
            8 : '2014'
        }
    @property
    def name(self):
        '''
        the name of multi-periods attribution
        '''
        return self._name
    @property
    def province_names(self):
        '''
        the name of each provinces
        '''
        return self._province_names
    def _get_spaam(self, left, right):
        assert left != right
        label = str(left) + '-' + str(right)
        if not self._cache.has_key(label):
            self._cache[label] = Spaam.build(self._dmus_s[left], self._dmus_s[right],
                                             self._year[left]+'-'+self._year[right],
                                             self._dmus_global)
        return self._cache[label]
    # emx
    def emx(self):
        '''
        emx contribution
        '''
        result = []
        for i in range(self._province_count):
            value = 0.0
            for t in range(1, self._period_count):
                if t-1 != 0:
                    #spaam_0_t_1 = self._get_spaam(0, t-1)
                    emx = self.emx_t(t-1)
                    spaam_t_1_t = self._get_spaam(t-1, t)
                    contribution = spaam_t_1_t.remx()[i] * spaam_t_1_t.emx_ratio()[i]
                    value += emx * contribution
                else:
                    emx = 1.0
                    spaam_t_1_t = self._get_spaam(t-1, t)
                    contribution = spaam_t_1_t.remx()[i] * spaam_t_1_t.emx_ratio()[i]
                    value += emx * contribution
            result.append(value)
        return result
    def emx_t(self, t):
        '''
        计算跨期的emx
        '''
        emx = 1.0
        for i in range(1, t+1):
            emx *= self._get_spaam(i-1, i).emx
        return emx
    # cef
    def cef(self):
        '''
        the cef contribution
        '''
        result = []
        for i in range(self._province_count):
            value = 0.0
            for t in range(1, self._period_count):
                if t-1 != 0:
                    #spaam_0_t_1 = self._get_spaam(0, t - 1)
                    cef = self.cef_t(t-1)
                    spaam_t_1_t = self._get_spaam(t-1, t)
                    contribution = spaam_t_1_t.rcef()[i] * spaam_t_1_t.cef_ratio()[i]
                    value += cef * contribution
                else:
                    cef = 1.0
                    spaam_t_1_t = self._get_spaam(t-1, t)
                    contribution = spaam_t_1_t.rcef()[i] * spaam_t_1_t.cef_ratio()[i]
                    value += cef * contribution
            result.append(value)
        return result
    def cef_t(self, t):
        '''
        计算跨期
        '''
        cef = 1.0
        for i in range(1, t+1):
            cef *= self._get_spaam(i-1, i).cef
        return cef
    # pei
    def pei_t(self, t):
        '''
        pei multi period
        '''
        pei = 1.0
        for i in range(1, t+1):
            pei *= self._get_spaam(i-1, i).pei
        return pei
    def pei(self):
        '''
        pei
        '''
        result = []
        for i in range(self._province_count):
            value = 0.0
            for t in range(1, self._period_count):
                if t-1 != 0:
                    #spaam_0_t_1 = self._get_spaam(0, t - 1)
                    pei = self.pei_t(t-1)
                    spaam_t_1_t = self._get_spaam(t-1, t)
                    contribution = spaam_t_1_t.rpei()[i] * spaam_t_1_t.pei_ratio()[i]
                    value += pei * contribution
                else:
                    pei = 1.0
                    spaam_t_1_t = self._get_spaam(t-1, t)
                    contribution = spaam_t_1_t.rpei()[i] * spaam_t_1_t.pei_ratio()[i]
                    value += pei * contribution
            result.append(value)
        return result
    #est
    def est_t(self, t):
        '''
        计算跨期
        '''
        est = 1.0
        for i in range(1, t+1):
            est *= self._get_spaam(i-1, i).est
        return est
    def est(self):
        '''
        est
        '''
        result = []
        for i in range(self._province_count):
            value = 0.0
            for t in range(1, self._period_count):
                if t-1 != 0:
                    #spaam_0_t_1 = self._get_spaam(0, t - 1)
                    est = self.est_t(t-1)
                    spaam_t_1_t = self._get_spaam(t-1, t)
                    contribution = spaam_t_1_t.rest()[i] * spaam_t_1_t.est_ratio()[i]
                    value += est * contribution
                else:
                    est = 1.0
                    spaam_t_1_t = self._get_spaam(t-1, t)
                    contribution = spaam_t_1_t.rest()[i] * spaam_t_1_t.est_ratio()[i]
                    value += est * contribution
            result.append(value)
        return result
    # eue
    def eue_t(self, t):
        '''
        计算跨期
        '''
        eue = 1.0
        for i in range(1, t+1):
            eue *= self._get_spaam(i-1, i).eue
        return eue
    def eue(self):
        '''
        eue
        '''
        result = []
        for i in range(self._province_count):
            value = 0.0
            for t in range(1, self._period_count):
                if t-1 != 0:
                    #spaam_0_t_1 = self._get_spaam(0, t - 1)
                    eue = self.eue_t(t-1)
                    spaam_t_1_t = self._get_spaam(t-1, t)
                    contribution = spaam_t_1_t.reue()[i] * spaam_t_1_t.eue_ratio()[i]
                    value += eue * contribution
                else:
                    eue = 1.0
                    spaam_t_1_t = self._get_spaam(t-1, t)
                    contribution = spaam_t_1_t.reue()[i] * spaam_t_1_t.eue_ratio()[i]
                    value += eue * contribution
            result.append(value)
        return result
    # pti
    def pti_t(self, t):
        '''
        计算跨期
        '''
        pti = 1.0
        for i in range(1, t+1):
            pti *= self._get_spaam(i-1, i).pti
        return pti
    def pti(self):
        '''
        pti
        '''
        result = []
        for i in range(self._province_count):
            value = 0.0
            for t in range(1, self._period_count):
                if t-1 != 0:
                    #spaam_0_t_1 = self._get_spaam(0, t - 1)
                    pti = self.pti_t(t-1)
                    spaam_t_1_t = self._get_spaam(t-1, t)
                    contribution = spaam_t_1_t.rpti()[i] * spaam_t_1_t.pti_ratio()[i]
                    value += pti * contribution
                else:
                    pti = 1.0
                    spaam_t_1_t = self._get_spaam(t-1, t)
                    contribution = spaam_t_1_t.rpti()[i] * spaam_t_1_t.pti_ratio()[i]
                    value += pti * contribution
            result.append(value)
        return result
    # yoe
    def yoe_t(self, t):
        '''
        计算跨期
        '''
        yoe = 1.0
        for i in range(1, t+1):
            yoe *= self._get_spaam(i-1, i).yoe
        return yoe
    def yoe(self):
        '''
        yoe
        '''
        result = []
        for i in range(self._province_count):
            value = 0.0
            for t in range(1, self._period_count):
                if t-1 != 0:
                    #spaam_0_t_1 = self._get_spaam(0, t - 1)
                    yoe = self.yoe_t(t-1)
                    spaam_t_1_t = self._get_spaam(t-1, t)
                    contribution = spaam_t_1_t.ryoe()[i] * spaam_t_1_t.yoe_ratio()[i]
                    value += yoe * contribution
                else:
                    yoe = 1.0
                    spaam_t_1_t = self._get_spaam(t-1, t)
                    contribution = spaam_t_1_t.ryoe()[i] * spaam_t_1_t.yoe_ratio()[i]
                    value += yoe * contribution
            result.append(value)
        return result
    # yct
    def yct_t(self,t):
        '''
        计算跨期
        '''
        yct = 1.0
        for i in range(1, t+1):
            yct *= self._get_spaam(i-1, i).yct
        return yct
    def yct(self):
        '''
        yct
        '''
        result = []
        for i in range(self._province_count):
            value = 0.0
            for t in range(1, self._period_count):
                if t-1 != 0:
                    #spaam_0_t_1 = self._get_spaam(0, t - 1)
                    yct = self.yct_t(t-1)
                    spaam_t_1_t = self._get_spaam(t-1, t)
                    contribution = spaam_t_1_t.ryct()[i] * spaam_t_1_t.yct_ratio()[i]
                    value += yct * contribution
                else:
                    yct = 1.0
                    spaam_t_1_t = self._get_spaam(t-1, t)
                    contribution = spaam_t_1_t.ryct()[i] * spaam_t_1_t.yct_ratio()[i]
                    value += yct * contribution
            result.append(value)
        return result
    #rts
    def rts_t(self, t):
        '''
        计算跨期
        '''
        rts = 1.0
        for i in range(1, t+1):
            rts *= self._get_spaam(i-1, i).rts
        return rts
    def rts(self):
        '''
        rts
        '''
        result = []
        for i in range(self._province_count):
            value = 0.0
            for t in range(1, self._period_count):
                if t-1 != 0:
                    #spaam_0_t_1 = self._get_spaam(0, t - 1)
                    rts = self.rts_t(t-1)
                    spaam_t_1_t = self._get_spaam(t-1, t)
                    contribution = spaam_t_1_t.rrts()[i] * spaam_t_1_t.rts_ratio()[i]
                    value += rts * contribution
                else:
                    rts = 1.0
                    spaam_t_1_t = self._get_spaam(t-1, t)
                    contribution = spaam_t_1_t.rrts()[i] * spaam_t_1_t.rts_ratio()[i]
                    value += rts * contribution
            result.append(value)
        return result
    def indexes(self, t):
        '''
        返回系数
        '''
        return [self.cef_t(t), self.emx_t(t), self.pei_t(t),
                self.est_t(t), self.eue_t(t), self.pti_t(t),
                self.yoe_t(t), self.yct_t(t), self.rts_t(t)]