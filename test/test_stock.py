"""
stock unittest
"""

import unittest
import pandas as pd
import numpy as np

from stock import get_balance_sheet, get_profit_statement
from stock import get_annual_report, get_quarterly_results
from stock import get_basic_info, get_level0_report, get_level1_report
from stock import classifier_level_report, pct_change
from stock.website import BALANCE_SHEET_INDEX, PROFIT_STATEMENT_INDEX
from stock.fundamental import ANNUAL_REPORT_INDEX, BASIC_REPORT_INDEX, LEVEL0_REPORT_INDEX, LEVEL1_REPORT_INDEX


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
        annual_report = get_annual_report('002367')
        # YoY
        #comparisions = annual_report.pct_change(axis=1)
        self.assertTrue(isinstance(annual_report, pd.DataFrame))
        self.assertEqual(annual_report.index.tolist(),
                         ANNUAL_REPORT_INDEX['new'])
        self.assertEqual(annual_report.columns.dtype, 'datetime64[ns]')
        columns_list = annual_report.columns.tolist()
        columns_list.sort()
        self.assertEqual(annual_report.columns.tolist(), columns_list)

    def test_get_quarterly_results(self):
        """
        测试季报表
        """
        quarterly_results = get_quarterly_results('002367')
        # YoY
        #comparisions = quarterly_results.pct_change(axis=1)
        # QoQ
        #comparisions = quarterly_results.pct_change(periods=4, axis=1)
        self.assertTrue(isinstance(quarterly_results, pd.DataFrame))
        self.assertEqual(quarterly_results.index.tolist(),
                         ANNUAL_REPORT_INDEX['new'])
        self.assertEqual(quarterly_results.columns.dtype, 'datetime64[ns]')
        columns_list = quarterly_results.columns.tolist()
        columns_list.sort()
        self.assertEqual(quarterly_results.columns.tolist(), columns_list)

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
        level0_report = get_level0_report(annual_report.iloc[:, -1])
        self.assertTrue(isinstance(level0_report, pd.Series))
        self.assertEqual(level0_report.index.tolist(), LEVEL0_REPORT_INDEX)

    def test_get_level1_report(self):
        """
        测试level1分析
        """
        level1_report = get_level1_report('002367', 2016, 4)
        self.assertTrue(isinstance(level1_report, pd.Series))
        self.assertEqual(level1_report.index.tolist(), LEVEL1_REPORT_INDEX)

    def test_classifier_level_report(self):
        """
        测试level report分类
        """
        annual_report = get_annual_report('002367')
        level0_report = get_level0_report(annual_report.iloc[:, -1])
        level0_report2 = classifier_level_report(level0_report)
        self.assertTrue(isinstance(level0_report2, pd.Series))

    def test_pct_change(self):
        """
        测试财务增速接口
        """
        quarterly_results = get_quarterly_results('002367')
        quarterly_results.dropna(axis=1, how='any', inplace=True)
        pct_change1 = quarterly_results.pct_change(axis=1)
        pct_change2 = pct_change(quarterly_results, axis=1)
        self.assertTrue(isinstance(pct_change1, pd.DataFrame))
        self.assertTrue(isinstance(pct_change2, pd.DataFrame))
        d1 = pct_change1.abs().round(4)
        d2 = pct_change2.abs().round(4)
        self.assertTrue(d1.equals(d2))
        self.assertFalse(d1.empty)
