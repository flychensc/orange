"""
基本面
"""

import numpy as np
import pandas as pd
import tushare as ts

from stock import get_balance_sheet, get_profit_statement

ANNUAL_REPORT_INDEX = {
    "raw": [
        '净利润(万元)', '营业收入(万元)', '货币资金(万元)', '存货(万元)', '流动资产合计(万元)',
        '非流动资产合计(万元)', '应收账款(万元)', '应付账款(万元)', '流动负债合计(万元)', '非流动负债合计(万元)',
        '负债合计(万元)'
    ],
    "new": [
        '净利润', '销售额', '现金', '存货', '流动资产', '非流动资产', '应收账款', '应付账款', '流动负债',
        '非流动负债', '所有债务'
    ]
}

BASIC_REPORT_INDEX = ['股票代码', '名称', '行业', '最新价', '市值(亿)', '市盈率', '市净率', '每股收益']
LEVEL0_REPORT_INDEX = [
    '存货大于收入', '应收账款大于销售额', '应付账款大于收入', '流动负债大于流动资产', '利润偿还非流动负债', '利润偿还所有负债'
]
LEVEL1_REPORT_INDEX = [
    '净资产收益率(%)', '净利率(%)', '每股主营业务收入(元)', '应收账款周转率(次)', '存货周转率(次)',
    '流动资产周转率(次)', '主营业务收入增长率(%)', '净利润增长率(%)', '每股收益增长率', '流动比率', '速动比率',
    '现金比率', '利息支付倍数', '资产的经营现金流量回报率', '经营现金净流量与净利润的比率', '经营现金净流量对负债比率',
    '现金流量比率'
]

LEVEL_REPORT_DICT = {
    '存货大于收入': '现金流量',
    '应收账款大于销售额': '营运能力',
    '应付账款大于收入': '营运能力',
    '流动负债大于流动资产': '偿债能力',
    '利润偿还非流动负债': '偿债能力',
    '利润偿还所有负债': '偿债能力',
    #'分配方案': '业绩报告',
    '净资产收益率(%)': '盈利能力',
    '净利率(%)': '盈利能力',
    '每股主营业务收入(元)': '盈利能力',
    '应收账款周转率(次)': '营运能力',
    '存货周转率(次)': '营运能力',
    '流动资产周转率(次)': '营运能力',
    '主营业务收入增长率(%)': '成长能力',
    '净利润增长率(%)': '成长能力',
    '每股收益增长率': '成长能力',
    '流动比率': '偿债能力',
    '速动比率': '偿债能力',
    '现金比率': '偿债能力',
    '利息支付倍数': '偿债能力',
    '资产的经营现金流量回报率': '现金流量',
    '经营现金净流量与净利润的比率': '现金流量',
    '经营现金净流量对负债比率': '现金流量',
    '现金流量比率': '现金流量',
}


def get_annual_report(code):
    """
        获取年报
    Parameters
    ------
        code:string
                股票代码 e.g. 002356
    return
    ------
        DataFrame
    """
    annual_report = pd.concat(
        [get_balance_sheet(code),
         get_profit_statement(code)])

    annual_report = annual_report.loc[ANNUAL_REPORT_INDEX["raw"]]
    annual_report.index = ANNUAL_REPORT_INDEX["new"]
    return annual_report.sort_index(axis=1)


def get_quarterly_results(code):
    """
        获取季报
    Parameters
    ------
        code:string
                股票代码 e.g. 002356
    return
    ------
        DataFrame
    """
    quarterly_results = pd.concat([
        get_balance_sheet(code, annual=False),
        get_profit_statement(code, annual=False)
    ])

    quarterly_results = quarterly_results.loc[ANNUAL_REPORT_INDEX["raw"]]
    quarterly_results.index = ANNUAL_REPORT_INDEX["new"]
    return quarterly_results.sort_index(axis=1)


