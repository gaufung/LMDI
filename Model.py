# -*- coding:utf8 -*-
'''
The model for PDA
'''


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
        return self._energy[-1]

    def __len__(self):
        '''
        the length of Energy
        '''
        return len(self._energy)

    def __getitem__(self, index):
        '''
        get the special energy consumption by index
        '''
        assert index <= len(self)
        return self._energy[index]

    def __setitem__(self, index, value):
        '''
        set the special energy consumption by index
        '''
        assert index <= len(self)
        self._energy[index] = value


class Co2(object):
    '''
    The co2 emission
    '''

    def __init__(self, name, co2):
        self._name = name
        self._co2 = co2

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
        return self._co2[-1]

    @property
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


class Dmu(object):
    '''
    the decision making unit
    '''

    def __init__(self, e, p, c):
        self._ene = e
        self._pro = p
        self._co2 = c

    @property
    def name(self):
        '''
        the name of this decision making unit
        '''
        if self._ene is None and self._pro is None and self._co2 is None:
            raise Exception
        else:
            return self._pro.name

    @property
    def pro(self):
        '''
        the production of this decision making unit
        '''
        return self._pro

    @property
    def co2(self):
        '''
        the co2 emission of this decision making unit
        '''
        return self._co2

    @property
    def ene(self):
        '''
        the energy consumption of this decision making unit
        '''
        return self._ene

    def energy_count(self):
        '''
        the number of this energy consumption
        '''
        return len(self._ene) - 1
