# -*- coding:utf8 -*-
'''
linear programming
lambda min
theta max
'''
from __future__ import division
import logging
from pulp import LpProblem, lpSum, LpVariable, LpMinimize, LpMaximize, GLPK, LpStatus,value

def _addelements(sequence, *elements):
    '''
    add elements into list
    '''
    for element in elements:
        sequence.append(element)

def _reciprocal(func):
    def _wrapper(*args, **kw):
        result = func(*args, **kw)
        return [1.0 / x for x in result]
    return _wrapper


def _lambda_min(enengies, productions, co2s, energy_right, production_right, co2_right):
    '''
    _lambda_min
    '''
    # the linear programming objective is minimize
    prob = LpProblem("lambda_min", LpMinimize)
    variablecount = len(enengies)
    ingredients = [str(symbols + 1) for symbols in range(variablecount)]
    # variable symbols such x1, x2, x3 ... xn
    symbols = LpVariable.dict('x_%s', ingredients, lowBound=0)
    cost = dict(zip(ingredients, enengies))
    prob += lpSum([cost[i] * symbols[i] for i in ingredients])
    pro_dict = dict(zip(ingredients, productions))
    co2_dict = dict(zip(ingredients, co2s))
    # linear constraint condition
    prob += lpSum([pro_dict[i] * symbols[i]
                   for i in ingredients]) >= production_right
    prob += lpSum([co2_dict[i] * symbols[i] for i in ingredients]) == co2_right
    if prob.solve() != 1:
        raise UserWarning
    else:
        #varibales = [x.varValue for x in prob.variables()]
        #print varibales
        return prob.objective.value() / energy_right

def _lambda_min_same_year(energies, productions, co2s, dmus_right, is_raise_exception=False):
    '''
    lambda min in same years
    '''
    energies_backup = energies[:]
    productions_backup = productions[:]
    co2s_backup = co2s[:]
    _addelements(energies_backup, 1.0)
    _addelements(productions_backup, 0.0)
    _addelements(co2s_backup, 0.0)
    result = []
    for dmu in dmus_right:
        try:
            result.append(_lambda_min(energies_backup, productions_backup, co2s_backup,
                                      dmu.ene.total, dmu.pro.production, dmu.co2.total))
        except UserWarning:
            if is_raise_exception:
                logging.error("unsolve occurs")
                raise Exception
            else:
                result.append(-1.0)
    return result
def _lambda_min_different_year(energies, productions, co2s, dmus_right):
    '''
    lambda min in different years
    '''
    energies_backup = energies[:]
    productions_backup = productions[:]
    co2s_backup = co2s[:]
    _addelements(energies_backup, 1.0, 0.0)
    _addelements(productions_backup, 0.0, 0.0)
    _addelements(co2s_backup, 0.0, -1.0)
    result = []
    for dmu in dmus_right:
        try:
            result.append(_lambda_min(energies_backup, productions_backup, co2s_backup,
                                      dmu.ene.total, dmu.pro.production, dmu.co2.total))
        except UserWarning:
            logging.error("unsolve occurs")
            raise Exception
    return result

@_reciprocal
def lambda_min(dmus_s, dmus_right, is_same_year=False):
    '''
    the min of energy
    '''
    energies = []
    productions = []
    co2s = []
    for dmus in dmus_s:
        for dmu in dmus:
            energies.append(dmu.ene.total)
            productions.append(dmu.pro.production)
            co2s.append(dmu.co2.total)
    if is_same_year:
        return _lambda_min_same_year(energies, productions, co2s, dmus_right, False)
    else:
        result = _lambda_min_same_year(energies, productions, co2s, dmus_right, False)
        lambda_differtent = _lambda_min_different_year(energies, productions, co2s, dmus_right)
        for idx, value in enumerate(result):
            if value == -1.0:
                result[idx] = lambda_differtent[idx]
        return result


def _theta_max(enengies, productions, co2s, energy_right, production_right, co2_right):
    '''
    _theta_max
    '''
    # the linear programming objective is maximize
    prob = LpProblem("theta_max", LpMaximize)
    variablecount = len(enengies)
    ingredients = [str(symbols + 1) for symbols in range(variablecount)]
    # the variable symbols  x1, x2, x3 .... xn
    symbols = LpVariable.dict('x_%s', ingredients, lowBound=0)
    cost = dict(zip(ingredients, productions))
    prob += lpSum([cost[i] * symbols[i] for i in ingredients])
    ene_dict = dict(zip(ingredients, enengies))
    co2_dict = dict(zip(ingredients, co2s))
    prob += lpSum([ene_dict[i] * symbols[i]
                   for i in ingredients]) <= energy_right
    prob += lpSum([co2_dict[i] * symbols[i] for i in ingredients]) == co2_right
    if prob.solve() != 1:
        raise UserWarning
    else:
        return prob.objective.value() / production_right

def _theta_max_same_year(energies, productions, co2s, dmus_right, is_raise_exception=False):
    energies_backup = energies[:]
    productions_backup = productions[:]
    co2s_backup = co2s[:]
    _addelements(energies_backup, 0.0)
    _addelements(productions_backup, -1.0)
    _addelements(co2s_backup, 0.0)
    result = []
    for dmu in dmus_right:
        try:
            result.append(_theta_max(energies_backup, productions_backup, co2s_backup,
                                     dmu.ene.total, dmu.pro.production, dmu.co2.total))
        except UserWarning:
            if is_raise_exception:
                logging.error("unsolve occurs")
                raise Exception
            else:
                result.append(-1.0)
    return result
