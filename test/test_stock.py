"""
stock unittest
"""

import unittest
import pandas as pd

from stock import get_balance_sheet, get_profit_statement
from stock import get_annual_report, get_quarterly_results
from stock import get_basic_info, get_level0_report
from stock.website import BALANCE_SHEET_INDEX, PROFIT_STATEMENT_INDEX
from stock.fundamental import ANNUAL_REPORT_INDEX, ANNUAL_REPORT_COLUMNS
from stock.fundamental import BASIC_REPORT_INDEX, LEVEL0_REPORT_INDEX


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
            self.assertEqual(annual_report.index.tolist(), ANNUAL_REPORT_INDEX)
            self.assertEqual(annual_report.columns.tolist(),
                             ANNUAL_REPORT_COLUMNS)

    def test_get_quarterly_results(self):
        """
        测试季报表
        """
        for quarter in range(1, 4):
            quarterly_results = get_quarterly_results('002367', 2016, quarter,
                                                      'YoY')
            self.assertTrue(isinstance(quarterly_results, pd.DataFrame))
            self.assertEqual(quarterly_results.index.tolist(),
                             ANNUAL_REPORT_INDEX)
            self.assertEqual(quarterly_results.columns.tolist(),
                             ANNUAL_REPORT_COLUMNS)

            quarterly_results = get_quarterly_results('002367', 2016, quarter,
                                                      'QoQ')
            self.assertTrue(isinstance(quarterly_results, pd.DataFrame))
            self.assertEqual(quarterly_results.index.tolist(),
                             ANNUAL_REPORT_INDEX)
            self.assertEqual(quarterly_results.columns.tolist(),
                             ANNUAL_REPORT_COLUMNS)

    def test_get_basic_info(self):
        """
        测试基本信息
        """
        basic_report = get_basic_info('002367')
        self.assertTrue(isinstance(basic_report, pd.Series))
        self.assertEqual(basic_report.index.tolist(), BASIC_REPORT_INDEX)

    def test_get_level0_report(self):
        """
        测试level0分析
        """
        annual_report = get_annual_report('002367')
        level0_report = get_level0_report(annual_report)
        self.assertTrue(isinstance(level0_report, pd.Series))
        self.assertEqual(level0_report.index.tolist(), LEVEL0_REPORT_INDEX)
