"""
分离gevent
这里面放置的为需要借助gevent的协程来下载的非一次性数据
"""

import gevent

from gevent.pool import Group

import pandas as pd

from stock.technical import get_sh_margin_details, get_sz_margin_details, get_tick_data


def _load_sz_margin_details(date, output_list):
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
    output_list.append(get_sz_margin_details(date=date))


def load_margin_details(code, start, end):
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
    sh_details = get_sh_margin_details(start=start, end=end)

    sz_list = list()
    group = Group()
    for date in sh_details['日期'].drop_duplicates():
        group.add(gevent.spawn(_load_sz_margin_details, date, sz_list))
    group.join()

    if len(sz_list) == 0:
        return sh_details

    sz_details = pd.concat(sz_list)
    details = pd.concat([sh_details, sz_details])

    return details


def _load_one_tick_data(code, date, output_list):
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
    tick_data = get_tick_data(code=code, date=date)
    output_list.append(tick_data)


def load_tick_data(code, start, end):
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
        group.add(
            gevent.spawn(_load_one_tick_data, code, str(date)[:10], data_list))
    group.join()
    tick_data = pd.concat(data_list)
    tick_data.sort_values(['时间'], ascending=True, inplace=True)
    tick_data.index = range(len(tick_data))
    return tick_data
