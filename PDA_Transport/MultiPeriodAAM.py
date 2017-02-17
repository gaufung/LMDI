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
    def _index_t(self, t, index_name):
        result = 1.0
        for i in range(1, t+1):
            result *= getattr(self._get_spaam(i-1, i), index_name)
        return result
    def _index(self, index_name):
        result = []
        for i in range(self._province_count):
            value = 0.0
            for t in range(1, self._period_count):
                aggerate_value = self._index_t(t-1, index_name)
                spaam_t_1_t = self._get_spaam(t-1, t)
                contribution = (getattr(spaam_t_1_t, 'r'+index_name)()[i] *
                                getattr(spaam_t_1_t, index_name+'_ratio')()[i])
                value += aggerate_value * contribution
            result.append(value)
        return result
    # emx
    def emx(self):
        '''
        emx contribution
        '''
        return self._index('emx')
    def emx_t(self, t):
        '''
        计算跨期的emx
        '''
        return self._index_t(t, 'emx')
    # cef
    def cef(self):
        '''
        the cef contribution
        '''
        return self._index('cef')
    def cef_t(self, t):
        '''
        计算跨期
        '''
        return self._index_t(t, 'cef')
    # pei
    def pei_t(self, t):
        '''
        pei multi period
        '''
        return self._index_t(t, 'pei')
    def pei(self):
        '''
        pei
        '''
        return self._index('pei')
    #est
    def est_t(self, t):
        '''
        计算跨期
        '''
        return self._index_t(t, 'est')
    def est(self):
        '''
        est
        '''
        return self._index('est')
    # eue
    def eue_t(self, t):
        '''
        计算跨期
        '''
        return self._index_t(t, 'eue')
    def eue(self):
        '''
        eue
        '''
        return self._index('eue')
    # pti
    def pti_t(self, t):
        '''
        计算跨期
        '''
        return self._index_t(t, 'pti')
    def pti(self):
        '''
        pti
        '''
        return self._index('pti')
    # yoe
    def yoe_t(self, t):
        '''
        计算跨期
        '''
        return self._index_t(t, 'yoe')
    def yoe(self):
        '''
        yoe
        '''
        return self._index('yoe')
    # yct
    def yct_t(self, t):
        '''
        计算跨期
        '''
        return self._index_t(t, 'yct')
    def yct(self):
        '''
        yct
        '''
        return self._index('yct')
    #rts
    def rts_t(self, t):
        '''
        计算跨期
        '''
        return self._index_t(t, 'rts')
    def rts(self):
        '''
        rts
        '''
        return self._index('rts')
    def indexes(self, t):
        '''
        返回系数
        '''
        return [self.cef_t(t), self.emx_t(t), self.pei_t(t),
                self.est_t(t), self.eue_t(t), self.pti_t(t),
                self.yoe_t(t), self.yct_t(t), self.rts_t(t)]
