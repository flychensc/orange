"""
stock unittest
"""

import unittest
import pandas as pd

from stock import get_balance_sheet, get_profit_statement, get_annual_report, get_quarterly_results
from stock.website import BALANCE_SHEET_INDEX, PROFIT_STATEMENT_INDEX
from stock.fundamental import REPORT_INDEX, REPORT_COLUMNS


class TestStock(unittest.TestCase):
    """
    测试股票接口
    """

    def test_get_balance_sheet(self):
        """
        测试资产负债表
        """
        balance_sheet = get_balance_sheet('002367')
        self.assertTrue(isinstance(balance_sheet, pd.DataFrame))
        self.assertEqual(balance_sheet.index.tolist(), BALANCE_SHEET_INDEX)
        self.assertEqual(balance_sheet.columns.dtype, 'datetime64[ns]')
        for column_name in balance_sheet.columns:
            self.assertEqual(balance_sheet[column_name].dtype, 'float64')

    def test_get_profit_statement(self):
        """
        测试利润表
        """
        profit_statement = get_profit_statement('002367')
        self.assertTrue(isinstance(profit_statement, pd.DataFrame))
        self.assertEqual(profit_statement.index.tolist(),
                         PROFIT_STATEMENT_INDEX)
        self.assertEqual(profit_statement.columns.dtype, 'datetime64[ns]')
        for column_name in profit_statement.columns:
            self.assertEqual(profit_statement[column_name].dtype, 'float64')

    def test_get_annual_report(self):
        """
        测试年报表
        """
        for year in range(2014, 2016):
            annual_report = get_annual_report('002367', year)
            self.assertTrue(isinstance(annual_report, pd.DataFrame))
            self.assertEqual(annual_report.index.tolist(), REPORT_INDEX)
            self.assertEqual(annual_report.columns.tolist(), REPORT_COLUMNS)

    def test_get_quarterly_results(self):
        """
        测试季报表
        """
        for quarter in range(1, 4):
            quarterly_results = get_quarterly_results('002367', 2016, quarter,
                                                      'YoY')
            self.assertTrue(isinstance(quarterly_results, pd.DataFrame))
            self.assertEqual(quarterly_results.index.tolist(), REPORT_INDEX)
            self.assertEqual(quarterly_results.columns.tolist(),
                             REPORT_COLUMNS)

            quarterly_results = get_quarterly_results('002367', 2016, quarter,
                                                      'QoQ')
            self.assertTrue(isinstance(quarterly_results, pd.DataFrame))
            self.assertEqual(quarterly_results.index.tolist(), REPORT_INDEX)
            self.assertEqual(quarterly_results.columns.tolist(),
                             REPORT_COLUMNS)
