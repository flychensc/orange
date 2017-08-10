"""
网易财经接口
"""

import functools
import requests
import pandas as pd
from pandas.compat import StringIO

HEADERS = {
    "Accept":
    "text/html, application/xhtml+xml, image/jxr, */*",
    "Accept-Language":
    "zh-CN",
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
    " Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063",
    "Accept-Encoding":
    "gzip, deflate",
    "Host":
    "quotes.money.163.com",
    "Connection":
    "Keep-Alive"
}


@functools.lru_cache()
def get_balance_sheet(code, annual=True):
    """
        获取个股资产负债表
    Parameters
    ------
        code:string
                股票代码 e.g. 002356
        annual:bool, 默认 true
                报表类型，默认年报
    return
    ------
        DataFrame
    """

    # http://quotes.money.163.com/service/zcfzb_002356.html
    url = r"http://quotes.money.163.com/service/zcfzb_%s.html" % code

    session = requests.Session()
    session.headers.update(HEADERS)

    if annual:
        response = session.get(url, params={"type": "year"}, timeout=5)
    else:
        response = session.get(url, timeout=5)

    response.encoding = "gbk"

    balance_sheet = pd.read_csv(
        StringIO(response.text),
        index_col=0,
        na_values="--",
        skipinitialspace=True)
    # pylint: disable=E1101
    # drop unnamed column
    balance_sheet = balance_sheet.drop(balance_sheet.columns[-1], axis=1)
    # convert type
    balance_sheet.columns = pd.to_datetime(balance_sheet.columns)
    return balance_sheet.astype(float)


@functools.lru_cache()
def get_profit_statement(code, annual=True):
    """
        获取个股利润表
    Parameters
    ------
        code:string
                股票代码 e.g. 002356
        annual:bool, 默认 true
                报表类型，默认年报
    return
    ------
        DataFrame
    """

    #http://quotes.money.163.com/service/lrb_002356.html
    url = r"http://quotes.money.163.com/service/lrb_%s.html" % code

    session = requests.Session()
    session.headers.update(HEADERS)

    if annual:
        response = session.get(url, params={"type": "year"}, timeout=5)
    else:
        response = session.get(url)

    response.encoding = "gbk"

    profit_statement = pd.read_csv(
        StringIO(response.text),
        index_col=0,
        na_values="--",
        skipinitialspace=True)
    # pylint: disable=E1101
    # drop unnamed column
    profit_statement = profit_statement.drop(
        profit_statement.columns[-1], axis=1)
    # convert type
    profit_statement.columns = pd.to_datetime(profit_statement.columns)
    return profit_statement.astype(float)
