# -*- encoding:utf-8 -*-
import xlrd
from model import Co2, Energy, Production, TurnOver, Capital, Dmu


class ExcelReader(object):
    _LOOKUP_TABLE = {}

    def __init__(self, config):
        self._config = config
        self._fill_lookup_table()

    def _fill_lookup_table(self):
        self._LOOKUP_TABLE = {
            "2006": (self._config.COL_2006, self._config.SHEET_2006),
            "2007": (self._config.COL_2007, self._config.SHEET_2007),
            "2008": (self._config.COL_2008, self._config.SHEET_2008),
            "2009": (self._config.COL_2009, self._config.SHEET_2009),
            "2010": (self._config.COL_2010, self._config.SHEET_2010),
            "2011": (self._config.COL_2011, self._config.SHEET_2011),
            "2012": (self._config.COL_2012, self._config.SHEET_2012),
            "2013": (self._config.COL_2013, self._config.SHEET_2013),
            "2014": (self._config.COL_2014, self._config.SHEET_2014),
        }

    def read_dmus(self, year):
        energies = self._read_energy(year)
        capitals = self._read_capital(year)
        productions = self._read_production(year)
        co2s = self._read_co2(year)
        turn_overs = self._read_turn_over(year)
        return [Dmu(energy, capital, production, co2, turn_over)
                for energy, capital, production, co2, turn_over in
                zip(energies, capitals, productions, co2s, turn_overs)]

    def _read_energy(self, year):
        workbook = xlrd.open_workbook(self._config.XLSX_PATH)
        _, sheet_index = self._LOOKUP_TABLE[year]
        table = workbook.sheets()[sheet_index]
        result = []
        for row_index in range(self._config.ENERGY_ROW_START, self._config.ENERGY_ROW_END + 1):
            row = table.row_values(row_index)
            name = row[self._config.COL_PROVINCE]
            energies = [float(x) for x in row[self._config.COL_START: self._config.COL_END + 1]]
            result.append(Energy(name, energies))
        return result

    def _read_co2(self, year):
        workbook = xlrd.open_workbook(self._config.XLSX_PATH)
        _, sheet_index = self._LOOKUP_TABLE[year]
        table = workbook.sheets()[sheet_index]
        result = []
        for row_index in range(self._config.CO2_ROW_START, self._config.CO2_ROW_END + 1):
            row = table.row_values(row_index)
            name = row[self._config.COL_PROVINCE]
            co2s = [float(x) for x in row[self._config.COL_START: self._config.COL_END + 1]]
            result.append(Co2(name, co2s))
        return result

    def _read_capital(self, year):
        workbook = xlrd.open_workbook(self._config.XLSX_PATH)
        col_index, _ = self._LOOKUP_TABLE[year]
        table = workbook.sheets()[self._config.CAPITAL_SHEET]
        province_names = table.col_values(self._config.COL_PROVINCE)[
                         self._config.HEA_ELE_CAP_TURN_PRO_ROW_START: self._config.HEA_ELE_CAP_TURN_PRO_ROW_END + 1]
        capitals = table.col_values(col_index)[
                   self._config.HEA_ELE_CAP_TURN_PRO_ROW_START: self._config.HEA_ELE_CAP_TURN_PRO_ROW_END + 1]
        return [
            Capital(province_name, capital) for province_name, capital in zip(province_names,
                                                                              capitals)]

    def _read_production(self, year):
        workbook = xlrd.open_workbook(self._config.XLSX_PATH)
        col_index, _ = self._LOOKUP_TABLE[year]
        table = workbook.sheets()[self._config.PRODUCTION_SHEET]
        province_names = table.col_values(self._config.COL_PROVINCE)[
                         self._config.HEA_ELE_CAP_TURN_PRO_ROW_START: self._config.HEA_ELE_CAP_TURN_PRO_ROW_END + 1]
        productions = table.col_values(col_index)[
                      self._config.HEA_ELE_CAP_TURN_PRO_ROW_START: self._config.HEA_ELE_CAP_TURN_PRO_ROW_END + 1]
        return [
            Production(province_name, production) for province_name, production in zip(province_names,
                                                                                       productions)]

    def _read_turn_over(self, year):
        workbook = xlrd.open_workbook(self._config.XLSX_PATH)
        col_index, _ = self._LOOKUP_TABLE[year]
        table = workbook.sheets()[self._config.TURN_OVER_SHEET]
        province_names = table.col_values(self._config.COL_PROVINCE)[
                         self._config.HEA_ELE_CAP_TURN_PRO_ROW_START: self._config.HEA_ELE_CAP_TURN_PRO_ROW_END + 1]
        turn_overs = table.col_values(col_index)[
                     self._config.HEA_ELE_CAP_TURN_PRO_ROW_START: self._config.HEA_ELE_CAP_TURN_PRO_ROW_END + 1]
        return [
            TurnOver(province_name, turn_over) for province_name, turn_over in zip(province_names,
                                                                                   turn_overs)]

    def _read_cef(self, year):
        workbook = xlrd.open_workbook(self._config.XLSX_PATH)
        col_index, _ = self._LOOKUP_TABLE[year]
        # heat
        table = workbook.sheets()[self._config.HEAT_COEFFICIENT]
        heats = table.col_values(col_index)[
               self._config.HEA_ELE_CAP_TURN_PRO_ROW_START: self._config.HEA_ELE_CAP_TURN_PRO_ROW_END + 1]
        # electricity
        table = workbook.sheets()[self._config.ELECTRICITY_COEFFICIENT]
        eccentricities = table.col_values(col_index)[
                      self._config.HEA_ELE_CAP_TURN_PRO_ROW_START: self._config.HEA_ELE_CAP_TURN_PRO_ROW_END + 1]
        cefs = []
        for heat, electricity in zip(heats, eccentricities):
            cef = [self._config.CO2_COEFFICIENT[k] / self._config.STAND_COAL_COEFFICIENT[k]
                   for k in self._config.ENERGY_TYPE_INDEX.keys()]
            cef.append(heat)
            cef.append(electricity)
            cefs.append(cef)
        return cefs

    def read_cef(self, *years):
        return {
            year: self._read_cef(year) for year in years
        }
