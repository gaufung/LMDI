# -*- encoding:utf-8 -*-
class Energy(object):
    def __init__(self, name, energy):
        self._name = name
        self._energy = energy
        self._total = sum(energy)

    @property
    def name(self):
        return self._name

    @property
    def energy(self):
        return self._energy

    @property
    def total(self):
        return self._total

    def __len__(self):
        return len(self._energy)

    def __getitem__(self, index):
        assert index < len(self)
        return self._energy[index]

    def __setitem__(self, index, value):
        assert index < len(self)
        self._energy[index] = value


class Capital(object):
    def __init__(self, name, capital):
        self._name = name
        self._capital = capital

    @property
    def name(self):
        return self._name

    @property
    def capital(self):
        return self._capital


class Co2(object):
    def __init__(self, name, co2):
        self._name = name
        self._co2 = co2
        self._total = sum(co2)

    @property
    def name(self):
        return self._name

    @property
    def co2(self):
        return self._co2

    @property
    def total(self):
        return self._total

    def __len__(self):
        return len(self._co2)

    def __getitem__(self, index):
        return self._co2[index]

    def __setitem__(self, index, value):
        self._co2[index] = value


class Production(object):
    def __init__(self, name, production):
        self._name = name
        self._production = production

    @property
    def name(self):
        return self._name

    @property
    def production(self):
        return self._production


class TurnOver(object):
    def __init__(self, name, turn_over):
        self._name = name
        self._turn_over = turn_over

    @property
    def name(self):
        return self._name

    @property
    def turn_over(self):
        return self._turn_over


class Dmu(object):

    def __init__(self, energy, capital, production, co2, turn_over):
        self._energy = energy
        self._capital = capital
        self._production = production
        self._co2 = co2
        self._turn_over = turn_over

    @property
    def energy(self):
        return self._energy

    @property
    def capital(self):
        return self._capital

    @property
    def production(self):
        return self._production

    @property
    def co2(self):
        return self._co2

    @property
    def turn_over(self):
        return self._turn_over

    @property
    def name(self):
        return self._capital.name

    @property
    def energy_count(self):
        return len(self._energy)
