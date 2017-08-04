"""
网易财经接口
"""

import logging
import requests
import pandas as pd
from pandas.compat import StringIO

LOGGER = logging.getLogger("stock")

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
    LOGGER.debug("URL:%s encoding=%s", url, response.encoding)

    response.encoding = "gbk"
    web_content = response.text

    balance_sheet = pd.read_csv(StringIO(web_content), index_col=0)
    # pylint: disable=E1101
    return balance_sheet.dropna(axis=1, how='any').T

if __name__ == '__main__':
    # 创建logger
    LOGGER.setLevel(logging.DEBUG)

    # 定义log格式
    LOG_FORMAT = logging.Formatter('%(asctime)s %(name)s:%(levelname)s %(message)s')

    # 创建控制台handler
    CONSOLE_HANDLE = logging.StreamHandler()
    CONSOLE_HANDLE.setLevel(logging.DEBUG)
    CONSOLE_HANDLE.setFormatter(LOG_FORMAT)

    # 注册handler
    LOGGER.addHandler(CONSOLE_HANDLE)

    print(get_balance_sheet('002356'))
