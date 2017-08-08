"""
基本面
"""

import pandas as pd
from stock import get_balance_sheet, get_profit_statement

REPORT_COLUMNS = ['本期数(万元)', '增长率(%)']
REPORT_INDEX = [
    '净利润', '销售额', '现金', '存货', '流动资产', '非流动资产', '应收账款', '应付账款', '流动负债', '非流动负债',
    '所有债务'
]

REPORT_PICK_INDEX = [
    '净利润(万元)', '营业收入(万元)', '货币资金(万元)', '存货(万元)', '流动资产合计(万元)', '流动资产合计(万元)',
    '应收账款(万元)', '应付账款(万元)', '流动负债合计(万元)', '非流动负债合计(万元)', '负债合计(万元)'
]


def _to_year(year):
    """
        转换为年报时间
    Parameters
    ------
        year:int
                年份
    return
    ------
        datetime64[ns]
    """
    return pd.to_datetime('%s-12-31' % year)


def _to_quarter(year, quarter):
    """
        转换为季报时间
    Parameters
    ------
        year:int
                年份
        quarter:int
                季度
    return
    ------
        datetime64[ns]
    """
    dt = {1: '-03-31', 2: '-06-30', 3: '-09-30', 4: '-12-31'}
    return pd.to_datetime('%s%s' % (year, dt[quarter]))


def _get_growth_rate(this, last):
    """
        计算增长率
    Parameters
    ------
        this:float
                期末
        last:float
                期初
    return
    ------
        float
    """
    return round((this - last) / last * 100, 2)


def _trim_report(full_report):
    """
        裁剪&标准化报表
    Parameters
    ------
        full_report:DataFrame
                原始报表
    return
    ------
        DataFrame
    """
    full_report.columns = REPORT_COLUMNS
    full_report = full_report.loc[REPORT_PICK_INDEX]
    full_report.index = REPORT_INDEX
    return full_report


def get_annual_report(code, year=2016):
    """
        获取年报
    Parameters
    ------
        code:string
                股票代码 e.g. 002356
        year:int
                年份
    return
    ------
        DataFrame
    """
    annual_report = pd.concat(
        [get_balance_sheet(code),
         get_profit_statement(code)])
    this_year = _to_year(year)
    last_year = _to_year(year - 1)
    comparisions = _get_growth_rate(annual_report[this_year],
                                    annual_report[last_year])
    annual_report = pd.concat([annual_report[this_year], comparisions], axis=1)

    return _trim_report(annual_report)


def get_quarterly_results(code, year=2016, quarter=4, measure='YoY'):
    """
        获取季报
    Parameters
    ------
        code:string
                股票代码 e.g. 002356
        year:int
                年份
        quarter:int
                季度
        measure:string, 默认 'YoY'
                'YoY'：同比
                'QoQ': 环比
    return
    ------
        DataFrame
    """
    quarterly_results = pd.concat([
        get_balance_sheet(code, annual=False),
        get_profit_statement(code, annual=False)
    ])
    if measure is 'YoY':
        this_quarter = _to_quarter(year, quarter)
        last_quarter = _to_quarter(year - 1, quarter)
    elif measure is 'QoQ':
        if quarter is 1:
            this_quarter = _to_quarter(year, quarter)
            last_quarter = _to_quarter(year - 1, 4)
        else:
            this_quarter = _to_quarter(year, quarter)
            last_quarter = _to_quarter(year, quarter - 1)
    else:
        raise TypeError('measure input error.')

    comparisions = _get_growth_rate(quarterly_results[this_quarter],
                                    quarterly_results[last_quarter])
    quarterly_results = pd.concat(
        [quarterly_results[this_quarter], comparisions], axis=1)

    return _trim_report(quarterly_results)
