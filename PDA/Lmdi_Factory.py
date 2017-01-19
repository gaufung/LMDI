# -*- coding:utf8 -*-
from LMDI import Lmdi
'''
LMDI 工厂
通过内部的一个字典项重复使用的 LMDI 对象保存下来
'''
class LmdiFactory(object):
    '''
    Lmdi factory
    '''
    cache = {}
    @classmethod
    def build(cls, dmus_t, dmus_t1, name):
        '''
        创建一个 LMDI 对象
        '''
        if not LmdiFactory.cache.has_key(name):
            LmdiFactory.cache[name] = Lmdi(dmus_t, dmus_t1, name)
        return LmdiFactory.cache[name]
        