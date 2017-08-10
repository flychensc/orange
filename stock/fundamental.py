"""
基本面
"""

import pandas as pd
import stock.tu_wrap as ts

from stock import get_balance_sheet, get_profit_statement

REPORT_COLUMNS = ['本期数(万元)', '增长率(%)']
REPORT_INDEX = [
    '净利润', '销售额', '现金', '存货', '流动资产', '非流动资产', '应收账款', '应付账款', '流动负债', '非流动负债',
    '所有债务'
]

REPORT_PICK_INDEX = [
    '净利润(万元)', '营业收入(万元)', '货币资金(万元)', '存货(万元)', '流动资产合计(万元)', '非流动资产合计(万元)',
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
    dict_quarter = {1: '-03-31', 2: '-06-30', 3: '-09-30', 4: '-12-31'}
    return pd.to_datetime('%s%s' % (year, dict_quarter[quarter]))


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


def get_basic_info(code):
    """
        上市公司基本信息
    Parameters
    ------
        code:string
    return
    ------
        DataFrame
    """
    basic = ts.get_stock_basics().loc[code]
    history = ts.get_k_data(code)
    history.set_index(['date'], inplace=True)
    history.sort_index(inplace=True)
    basic_report = pd.DataFrame(
        [
            ['股票代码', code],
            ['名称', basic.loc['name']],
            ['行业', basic.loc['industry']],
            ['最新价', history['close'][-1]],
            ['流通股本(亿)', basic.loc['outstanding']],
            ['市盈率', basic.loc['pe']],
            ['市净率', basic.loc['pb']],
            ['每股收益', basic.loc['esp']],
        ],
        columns=['项目', '结果'])
    return basic_report


def get_level0_report(annual_report):
    """
        Level0基本面分析
    Parameters
    ------
        annual_report:DataFrame
                年报表、季报表
    return
    ------
        DataFrame
    """
    data_series = annual_report['本期数(万元)']

    _is_larger_to_str = lambda a, b, msg: msg if a > b else "正常"
    _calc_ratio_to_str = lambda d, r: str(round(d / r, 2))

    level0_report = pd.DataFrame(
        [
            [
                '现金流量',
                '存货大于收入',
                _is_larger_to_str(data_series['存货'], data_series['销售额'],
                                  '警告信号: 销售量下降'),
            ],
            [
                '营运能力',
                '应收账款大于销售额',
                _is_larger_to_str(data_series['应收账款'], data_series['销售额'],
                                  '出现问题: 货卖了，收不了款'),
            ],
            [
                '营运能力',
                '应付账款大于收入',
                _is_larger_to_str(data_series['应付账款'], data_series['销售额'],
                                  '出现问题: 货卖了，赚不了钱'),
            ],
            [
                '偿债能力',
                '流动负债大于流动资产',
                _is_larger_to_str(data_series['流动负债'], data_series['流动资产'],
                                  '出现麻烦: 无法偿还贷款'),
            ],
            [
                '偿债能力',
                '利润偿还非流动负债',
                _calc_ratio_to_str(data_series['非流动负债'], data_series['净利润']),
            ],
            [
                '偿债能力',
                '利润偿还所有负债',
                _calc_ratio_to_str(data_series['所有债务'], data_series['净利润']),
            ],
        ],
        columns=['属性', '项目', '结果'])
    return level0_report.set_index(['属性', '项目'])