def _theta_max_different_year(energies, productions, co2s, dmus_right):
    energies_backup = energies[:]
    productions_backup = productions[:]
    co2s_backup = co2s[:]
    _addelements(energies_backup, 0.0, -1.0)
    _addelements(productions_backup, -1.0, 0.0)
    _addelements(co2s_backup, 0.0, 0.0)
    result = []
    for dmu in dmus_right:
        try:
            result.append(_theta_max(energies_backup, productions_backup, co2s_backup,
                                     dmu.ene.total, dmu.pro.production, dmu.co2.total))
        except UserWarning:
            logging.error("unsolve occurs")
            raise Exception
    return result

@_reciprocal
def theta_max(dmus_s, dmus_right, is_same_year=False):
    '''
    the production max
    '''
    energies = []
    productions = []
    co2s = []
    for dmus in dmus_s:
        for dmu in dmus:
            energies.append(dmu.ene.total)
            productions.append(dmu.pro.production)
            co2s.append(dmu.co2.total)
    # add slack variables
    if is_same_year:
        return _theta_max_same_year(energies, productions, co2s, dmus_right, True)
    else:
        result = _theta_max_same_year(energies, productions, co2s, dmus_right, False)
        theta_different = _theta_max_different_year(energies, productions, co2s, dmus_right)
        for idx, value in enumerate(result):
            if value == -1.0:
                result[idx] = theta_different[idx]
        return result

def _linear_program(energies, productions, co2s, energy, production, co2):
    # object
    factors1 = []
    for dmu in zip(productions, energies, co2s):
        factors1.append(dmu[0]/production - dmu[1]/energy - dmu[2] / co2)
    _addelements(factors1, -1.0 / energy, -1.0 / production)
    # subject to alpha
    factors2 = [x/energy for x in energies]
    _addelements(factors2, 1.0/energy, 0.0)
    # subject to beta
    factors3 = [x/production for x in productions]
    _addelements(factors3, 0.0, -1.0/production)
    # subject to omega
    factors4 = [x/co2 for x in co2s]
    _addelements(factors4, 0.0, 0.0)

    # start linear_programming
    prob = LpProblem('max', LpMaximize)
    ingredinets = [str(symbols + 1) for symbols in range(len(factors1))]
    symbols = LpVariable.dict('x_%s', ingredinets, lowBound=0)
    cost = dict(zip(ingredinets, factors1))
    prob += lpSum([cost[i] * symbols[i] for i in ingredinets])
    # subject dict
    sub_dict_alpha = dict(zip(ingredinets, factors2))
    sub_dict_beta = dict(zip(ingredinets, factors3))
    sub_dict_omega = dict(zip(ingredinets, factors4))
    prob += lpSum([sub_dict_alpha[i] *symbols[i]
                   for i in ingredinets]) <= 1.0
    prob += lpSum([sub_dict_beta[i] * symbols[i]
                   for i in ingredinets]) >= 1.0
    prob += lpSum([sub_dict_omega[i] * symbols[i]
                   for i in ingredinets]) <= 1.0
    if prob.solve(GLPK(msg=2)) != 1:
        raise UserWarning
    else:
        varibales = {v.name : v.varValue for v in prob.variables()}
        alpha = 1 - sum([sub_dict_alpha[i] * varibales['x_'+str(i)] for i in ingredinets])
        beta = sum([sub_dict_beta[i] * varibales['x_'+str(i)] for i in ingredinets]) - 1
        omega = 1 - sum([sub_dict_omega[i] * varibales['x_'+str(i)] for i in ingredinets])
        #print alpha+beta+omega, prob.objective.value() + 1.0
        return alpha, beta, omega
        #return 0.0, 0.0, 0.0
        #return (prob.objective.value() + 1.0) / 3.0

def linear_program(dmus_left, dmus_right):
    '''
    linear_program
    '''
    energies = [dmu.ene.total for dmu in dmus_left]
    productions = [dmu.pro.production for dmu in dmus_left]
    co2s = [dmu.co2.total for dmu in dmus_left]
    result = []
    for dmu in dmus_right:
        try:
            result.append(_linear_program(energies, productions, co2s,
                          dmu.ene.total, dmu.pro.production, dmu.co2.total))
        except UserWarning:
            result.append((-1.0, -1.0, -1.0))
    return result

# theta_min
def _theta_min(enengies, productions, co2s, energy_right, production_right, co2_right):
    '''
    theta min
    '''
    # the linear programming objective is minimize
    prob = LpProblem('theta_min', LpMinimize)
    variablecount = len(enengies)
    ingredients = [str(symbols+1) for symbols in range(variablecount)]
    # the variable symbols such as x1, x2, x3 ... xn
    symbols = LpVariable.dict('x_%s', ingredients, lowBound=0)
    cost = dict(zip(ingredients, co2s))
    prob += lpSum([cost[i] * symbols[i] for i in ingredients])
    ene_dict = dict(zip(ingredients, enengies))
    pro_dict = dict(zip(ingredients, productions))
    prob += lpSum([ene_dict[i] * symbols[i]
                   for i in ingredients]) <= energy_right
    prob += lpSum([pro_dict[i] * symbols[i]
                   for i in ingredients]) >= production_right
    if prob.solve() != 1:
        raise UserWarning
    return prob.objective.value() / co2_right


@_reciprocal
def theta_min(dmus_s, dmus_right):
    '''
    theta min
    '''
    energies = []
    productions = []
    co2s = []
    for dmus in dmus_s:
        for dmu in dmus:
            energies.append(dmu.ene.total)
            productions.append(dmu.pro.production)
            co2s.append(dmu.co2.total)
    result = []
    for dmu in dmus_right:
        try:
            result.append(_theta_min(energies, productions, co2s,
                                     dmu.ene.total, dmu.pro.production, dmu.co2.total))
        except UserWarning:
            result.append(-1.0)
    return result

