# -*- encoding:utf-8 -*-
from collections import Iterable
import logging
import itertools
from pulp import LpProblem, lpSum, LpVariable, LpMinimize, LpMaximize


def _add_elements(seq, *elements):
    for element in elements:
        seq.append(element)


def _reciprocal(func):
    def _wrapper(*args, **kw):
        result = func(*args, **kw)
        if isinstance(result, Iterable):
            return [1.0 / x for x in result]
        else:
            return 1.0 / result

    return _wrapper


def _energy_min(energies, capitals, productions, turn_overs, co2s, dmu_right):
    energy_right = dmu_right.energy.total
    capital_right = dmu_right.capital.capital
    production_right = dmu_right.production.production
    turn_over_right = dmu_right.turn_over.turn_over
    co2_right = dmu_right.co2.total
    prob = LpProblem("lambda_min", LpMinimize)
    variables_count = len(energies)
    ingredients = [str(symbols + 1) for symbols in range(variables_count)]
    symbols = LpVariable.dict("x_%s", ingredients, lowBound=0)
    cost = dict(zip(ingredients, energies))
    prob += lpSum([cost[i] * symbols[i] for i in ingredients])
    capital_dict = dict(zip(ingredients, capitals))
    turn_over_dict = dict(zip(ingredients, turn_overs))
    production_dict = dict(zip(ingredients, productions))
    co2_dict = dict(zip(ingredients, co2s))
    prob += lpSum([capital_dict[i] * symbols[i]
                   for i in ingredients]) <= capital_right
    prob += lpSum([turn_over_dict[i] * symbols[i]
                   for i in ingredients]) >= turn_over_right
    prob += lpSum([production_dict[i] * symbols[i]
                   for i in ingredients]) >= production_right
    prob += lpSum([co2_dict[i] * symbols[i]
                   for i in ingredients]) == co2_right
    if prob.solve() != 1:
        logging.error("psi minimize unsolved situation")
        raise UserWarning
    else:
        values = prob.objective.value()
        return values / energy_right


@_reciprocal
def contemporaneous_energy_min(dmus, dmu_right):
    energies = [dmu.energy.total for dmu in dmus]
    capitals = [dmu.capital.capital for dmu in dmus]
    turn_overs = [dmu.turn_over.turn_over for dmu in dmus]
    productions = [dmu.production.production for dmu in dmus]
    co2s = [dmu.co2.total for dmu in dmus]
    return _energy_min(energies, capitals, productions, turn_overs, co2s, dmu_right)


@_reciprocal
def global_energy_min(dmus_s, *dmus_right):
    energies = list(itertools.chain.from_iterable([[dmu.energy.total for dmu in dmus]
                                                   for dmus in dmus_s]))
    capitals = list(itertools.chain.from_iterable([[dmu.capital.capital for dmu in dmus]
                                                   for dmus in dmus_s]))
    turn_overs = list(itertools.chain.from_iterable([[dmu.turn_over.turn_over for dmu in dmus]
                                                     for dmus in dmus_s]))
    productions = list(itertools.chain.from_iterable([[dmu.production.production for dmu in dmus]
                                                      for dmus in dmus_s]))
    co2s = list(itertools.chain.from_iterable([[dmu.co2.total for dmu in dmus]
                                               for dmus in dmus_s]))
    result = []
    for dmu_right in dmus_right:
        result.append(_energy_min(energies, capitals, productions, turn_overs, co2s, dmu_right))
    return result


def _production_max(energies, capitals, productions, turn_overs, co2s, dmu_right):
    energy_right = dmu_right.energy.total
    capital_right = dmu_right.capital.capital
    turn_over_right = dmu_right.turn_over.turn_over
    production_right = dmu_right.production.production
    co2_right = dmu_right.co2.total
    prob = LpProblem("eta max", LpMaximize)
    variables_count = len(productions)
    ingredients = [str(symbol + 1) for symbol in range(variables_count)]
    symbols = LpVariable.dict('x_%s', ingredients, lowBound=0)
    cost = dict(zip(ingredients, productions))
    prob += lpSum([cost[i] * symbols[i] for i in ingredients])
    energy_dict = dict(zip(ingredients, energies))
    capital_dict = dict(zip(ingredients, capitals))
    turn_over_dict = dict(zip(ingredients, turn_overs))
    co2_dict = dict(zip(ingredients, co2s))
    prob += lpSum([energy_dict[i] * symbols[i]
                   for i in ingredients]) <= energy_right
    prob += lpSum([capital_dict[i] * symbols[i]
                   for i in ingredients]) <= capital_right
    prob += lpSum([turn_over_dict[i] * symbols[i]
                   for i in ingredients]) >= turn_over_right
    prob += lpSum([co2_dict[i] * symbols[i]
                   for i in ingredients]) == co2_right
    if prob.solve() != 1:
        logging.error("eta max unsolved situation")
        raise UserWarning
    else:
        return prob.objective.value() / production_right


@_reciprocal
def contemporaneous_production_max(dmus, dmu_right):
    energies = [dmu.energy.total for dmu in dmus]
    capitals = [dmu.capital.capital for dmu in dmus]
    turn_overs = [dmu.turn_over.turn_over for dmu in dmus]
    productions = [dmu.production.production for dmu in dmus]
    co2s = [dmu.co2.total for dmu in dmus]
    return _production_max(energies, capitals, productions, turn_overs, co2s, dmu_right)


@_reciprocal
def global_production_max(dmus_s, *dmus_right):
    energies = list(itertools.chain.from_iterable([[dmu.energy.total for dmu in dmus]
                                                   for dmus in dmus_s]))
    capitals = list(itertools.chain.from_iterable([[dmu.capital.capital for dmu in dmus]
                                                   for dmus in dmus_s]))
    turn_overs = list(itertools.chain.from_iterable([[dmu.turn_over.turn_over for dmu in dmus]
                                                     for dmus in dmus_s]))
    productions = list(itertools.chain.from_iterable([[dmu.production.production for dmu in dmus]
                                                      for dmus in dmus_s]))
    co2s = list(itertools.chain.from_iterable([[dmu.co2.total for dmu in dmus]
                                               for dmus in dmus_s]))
    result = []
    for dmu_right in dmus_right:
        result.append(_production_max(energies, capitals, productions, turn_overs, co2s, dmu_right))
    return result