def get_basic_info(code):
    """
        上市公司基本信息
    Parameters
    ------
        code:string
    return
    ------
        Series
    """
    basic = ts.get_stock_basics().loc[code]
    #获取连接备用
    cons = ts.get_apis()
    history = ts.bar(code, conn=cons, adj='qfq')
    #释放，否则python无法正常退出
    ts.close_apis(cons)
    basic_report = pd.Series(
        {
            '股票代码': code,
            '名称': basic.loc['name'],
            '行业': basic.loc['industry'],
            '最新价': history['close'][0],
            '市值(亿)': basic.loc['outstanding'] * history['close'][0],
            '市盈率': basic.loc['pe'],
            '市净率': basic.loc['pb'],
            '每股收益': basic.loc['esp'],
        },
        index=BASIC_REPORT_INDEX)
    return basic_report


def get_level0_report(annual_report):
    """
        Level0基本面分析
    Parameters
    ------
        annual_report:Series
                年报表、季报表
    return
    ------
        Series
    """
    data_series = annual_report

    _is_larger_to_str = lambda a, b, msg: msg if a > b else "正常"
    _calc_ratio_to_str = lambda d, r: str(round(d / r, 2))

    level0_report = pd.Series(
        {
            '存货大于收入':
            _is_larger_to_str(data_series['存货'], data_series['销售额'],
                              '警告信号: 销售量下降'),
            '应收账款大于销售额':
            _is_larger_to_str(data_series['应收账款'], data_series['销售额'],
                              '出现问题: 货卖了，收不了款'),
            '应付账款大于收入':
            _is_larger_to_str(data_series['应付账款'], data_series['销售额'],
                              '出现问题: 货卖了，赚不了钱'),
            '流动负债大于流动资产':
            _is_larger_to_str(data_series['流动负债'], data_series['流动资产'],
                              '出现麻烦: 无法偿还贷款'),
            '利润偿还非流动负债':
            _calc_ratio_to_str(data_series['非流动负债'], data_series['净利润']),
            '利润偿还所有负债':
            _calc_ratio_to_str(data_series['所有债务'], data_series['净利润']),
        },
        index=LEVEL0_REPORT_INDEX)
    return level0_report


def get_level1_report(code, year, quarter):
    """
        Level1基本面分析
    Parameters
    ------
        code:string
        year:int
        quarter:int
    return
    ------
        Series
    """
    #report_data = ts.get_report_data(year, quarter).set_index(['code'])
    profit_data = ts.get_profit_data(year, quarter).set_index(['code'])
    operation_data = ts.get_operation_data(year, quarter).set_index(['code'])
    growth_data = ts.get_growth_data(year, quarter).set_index(['code'])
    debtpaying_data = ts.get_debtpaying_data(year, quarter).set_index(['code'])
    cashflow_data = ts.get_cashflow_data(year, quarter).set_index(['code'])

    #report_data[['name', 'distrib']]
    level1_report = profit_data[['roe', 'net_profit_ratio', 'bips']].merge(
        operation_data[[
            'arturnover', 'inventory_turnover', 'currentasset_turnover'
        ]],
        left_index=True,
        right_index=True).merge(
            growth_data[['mbrg', 'nprg', 'epsg']],
            left_index=True,
            right_index=True).merge(
                debtpaying_data[[
                    'currentratio', 'quickratio', 'cashratio', 'icratio'
                ]],
                left_index=True,
                right_index=True).merge(
                    cashflow_data[[
                        'rateofreturn', 'cf_nm', 'cf_liabilities',
                        'cashflowratio'
                    ]],
                    left_index=True,
                    right_index=True)

    level1_report.drop_duplicates(keep='last', inplace=True)
    level1_report.columns = LEVEL1_REPORT_INDEX

    return level1_report.loc[
        code] if code in level1_report.index else pd.Series(
            index=LEVEL1_REPORT_INDEX)


def classifier_level_report(level_report):
    """
        Level report分类
    Parameters
    ------
        level_report:Series
                level report
    return
    ------
        Series
    """
    index1 = [LEVEL_REPORT_DICT[name] for name in level_report.index.tolist()]
    level_report.index = [
        np.array(index1),
        np.array(level_report.index.tolist())
    ]
    return level_report


def pct_change(data_report, periods=1, axis=0):
    """
        财务数据增速
    Parameters
    ------
        data_frame:DataFrame
                annual report
        periods:int
                计算周期
        axis:int
                0:行, 1:列
    return
    ------
        DataFrame
    """
    return data_report.diff(
        periods=periods, axis=axis) / data_report.shift(
            periods=periods, axis=axis).abs()
