# -*- encoding:utf-8 -*-
from single_period_aam import Spaam


class Mpaam(object):
    def __init__(self, dmus_s, name, global_dmus, cefs, years):
        self._period_count = len(dmus_s)
        self._dmus_s = dmus_s
        self._province_count = len(dmus_s[0])
        self._province_names = [item.name for item in dmus_s[0]]
        self._name = name
        self._cache = {}
        self._global_dmus = global_dmus
        self._cefs = cefs
        self._years = years

    @property
    def name(self):
        return self._name

    @property
    def province_names(self):
        return self._province_names

    def _get_spaam(self, left, right):
        assert left != right
        label = str(left) + '-' + str(right)
        if label not in self._cache:
            self._cache[label] = Spaam.build(self._dmus_s[left], self._dmus_s[right],
                                             self._years[left] + '-' + self._years[right],
                                             self._global_dmus, self._cefs)
        return self._cache[label]

    def _index_t(self, t, index_name):
        result = 1.0
        for i in range(1, t + 1):
            result *= getattr(self._get_spaam(i - 1, i), index_name)
        return result

    def _index(self, index_name):
        result = []
        for i in range(self._province_count):
            value = 0.0
            for t in range(1, self._period_count):
                aggerate_value = self._index_t(t - 1, index_name)
                spaam_t_1_t = self._get_spaam(t - 1, t)
                contribution = (getattr(spaam_t_1_t, 'r' + index_name)()[i] *
                                getattr(spaam_t_1_t, index_name + '_ratio')()[i])
                value += aggerate_value * contribution
            result.append(value)
        return result

    # emx
    def emx(self):
        return self._index('emx')

    def emx_t(self, t):
        return self._index_t(t, 'emx')

    # cef
    def cef(self):
        return self._index('cef')

    def cef_t(self, t):
        return self._index_t(t, 'cef')

    # pei
    def pei_t(self, t):
        return self._index_t(t, 'pei')

    def pei(self):
        return self._index('pei')

    # est
    def est_t(self, t):
        return self._index_t(t, 'est')

    def est(self):
        return self._index('est')

    # eue
    def eue_t(self, t):
        return self._index_t(t, 'eue')

    def eue(self):
        return self._index('eue')

    # pti
    def pti_t(self, t):
        return self._index_t(t, 'pti')

    def pti(self):
        return self._index('pti')

    # yoe
    def yoe_t(self, t):
        return self._index_t(t, 'yoe')

    def yoe(self):
        return self._index('yoe')

    # yct
    def yct_t(self, t):
        return self._index_t(t, 'yct')

    def yct(self):
        return self._index('yct')

    # rts
    def rts_t(self, t):
        return self._index_t(t, 'rts')

    def rts(self):
        return self._index('rts')

    def indexes(self, t):
        return [self.cef_t(t), self.emx_t(t), self.pei_t(t),
                self.est_t(t), self.eue_t(t), self.pti_t(t),
                self.yoe_t(t), self.yct_t(t), self.rts_t(t)]