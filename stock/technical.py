"""
技术面
"""

import tushare as ts
import pandas as pd

MARGIN_COLUMNS = ['日期', '股票代码', '融资余额(元)', '融资买入额(元)', '融券余量', '融券卖出量']

TICK_COLUMNS = ['时间', '成交价', '成交量', '买卖类型']
TICK_COLUMNS1 = ['时间', '一区买入', '一区卖出', '二区买入', '二区卖出', '三区买入', '三区卖出', '四区买入', '四区卖出']


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


def _classifier_tick_data(tick_data):
    day = tick_data['时间'][0][:10]
    buy = tick_data[ tick_data['买卖类型'] == 0]
    sell = tick_data[ tick_data['买卖类型'] == 1]
    
    sum = buy[ buy['时间'] <= f'{day} 10:30'].sum()
    sec1_buy = sum['成交价']*sum['成交量']
    sum = sell[ sell['时间'] <= f'{day} 10:30'].sum()
    sec1_sell = sum['成交价']*sum['成交量']

    sum = buy[ buy['时间'] <= f'{day} 11:30'].sum()
    sec2_buy = sum['成交价']*sum['成交量']
    sum = sell[ sell['时间'] <= f'{day} 11:30'].sum()
    sec2_sell = sum['成交价']*sum['成交量']

    sum = buy[ buy['时间'] <= f'{day} 14:00'].sum()
    sec3_buy = sum['成交价']*sum['成交量']
    sum = sell[ sell['时间'] <= f'{day} 14:00'].sum()
    sec3_sell = sum['成交价']*sum['成交量']

    sum = buy[ buy['时间'] <= f'{day} 15:00'].sum()
    sec4_buy = sum['成交价']*sum['成交量']
    sum = sell[ sell['时间'] <= f'{day} 15:00'].sum()
    sec4_sell = sum['成交价']*sum['成交量']

    return pd.DataFrame([[day, sec1_buy, sec1_sell, sec2_buy, sec2_sell,
                            sec3_buy, sec3_sell, sec4_buy, sec4_sell]],
                        columns=TICK_COLUMNS1)


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
    return _classifier_tick_data(tick_data)


def get_k_data(code, start=''):
    """
    相对于bar，这个API可以无法取出当天的数据，但速度很快
    """
    # ts.bar(code, conn=cons, adj='qfq', start_date=start)
    his_data = ts.get_k_data(code, start=start)
    return his_data


def bar(code, start=''):
    """
    相对于get_k_data，这个API可以取出完整的数据，但速度太慢，30多分钟都没取完
    """
    #获取连接备用
    cons = ts.get_apis()
    his_data = ts.bar(code, conn=cons, adj='qfq', start_date=start)
    #释放，否则python无法正常退出
    ts.close_apis(cons)
    return his_data
