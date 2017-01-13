# -*- coding:utf8 -*-
# multiperiod attribute analysis method
from Model import *
from LMDI import Lmdi
from math import sqrt, log, exp
from SinglePeriodAAM import Spaam

class Mpaam(object):
    '''
    multi period
    '''
    def __init__(self, dmus_s):
        '''
        dmus_s is a list of dmus, the first one is first period
        the last is last period
        '''
        assert len(dmus_s) > 1
        self._period_count = len(dmus_s)
        self._dmus_s = dmus_s
        self._province_count = len(dmus_s[0])
        self._cache = {}
    def _get_spaam(self, left, right):
        assert left != right
        label = str(left) + '-' + str(right)
        if not self._cache.has_key(label):
            self._cache[label] = Spaam(self._dmus_s[left], self._dmus_s[right])
        return self._cache[label]
    def emx(self):
        '''
        emx contribution
        '''
        result = []
        for i in range(self._province_count):
            value = []
            for t in range(1, self._period_count):
                if t-1 != 0:
                    spaam_0_t_1 = self._get_spaam(0, t-1)
                    emx = spaam_0_t_1.emx()
                    spaam_t_1_t = self._get_spaam(t-1, t)
                    contribution = spaam_t_1_t.remx()[i] * spaam_t_1_t.emx_ratio()[i]
                    value.append(emx * contribution)
                else:
                    emx = 1.0
                    spaam_t_1_t = self._get_spaam(t-1, t)
                    contribution = spaam_t_1_t.remx()[i] * spaam_t_1_t.emx_ratio()[i]
                    value.append(emx * contribution)
            result.append(sum(value))
        return result
    def pei(self):
        '''
        pei contribution
        '''
        result = []
        for i in range(self._province_count):
            value = 0.0
            for t in range(1, self._period_count):
                if t-1 != 0:
                    spaam_0_t_1 = self._get_spaam(0, t - 1)
                    pei = spaam_0_t_1.pei()
                    spaam_t_1_t = self._get_spaam(t - 1, t)
                    contribution = spaam_t_1_t.rpei()[i] * spaam_t_1_t.peiRatio()[i]
                    value += pei * contribution
                else:
                    pei = 1.0
                    spaam_t_1_t = self._get_spaam(t-1, t)
                    contribution = spaam_t_1_t.rpei()[i] * spaam_t_1_t.peiRatio()[i]
                    value += pei * contribution
            result.append(value)
        return result
    def pis(self):
        '''
        pis contribution
        '''
        result = []
        for i in range(self._province_count):
            value = 0.0
            for t in range(1, self._province_count):
                if t-1 != 0:
                    spaam_0_t_1 = self._get_spaam(0,t - 1)
                    pis = spaam_0_t_1.pis()
                    spaam_t_1_t = self._get_spaam(t-1, t)
                    contribution = spaam_t_1_t.rpis()[i] * spaam_t_1_t.pisRatio()[i]
                    value += pis * contribution
                else:
                    pis = 1.0
                    spaam_t_1_t = self._get_spaam(t-1, t)
                    contribution = spaam_t_1_t.rpis()[i] * spaam_t_1_t.pisRatio()[i]
                    value += pis * contribution
            result.append(value)
        return result
    def isg(self):
        '''
        isg contribution
        '''
        result = []
        for i in range(self._province_count):
            value = 0.0
            for t in range(1, self._period_count):
                if t-1 != 0:
                    spaam_0_t_1 = self._get_spaam(0, t - 1)
                    isg = spaam_0_t_1.isg()
                    spaam_t_1_t = self._get_spaam(t-1, t)
                    contribution = spaam_t_1_t.risg()[i] * spaam_t_1_t.isgRatio()[i]
                    value += isg * contribution
                else:
                    isg = 1.0
                    spaam_t_1_t = self._get_spaam(t-1, t)
                    contribution = spaam_t_1_t.risg()[i] * spaam_t_1_t.isgRatio()[i]
                    value += isg * contribution
            result.append(value)
        return result
    def eue(self):
        '''
        eue contribution
        '''
        result = []
        for i in range(self._province_count):
            value = 0.0
            for t in range(1, self._period_count):
                if t-1 != 0:
                    spaam_0_t_1 = self._get_spaam(0, t - 1)
                    eue = spaam_0_t_1.eue()
                    spaam_t_1_t = self._get_spaam(t-1, t)
                    contribution = spaam_t_1_t.reue()[i] * spaam_t_1_t.eueRatio()[i]
                    value += eue * contribution
                else:
                    eue = 1.0
                    spaam_t_1_t = self._get_spaam(t-1, t)
                    contribution = spaam_t_1_t.reue()[i] * spaam_t_1_t.eueRatio()[i]
                    value += eue * contribution
            result.append(value)
        return result
    def est(self):
        '''
        est contribution
        '''
        result = []
        for i in range(self._province_count):
            value = 0.0
            for t in range(1, self._period_count):
                if t-1 != 0:
                    spaam_0_t_1 = self._get_spaam(0, t - 1)
                    est = spaam_0_t_1.est()
                    spaam_t_1_t = self._get_spaam(t-1, t)
                    contribution = spaam_t_1_t.rest()[i] * spaam_t_1_t.estRatio()[i]
                    value += est * contribution
                else:
                    est = 1.0
                    spaam_t_1_t = self._get_spaam(t-1, t)
                    contribution = spaam_t_1_t.rest()[i] * spaam_t_1_t.estRatio()[i]
                    value += est * contribution
            result.append(value)
        return result
    def yoe(self):
        '''
        the yoe contribution
        '''
        result = []
        for i in range(self._province_count):
            value = 0.0
            for t in range(1, self._period_count):
                if t-1 != 0:
                    spaam_0_t_1 = self._get_spaam(0, t - 1)
                    yoe = spaam_0_t_1.yoe()
                    spaam_t_1_t = self._get_spaam(t-1, t)
                    contribution = spaam_t_1_t.ryoe()[i] * spaam_t_1_t.yoeRatio()[i]
                    value += yoe * contribution
                else:
                    yoe = 1.0
                    spaam_t_1_t = self._get_spaam(t-1, t)
                    contribution = spaam_t_1_t.ryoe()[i] * spaam_t_1_t.yoeRatio()[i]
                    value += yoe * contribution
            result.append(value)
        return result
    def yct(self):
        '''
        yct contribution
        '''
        result = []
        for i in range(self._province_count):
            value = 0.0
            for t in range(1, self._period_count):
                if t-1 != 0:
                    spaam_0_t_1 = self._get_spaam(0, t - 1)
                    yct = spaam_0_t_1.yct()
                    spaam_t_1_t = self._get_spaam(t-1, t)
                    contribution = spaam_t_1_t.ryct()[i] * spaam_t_1_t.yctRatio()[i]
                    value += yct * contribution
                else:
                    yct = 1.0
                    spaam_t_1_t = self._get_spaam(t-1, t)
                    contribution = spaam_t_1_t.ryct()[i] * spaam_t_1_t.yctRatio()[i]
                    value += yct * contribution
            result.append(value)
        return result
