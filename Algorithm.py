# -*- coding:utf8 -*-
'''
linear programming
lambda min
theta max
'''
from __future__ import division
import logging
from pulp import LpProblem, lpSum, LpVariable, LpMinimize, LpMaximize

def addelements(sequence, *elements):
    '''
    add elements into list
    '''
    for element in elements:
        sequence.append(element)


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
    return prob.objective.value() / energy_right


def lambda_min(dmus_s, dmus_right):
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
    # add slack varibales
    addelements(energies, 1.0, 0.0)
    addelements(productions, 0.0, 0.0)
    addelements(co2s, 0.0, -1.0)
    result = []
    for dmu in dmus_right:
        try:
            result.append(_lambda_min(energies, productions, co2s,
                                      dmu.ene.total, dmu.pro.production, dmu.co2.total))
        except UserWarning:
            logging.error("unsolve occurs")
            result.append(-1.0)
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


def theta_max(dmus_s, dmus_right):
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
    addelements(energies, 0, -1.0)
    addelements(productions, -1.0, 0.0)
    addelements(co2s, 0.0, 0.0)
    result = []
    for dmu in dmus_right:
        try:
            result.append(_theta_max(energies, productions, co2s,
                                     dmu.ene.total, dmu.pro.production, dmu.co2.total))
        except UserWarning:
            logging.error("unsolve occurs")
            result.append(-1.0)
    return result
    