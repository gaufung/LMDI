# -*- coding:utf-8 -*-
'''
the model for Wang yi zhong
'''
class Dmu(object):
    '''
    the model for dmu (decision making unit)
    '''
    def __init__(self, name, energy, capital, labour, produciton, co2):
        self._name = name
        self._energy = energy
        self._capital = capital
        self._labour = labour
        self._production = produciton
        self._co2 = co2
    @property
    def name(self):
        '''
        the name of dmu
        '''
        return self._name
    @property
    def energy(self):
        '''
        energy
        '''
        return self._energy
    @property
    def capital(self):
        '''
        capital
        '''
        return self._capital
    @property
    def labour(self):
        '''
        labour
        '''
        return self._labour
    @property
    def production(self):
        '''
        produciton
        '''
        return self._production
    @property
    def co2(self):
        '''
        co2
        '''
        return self._co2
    