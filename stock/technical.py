"""
技术面
"""

import gevent

import stock.tu_wrap as ts
import pandas as pd

from gevent.pool import Group

MARGIN_COLUMNS = ['融资余额(元)', '融资买入额(元)', '融券余量', '融券卖出量']


def _get_sz_margin_details(date, output_list):
    """
    获取某天的融资融券明细列表
    Parameters
    --------
    date:string
                日期 format：YYYY-MM-DD
    output_list:list
                存放结果
    Return
    ------
    None
    """
    output_list.append(ts.sz_margin_details(date=date))


def get_margin_details(code, start, end):
    """
    获取融资融券明细列表
    Parameters
    --------
    code：string
                股票代码, e.g.600728
    start:string
                开始日期 format：YYYY-MM-DD
    end:string
                结束日期 format：YYYY-MM-DD
    Return
    ------
    DataFrame
    """
    sh_details = ts.sh_margin_details(start=start, end=end)

    sz_list = list()
    group = Group()
    for date in sh_details['opDate'].drop_duplicates():
        group.add(gevent.spawn(_get_sz_margin_details, date, sz_list))
    group.join()
    sz_details = pd.concat(sz_list)

    details = pd.concat([
        sh_details[['opDate', 'stockCode', 'rzye', 'rzmre', 'rqyl', 'rqmcl']],
        sz_details[['opDate', 'stockCode', 'rzye', 'rzmre', 'rqyl', 'rqmcl']]
    ])

    detail = details.where(details['stockCode'] == code).dropna().drop(
        ['stockCode'], axis=1).set_index('opDate')
    detail.columns = MARGIN_COLUMNS
    return detail


def _get_one_tick_data(code, date, output_list):
    """
    获取某天的分笔数据
    Parameters
    --------
    code：string
                股票代码, e.g.600728
    date:string
                日期 format：YYYY-MM-DD
    output_list:list
                存放结果
    Return
    ------
    None
    """
    output_list.append(ts.get_tick_data(code, date))

def get_tick_data(code, start, end):
    """
    获取分笔数据
    Parameters
    --------
    code：string
                股票代码, e.g.600728
    start:string
                开始日期 format：YYYY-MM-DD
    end:string
                结束日期 format：YYYY-MM-DD
    Return
    ------
    DataFrame
    """
    data_list = list()
    group = Group()
    for date in pd.date_range(start, end):
        group.add(gevent.spawn(_get_one_tick_data, code, str(date)[:10], data_list))
    group.join()
    tick_data = pd.concat(data_list)
