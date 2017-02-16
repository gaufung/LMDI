# -*- coding:utf8 -*-
from __future__ import division
import logging
from pulp import LpProblem, lpSum, LpVariable, LpMinimize, LpMaximize

def _add_elements(sequenece, *elements):
    '''
    add elements into sequenece
    [1,2,0,10] ->(4,5)
    -> [1,2,0,10,4,5]
    '''
    for element in elements:
        sequenece.append(element)
def _reciprocal(func):
    def _wrapper(*args, **kw):
        result = func(*args, **kw)
        return [1.0 / x for x in result]
    return _wrapper

def _pis_min(energies, productions, co2s, turn_overs, dmu_right):
    '''
    psi min value
    '''
    energy_right = dmu_right.energy.total
    co2_right = dmu_right.co2.total
    turn_over_right = dmu_right.turn_over.turn_over
    produciton_right = dmu_right.production.production
    prob = LpProblem("lambda_min", LpMinimize)
    variables_count = len(energies)
    ingredients = [str(symbols + 1) for symbols in range(variables_count)]
    symbols = LpVariable.dict('x_%s', ingredients, lowBound=0)
    cost = dict(zip(ingredients, energies))
    prob += lpSum([cost[i] * symbols[i] for i in ingredients])
    turn_over_dict = dict(zip(ingredients, turn_overs))
    production_dict = dict(zip(ingredients, productions))
    co2_dict = dict(zip(ingredients, co2s))
    prob += lpSum([turn_over_dict[i]* symbols[i]
                   for i in ingredients]) >= turn_over_right
    prob += lpSum([production_dict[i]*symbols[i]
                   for i in ingredients]) >= produciton_right
    prob += lpSum([co2_dict[i] * symbols[i]
                   for i in ingredients]) == co2_right
    if prob.solve() != 1:
        raise UserWarning
    else:
        return prob.objective.value() / energy_right
@_reciprocal
def psi_min(dmus_s, dmus_right):
    '''
    pis min value
    '''
    energies = []
    productions = []
    co2s = []
    turn_overs = []
    for dmus in dmus_s:
        for dmu in dmus:
            energies.append(dmu.energy.total)
            productions.append(dmu.production.production)
            co2s.append(dmu.co2.total)
            turn_overs.append(dmu.turn_over.turn_over)
    _add_elements(energies, 1.0)
    _add_elements(turn_overs, 0.0)
    _add_elements(productions, 0.0)
    _add_elements(co2s, 0.0)
    result = []
    for dmu in dmus_right:
        result.append(_pis_min(energies, productions, co2s, turn_overs, dmu))
    return result

def _eta_max(energies, productions, co2s, turn_overs, dmu_right):
    '''
    eta max
    '''
    energy_right = dmu_right.energy.total
    co2_right = dmu_right.co2.total
    turn_over_right = dmu_right.turn_over.turn_over
    produciton_right = dmu_right.production.production
    prob = LpProblem('eta max', LpMaximize)
    variables_count = len(productions)
    ingredients = [str(symbols + 1) for symbols in range(variables_count)]
    symbols = LpVariable.dict('x_%s', ingredients, lowBound=0)
    cost = dict(zip(ingredients, productions))
    prob += lpSum([cost[i] * symbols[i] for i in ingredients])
    energy_dict = dict(zip(ingredients, energies))
    turn_over_dict = dict(zip(ingredients, turn_overs))
    co2_dict = dict(zip(ingredients, co2s))
    prob += lpSum([energy_dict[i] * symbols[i]
                   for i in ingredients]) <= energy_right
    prob += lpSum([turn_over_dict[i] * symbols[i]
                   for i in ingredients]) >= turn_over_right
    prob += lpSum([co2_dict[i] * symbols[i]
                   for i in ingredients]) == co2_right
    if prob.solve() != 1:
        raise UserWarning
    else:
        return prob.objective.value() / produciton_right
@_reciprocal
def eta_max(dmus_s, dmus_right):
    '''
    eta max
    '''
    energies = []
    productions = []
    co2s = []
    turn_overs = []
    for dmus in dmus_s:
        for dmu in dmus:
            energies.append(dmu.energy.total)
            productions.append(dmu.production.production)
            co2s.append(dmu.co2.total)
            turn_overs.append(dmu.turn_over.turn_over)
    _add_elements(energies, 0.0)
    _add_elements(turn_overs, 0.0)
    _add_elements(co2s, 0.0)
    _add_elements(productions, -1.0)
    result = []
    for dmu in dmus_right:
        result.append(_eta_max(energies, productions, co2s, turn_overs, dmu))
    return result


