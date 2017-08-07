"""
基本面
"""

import pandas as pd
from stock import get_balance_sheet, get_profit_statement


def _int_to_year(year):
    """
        转换年份为年报时间
    Parameters
    ------
        year:int
                年份
    return
    ------
        datetime64[ns]
    """
    return pd.to_datetime('%s-12-31' % year)


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
    this_year = _int_to_year(year)
    last_year = _int_to_year(year - 1)
    comparisions = _get_growth_rate(annual_report[this_year],
                                    annual_report[last_year])
    return pd.concat([annual_report[this_year], comparisions])


def get_quarterly_results(code, year=2016, measure='YoY'):
    """
        获取季报
    Parameters
    ------
        code:string
                股票代码 e.g. 002356
        year:int
                年份
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
        this_quarter = _int_to_quarter(year)
        last_quarter = _int_to_quarter(year - 1)
    elif measure is 'QoQ':
        this_quarter = _int_to_quarter(year)
        last_quarter = _int_to_quarter(year - 1)
    else:
        raise TypeError('measure input error.')

    comparisions = _get_growth_rate(quarterly_results[this_quarter],
                                    quarterly_results[last_quarter])
    return
