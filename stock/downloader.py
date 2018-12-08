"""
分离gevent
这里面放置的为需要借助gevent的协程来下载的非一次性数据
"""

import gevent

from gevent.pool import Group
from gevent.queue import Queue

import socket
import pandas as pd

from stock.technical import (get_sh_margin_details, get_sz_margin_details, 
                            get_tick_data, get_k_data)
from stock.fundamental import get_stock_basics


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


def _load_history_worker(todo_q, result_q, start, end):
    while not todo_q.empty():
        try:
            (retry_count, stock_id) = todo_q.get(timeout=3)
            print("%(stock_id)s try %(retry_count)d times" % locals())
            # 获取历史数据
            his_data = get_k_data(stock_id, start, end)
            # his_data.set_index(["date"], inplace=True)
            result_q.put(his_data)
        except gevent.queue.Empty:
            return
        except socket.timeout:
            print("%(stock_id)s as socket.timeout" % locals())
            todo_q.put((retry_count+1, stock_id))
        except Exception as e:
            print("%(stock_id)s exception as %(e)s" % locals())
        gevent.sleep(0)


def load_historys(start_day, end_day):
    todo_q = Queue()
    # put all stocks' code
    for code in get_stock_basics().index:
        todo_q.put((0, code))
   
    result_q = Queue()
    group = Group()
    # workers
    for i in range(10):
        group.add(gevent.spawn(_load_history_worker,
                               todo_q=todo_q, result_q=result_q,
                               start=start_day, end=end_day))
    group.join()

    # collect history
    his_list = []
    while not result_q.empty():
        his_list.append(result_q.get())
    return his_list
