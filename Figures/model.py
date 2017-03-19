# -*- coding:utf8 -*- 
'''
the unit of index
'''
class Unit(object):
    '''
    the unit of the index
    '''
    def __init__(self, name, dyct, dpei, color):
        self._name = name
        self._dyct = dyct
        self._dpei = dpei
        self._color = color
    @property
    def name(self):
        return self._name
    @property
    def yct(self):
        return self._dyct
    @property
    def pei(self):
        return self._dpei
    @property
    def color(self):
        return self._color