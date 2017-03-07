# -*- coding:utf -*-
'''
linear propramming
'''
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

def _universal_linprog(kind, object_cost, constrains_left,
                       constrains_right, constrains_type, addition=1.0):
    '''
    '''
    prob = LpProblem('max_lp', LpMaximize) if kind == 'max' else LpProblem('min_lp', LpMinimize)
    variables_count = len(object_cost)
    ingredients = [str(symbol+1) for symbol in range(variables_count)]
    symbols = LpVariable.dict('x_%s', ingredients, lowBound=0)
    cost = dict(zip(ingredients, object_cost))
    prob += lpSum([cost[i] * symbols[i] for i in ingredients])
    for (constrain_left, constrain_right, constrain_type) in zip(constrains_left,
                                                                 constrains_right,
                                                                 constrains_type):
        constrain_dict = dict(zip(ingredients, constrain_left))
        if constrain_type == '<=':
            prob += lpSum([constrain_dict[i] * symbols[i] for i in ingredients]) <= constrain_right
        elif constrain_type == '<':
            prob += lpSum([constrain_dict[i] * symbols[i] for i in ingredients]) < constrain_right
        elif constrain_type == '>=':
            prob += lpSum([constrain_dict[i] * symbols[i] for i in ingredients]) >= constrain_right
        elif constrain_type == '>':
            prob += lpSum([constrain_dict[i] * symbols[i] for i in ingredients]) > constrain_right
        else:
            prob += lpSum([constrain_dict[i] * symbols[i] for i in ingredients]) == constrain_right
    if prob.solve() != 1:
        logging.error(kind+' unsolved situation occurs')
        raise UserWarning
    else:
        return prob.objective.value() / addition

def _theta_min(energies, capitals, labours, productions, co2s,
               dmu_right):
    '''
    theta min
    '''
    energy_right = dmu_right.energy
    capital_right = dmu_right.capital
    labour_right = dmu_right.labour
    production_right = dmu_right.production
    co2_right = dmu_right.co2
    return _universal_linprog('min',
                              energies,
                              [capitals, labours, productions, co2s],
                              [capital_right, labour_right, production_right, co2_right],
                              ['<=', '<=', '>=', '='], energy_right)
    ''''
    prob = LpProblem('theta_min', LpMinimize)
    variables_count = len(energies)
    ingredients = [str(symbol+1) for symbol in range(variables_count)]
    symbols = LpVariable.dict('x_%s', ingredients, lowBound=0)
    cost = dict(zip(ingredients, energies))
    prob += lpSum([cost[i] * symbols[i] for i in ingredients])
    capital_dict = dict(zip(ingredients, capitals))
    labour_dict = dict(zip(ingredients, labours))
    production_dict = dict(zip(ingredients, productions))
    co2s_dict = dict(zip(ingredients, co2s))
    # constraint
    prob += lpSum([capital_dict[i] * symbols[i]
                   for i in ingredients]) <= capital_right
    prob += lpSum([labour_dict[i] * symbols[i]
                   for i in ingredients]) <= labour_right
    prob += lpSum([production_dict[i] * symbols[i]
                   for i in ingredients]) >= production_right
    prob += lpSum([co2s_dict[i] * symbols[i]
                   for i in ingredients]) == co2_right
    if prob.solve() != 1:
        logging.error('theta min unsolved situation occurs')
        raise UserWarning
    else:
        return prob.objective.value() / energy_right
    '''

@_reciprocal
def theta_min(dmus_s, dmus_right):
    '''
    theta min
    '''
    energies = []
    capitals = []
    labours = []
    producitons = []
    co2s = []
    for dmus in dmus_s:
        for dmu in dmus:
            energies.append(dmu.energy)
            capitals.append(dmu.capital)
            labours.append(dmu.labour)
            producitons.append(dmu.production)
            co2s.append(dmu.co2)
    _add_elements(energies, 1.0)
    _add_elements(capitals, 0.0)
    _add_elements(labours, 0.0)
    _add_elements(producitons, 0.0)
    _add_elements(co2s, 0.0)
    result = []
    for dmu in dmus_right:
        try:
            result.append(_theta_min(energies, capitals,
                                     labours, producitons, co2s, dmu))
        except UserWarning:
            result.append(-1.0)
    return result

