"""
技术面
"""

import tushare as ts
import pandas as pd

MARGIN_COLUMNS = ['日期', '股票代码', '融资余额(元)', '融资买入额(元)', '融券余量', '融券卖出量']

TICK_COLUMNS = ['时间', '成交价', '成交量', '买卖类型']


def get_sh_margin_details(start, end):
    """
    获取沪市某段时间的融资融券明细列表
    Parameters
    --------
    start:string
                开始日期 format：YYYY-MM-DD
    end:string
                结束日期 format：YYYY-MM-DD
    Return
    ------
    DataFrame
    """
    sh_details = ts.sh_margin_details(start=start, end=end)
    if sh_details.empty:
        return pd.DataFrame(columns=MARGIN_COLUMNS)
    details = sh_details[['opDate', 'stockCode', 'rzye', 'rzmre', 'rqyl', 'rqmcl']]

    details.columns = MARGIN_COLUMNS
    return details 


def get_sz_margin_details(date):
    """
    获取深市某天的融资融券明细列表
    Parameters
    --------
    date:string
                日期 format：YYYY-MM-DD
    output_list:list
                存放结果
    Return
    ------
    DataFrame
    """
    sz_details = ts.sz_margin_details(date=date)
    if sz_details.empty:
        return pd.DataFrame(columns=MARGIN_COLUMNS)
    details = sz_details[['opDate', 'stockCode', 'rzye', 'rzmre', 'rqyl', 'rqmcl']]

    details.columns = MARGIN_COLUMNS
    return details


def get_tick_data(code, date):
    """
    获取某天的分笔数据
    Parameters
    --------
    code：string
                股票代码, e.g.600728
    date:string
                日期 format：YYYY-MM-DD
    Return
    ------
    DataFrame
    """
    #获取连接备用
    cons = ts.get_apis()
    tick_data = ts.tick(code=code, conn=cons, date=date)
    #释放，否则python无法正常退出
    ts.close_apis(cons)
    if tick_data is None:
        return pd.DataFrame(columns=TICK_COLUMNS)
    tick_data.columns = TICK_COLUMNS
    return tick_data
