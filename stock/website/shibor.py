"""
上海银行间拆放利率
"""

import datetime
import requests
import pandas as pd
import numpy as np

from pandas.compat import BytesIO

HEADERS = {
    'Host': 'www.shibor.org',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Referer': 'http://www.shibor.org/shibor/web/downLoad.jsp',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}


def get_shibor(year):
    """
    Parameters
    ------
        year: string
            年份，e.g. '2018'
    """
    url = f'http://www.shibor.org/shibor/web/html/downLoad.html?nameNew=Historical_Shibor_Data_{year}.xls&nameOld=Shibor%CA%FD%BE%DD{year}.xls&shiborSrc=http%3A%2F%2Fwww.shibor.org%2Fshibor%2F&downLoadPath=data'
    session = requests.Session()
    session.headers.update(HEADERS)

    response = session.get(url, timeout=5)
    response.encoding = "gbk"
    session.close()
    shibor = pd.read_excel(
        BytesIO(response.content),
        na_values=np.NaN,
        converters={
            '日期': lambda x: x.date()
        })
    return shibor.set_index(['日期'])
