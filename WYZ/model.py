# -*- coding:utf-8 -*-
'''
the model for Wang yi zhong
'''
class Dmu(object):
    '''
    the model for dmu (decision making unit)
    '''
    def __init__(self, **kw):
        for k, v in kw.items():
            setattr(self, k, v)