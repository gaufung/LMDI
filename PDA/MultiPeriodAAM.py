# -*- coding:utf8 -*-
# multiperiod attribute analysis method

from Model import *
from SinglePeriodAAM import Spaam_Factory

class Mpaam(object):
    '''
    multi period
    '''
    def __init__(self, dmus_s, name):
        '''
        dmus_s is a list of dmus, the first one is first period
        the last is last period
        '''
        assert len(dmus_s) > 1
        self._period_count = len(dmus_s)
        self._dmus_s = dmus_s
        self._province_count = len(dmus_s[0])
        self._province_names = [item.name for item in dmus_s[0]]
        self._cache = {}
        self._name = name
        self._year={0 : '2006',
                    1 : '2007',
                    2 : '2008',
                    3 : '2009',
                    4 : '2010',
                    5 : '2011',
                    6 : '2012',
                    7 : '2013',
                    8 : '2014'}
    @property
    def name(self):
        '''
        the name of multi-periods attribution
        '''
        return self._name
    @property
    def province_names(self):
        '''
        the names of provinces
        '''
        return self._province_names
    def _get_spaam(self, left, right):
        assert left != right
        label = str(left) + '-' + str(right)
        if not self._cache.has_key(label):
            self._cache[label] = Spaam_Factory.build(self._dmus_s[left], self._dmus_s[right],
                                                     self._year[left]+'-'+self._year[right])
        return self._cache[label]
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
    def pei(self):
        '''
        pei contribution
        '''
        result = []
        for i in range(self._province_count):
            value = 0.0
            for t in range(1, self._period_count):
                if t-1 != 0:
                    #spaam_0_t_1 = self._get_spaam(0, t - 1)
                    pei = self.pei_t(t-1)
                    spaam_t_1_t = self._get_spaam(t - 1, t)
                    contribution = spaam_t_1_t.rpei()[i] * spaam_t_1_t.pei_ratio()[i]
                    value += pei * contribution
                else:
                    pei = 1.0
                    spaam_t_1_t = self._get_spaam(t-1, t)
                    contribution = spaam_t_1_t.rpei()[i] * spaam_t_1_t.pei_ratio()[i]
                    value += pei * contribution
            result.append(value)
        return result
    def pei_t(self, t):
        '''
        计算跨期的pei
        '''
        pei = 1.0
        for i in range(1, t+1):
            pei *= self._get_spaam(i-1, i).pei
        return pei
    def pis(self):
        '''
        pis contribution
        '''
        result = []
        for i in range(self._province_count):
            value = 0.0
            for t in range(1, self._period_count):
                if t-1 != 0:
                    #spaam_0_t_1 = self._get_spaam(0, t - 1)
                    pis = self.pis_t(t-1)
                    spaam_t_1_t = self._get_spaam(t-1, t)
                    contribution = spaam_t_1_t.rpis()[i] * spaam_t_1_t.pis_ratio()[i]
                    value += pis * contribution
                else:
                    pis = 1.0
                    spaam_t_1_t = self._get_spaam(t-1, t)
                    contribution = spaam_t_1_t.rpis()[i] * spaam_t_1_t.pis_ratio()[i]
                    value += pis * contribution
            result.append(value)
        return result
    def pis_t(self, t):
        '''
        计算 pei 跨期
        '''
        pis = 1.0
        for i in range(1, t+1):
            pis *= self._get_spaam(i-1, i).pis
        return pis
    def isg(self):
        '''
        isg contribution
        '''
        result = []
        for i in range(self._province_count):
            value = 0.0
            for t in range(1, self._period_count):
                if t-1 != 0:
                    #spaam_0_t_1 = self._get_spaam(0, t - 1)
                    isg = self.isg_t(t-1)
                    spaam_t_1_t = self._get_spaam(t-1, t)
                    contribution = spaam_t_1_t.risg()[i] * spaam_t_1_t.isg_ratio()[i]
                    value += isg * contribution
                else:
                    isg = 1.0
                    spaam_t_1_t = self._get_spaam(t-1, t)
                    contribution = spaam_t_1_t.risg()[i] * spaam_t_1_t.isg_ratio()[i]
                    value += isg * contribution
            result.append(value)
        return result
    def isg_t(self, t):
        '''
        计算isg 跨期
        '''
        isg = 1.0 
        for i in range(1, t+1):
            isg *= self._get_spaam(i-1, i).isg
        return isg
    def eue(self):
        '''
        eue contribution
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
    def eue_t(self, t):
        '''
        计算 eue 跨期
        '''
        eue = 1.0
        for i in range(1, t+1):
            eue *= self._get_spaam(i-1, i).eue
        return eue
    def est(self):
        '''
        est contribution
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
    def est_t(self, t):
        '''
        计算跨期 est 
        '''
        est = 1.0
        for i in range(1, t+1):
            est *= self._get_spaam(i-1, i).est
        return est
    def yoe(self):
        '''
        the yoe contribution
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
    def yoe_t(self, t):
        '''
        计算跨期 yoe
        '''
        yoe = 1.0
        for i in range(1, t+1):
            yoe *= self._get_spaam(i-1, i).yoe
        return yoe
    def yct(self):
        '''
        yct contribution
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
    def yct_t(self, t):
        '''
        计算跨期
        '''
        yct = 1.0
        for i in range(1, t+1):
            yct *= self._get_spaam(i-1, i).yct
        return yct
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
    def indexes(self, t):
        '''
        返回系数
        '''
        return [self.cef_t(t), self.emx_t(t), self.pei_t(t),
                self.pis_t(t), self.isg_t(t), self.eue_t(t),
                self.est_t(t), self.yoe_t(t), self.yct_t(t)]