def _eta_max(energies, capitals, labours, productions, co2s,
             dmu_right):
    '''
    eta max
    '''
    energy_right = dmu_right.energy
    capital_right = dmu_right.capital
    labour_right = dmu_right.labour
    production_right = dmu_right.production
    co2_right = dmu_right.co2
    return _universal_linprog('max',
                              productions,
                              [energies, capitals, labours, co2s],
                              [energy_right, capital_right, labour_right, co2_right],
                              ['<=', '<=', '<=', '='],
                              production_right)
    '''
    prob = LpProblem('eta_max', LpMaximize)
    variables_count = len(productions)
    ingredients = [str(symbol+1) for symbol in range(variables_count)]
    symbols = LpVariable.dict('x_%s', ingredients, lowBound=0)
    cost = dict(zip(ingredients, productions))
    prob += lpSum([cost[i] * symbols[i] for i in ingredients])
    energy_dict = dict(zip(ingredients, energies))
    capital_dict = dict(zip(ingredients, capitals))
    labour_dict = dict(zip(ingredients, labours))
    co2s_dict = dict(zip(ingredients, co2s))
    #constraint
    prob += lpSum([energy_dict[i] * symbols[i]
                   for i in ingredients]) <= energy_right
    prob += lpSum([capital_dict[i] * symbols[i]
                   for i in ingredients]) <= capital_right
    prob += lpSum([labour_dict[i] * symbols[i]
                   for i in ingredients]) <= labour_right
    prob += lpSum([co2s_dict[i] * symbols[i]
                   for i in ingredients]) == co2_right
    if prob.solve() != 1:
        logging.error('theta min unsolved situation occurs')
        raise UserWarning
    else:
        return prob.objective.value() / production_right
    '''

@_reciprocal
def eta_max(dmus_s, dmus_right):
    '''
    eta max
    '''
    energies = []
    capitals = []
    labours = []
    producitons = []
    co2s = []
    for dmus in dmus_s:
        for dmu in dmus:
            energies.append(dmu.energy)
            capitals.append(dmu.capital)
            labours.append(dmu.labour)
            producitons.append(dmu.production)
            co2s.append(dmu.co2)
    _add_elements(energies, 0.0)
    _add_elements(capitals, 0.0)
    _add_elements(labours, 0.0)
    _add_elements(producitons, -1.0)
    _add_elements(co2s, 0.0)
    result = []
    for dmu in dmus_right:
        try:
            result.append(_eta_max(energies, capitals,
                                   labours, producitons, co2s, dmu))
        except UserWarning:
            result.append(-1.0)
    return result

def _lambda_min(energies, capitals, labours, productions, co2s,
                dmu_right):
    '''
    lambda min
    '''
    energy_right = dmu_right.energy
    capital_right = dmu_right.capital
    labour_right = dmu_right.labour
    production_right = dmu_right.production
    co2_right = dmu_right.co2
    return _universal_linprog('min',
                              co2s,
                              [energies, capitals, labours, productions],
                              [energy_right, capital_right, labour_right, production_right],
                              ['<=', '<=', '<=', '>='],
                              co2_right)
    '''
    prob = LpProblem('lambda_min', LpMinimize)
    variables_count = len(co2s)
    ingredients = [str(symbol+1) for symbol in range(variables_count)]
    symbols = LpVariable.dict('x_%s', ingredients, lowBound=0)
    cost = dict(zip(ingredients, co2s))
    prob += lpSum([cost[i] * symbols[i] for i in ingredients])
    energy_dict = dict(zip(ingredients, energies))
    capital_dict = dict(zip(ingredients, capitals))
    labour_dict = dict(zip(ingredients, labours))
    production_dict = dict(zip(ingredients, productions))
    # constraint
    prob += lpSum([energy_dict[i] * symbols[i]
                   for i in ingredients]) <= energy_right
    prob += lpSum([capital_dict[i] * symbols[i]
                   for i in ingredients]) <= capital_right
    prob += lpSum([labour_dict[i] * symbols[i]
                   for i in ingredients]) <= labour_right
    prob += lpSum([production_dict[i] * symbols[i]
                   for i in ingredients]) >= production_right
    if prob.solve() != 1:
        logging.error('theta min unsolved situation occurs')
        raise UserWarning
    else:
        return prob.objective.value() / co2_right
    '''
@_reciprocal
def lambda_min(dmus_s, dmus_right):
    '''
    lanbda min
    '''
    energies = []
    capitals = []
    labours = []
    producitons = []
    co2s = []
    for dmus in dmus_s:
        for dmu in dmus:
            energies.append(dmu.energy)
            capitals.append(dmu.capital)
            labours.append(dmu.labour)
            producitons.append(dmu.production)
            co2s.append(dmu.co2)
    result = []
    for dmu in dmus_right:
        try:
            result.append(_lambda_min(energies, capitals,
                                      labours, producitons, co2s, dmu))
        except UserWarning:
            result.append(-1.0)
    return result
