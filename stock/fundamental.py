"""
基本面
"""

import numpy as np
import pandas as pd
import stock.tu_wrap as ts

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

LEVEL_REPORT_DICT = {
    '存货大于收入': '现金流量',
    '应收账款大于销售额': '营运能力',
    '应付账款大于收入': '营运能力',
    '流动负债大于流动资产': '偿债能力',
    '利润偿还非流动负债': '偿债能力',
    '利润偿还所有负债': '偿债能力',
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
    history = ts.get_k_data(code)
    history.set_index(['date'], inplace=True)
    history.sort_index(inplace=True)
    basic_report = pd.Series(
        {
            '股票代码': code,
            '名称': basic.loc['name'],
            '行业': basic.loc['industry'],
            '最新价': history['close'][-1],
            '市值(亿)': basic.loc['outstanding'] * history['close'][-1],
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
