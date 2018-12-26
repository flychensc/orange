"""
海事服务网
"""

import requests
import pandas as pd

HEADERS = {
    'Host': 'www.cnss.com.cn',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}


def get_bdi_index():
    exponents = ['day', 'week', 'month', 'season', 'half', 'year']
    url = r'http://www.cnss.com.cn/caches/task/exponent/bdi/%s.json' % exponents[4]
    session = requests.Session()
    session.headers.update(HEADERS)

    response = session.get(url, timeout=5)
    session.close()
    bdi = pd.read_json(response.text)
    return bdi.set_index(['date'])
    
