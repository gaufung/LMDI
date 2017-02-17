# -*- coding:utf8 -*-
'''
the model for this project
energy, production, turn_over, co2
'''
from __future__ import unicode_literals

class Energy(object):
    '''
    the Energy model
    '''

    def __init__(self, name, energy):
        '''
        The construction funtion
        '''
        self._name = name
        self._energy = energy
        self._total = sum(energy)

    @property
    def name(self):
        '''
        the province name
        '''
        return self._name

    @property
    def energy(self):
        '''
        the energy
        '''
        return self._energy

    @property
    def total(self):
        '''
        total energy sumpation
        '''
        return self._total

    def __len__(self):
        '''
        the length of Energy
        '''
        return len(self._energy)

    def __getitem__(self, index):
        '''
        get the special energy consumption by index
        '''
        assert index < len(self)
        return self._energy[index]

    def __setitem__(self, index, value):
        '''
        set the special energy consumption by index
        '''
        assert index < len(self)
        self._energy[index] = value


class Co2(object):
    '''
    The co2 emission
    '''

    def __init__(self, name, co2):
        self._name = name
        self._co2 = co2
        self._total = sum(co2)

    @property
    def name(self):
        '''
        the province name
        '''
        return self._name

    @property
    def co2(self):
        '''
        the co2
        '''
        return self._co2

    @property
    def total(self):
        '''
        total co2 emission
        '''
        return self._total

    def __len__(self):
        '''
        the length of co2
        '''
        return len(self._co2)

    def __getitem__(self, index):
        '''
        get the special co2 emission by index
        '''
        return self._co2[index]

    def __setitem__(self, index, value):
        '''
        set the special co2 emission by index
        '''
        self._co2[index] = value


class Production(object):
    '''
    the production of each province
    '''

    def __init__(self, name, prodcution):
        self._name = name
        self._production = prodcution

    @property
    def name(self):
        '''
        the name of province
        '''
        return self._name

    @property
    def production(self):
        '''
        the production of this province
        '''
        return self._production

class Turnover(object):
    '''
    the turn over of each dmu
    '''
    def __init__(self, name, turn_over):
        self._name = name
        self._turn_over = turn_over
    @property
    def name(self):
        '''
        the name of province
        '''
        return self._name
    @property
    def turn_over(self):
        '''
        the turn over of this dmu
        '''
        return self._turn_over

class Dmu(object):
    '''
    the dmu
    '''
    def __init__(self, energy, production, co2, turn_over):
        self._energy = energy
        self._produciton = production
        self._co2 = co2
        self._turn_over = turn_over
    @property
    def energy(self):
        '''
        the energy
        '''
        return self._energy
    @property
    def production(self):
        '''
        the production
        '''
        return self._produciton
    @property
    def co2(self):
        '''
        the Co2
        '''
        return self._co2
    @property
    def turn_over(self):
        '''
        the turn over
        '''
        return self._turn_over
    @property
    def name(self):
        '''
        the name of province
        '''
        return self._co2.name
    @property
    def energy_count(self):
        '''
        the energy count
        '''
        return len(self._energy)

