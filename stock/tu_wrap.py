"""
对tushare的再封装，用cache提高速度
"""

from fastcache import lru_cache

import tushare as ts


@lru_cache()
def get_stock_basics(date=None):
    """
        获取沪深上市公司基本情况
    Parameters
    date:日期YYYY-MM-DD，默认为上一个交易日，目前只能提供2016-08-09之后的历史数据

    Return
    --------
    DataFrame
               code,代码
               name,名称
               industry,细分行业
               area,地区
               pe,市盈率
               outstanding,流通股本
               totals,总股本(万)
               totalAssets,总资产(万)
               liquidAssets,流动资产
               fixedAssets,固定资产
               reserved,公积金
               reservedPerShare,每股公积金
               eps,每股收益
               bvps,每股净资
               pb,市净率
               timeToMarket,上市日期
    """
    return ts.get_stock_basics(date)


@lru_cache()
def get_k_data(code=None,
               start='',
               end='',
               ktype='D',
               autype='qfq',
               index=False,
               retry_count=3,
               pause=0.001):
    """
    获取k线数据
    ---------
    Parameters:
      code:string
                  股票代码 e.g. 600848
      start:string
                  开始日期 format：YYYY-MM-DD 为空时取上市首日
      end:string
                  结束日期 format：YYYY-MM-DD 为空时取最近一个交易日
      autype:string
                  复权类型，qfq-前复权 hfq-后复权 None-不复权，默认为qfq
      ktype：string
                  数据类型，D=日k线 W=周 M=月 5=5分钟 15=15分钟 30=30分钟 60=60分钟，默认为D
      retry_count : int, 默认 3
                 如遇网络等问题重复执行的次数 
      pause : int, 默认 0
                重复请求数据过程中暂停的秒数，防止请求间隔时间太短出现的问题
    return
    -------
      DataFrame
          date 交易日期 (index)
          open 开盘价
          high  最高价
          close 收盘价
          low 最低价
          volume 成交量
          amount 成交额
          turnoverratio 换手率
          code 股票代码
    """
    return ts.get_k_data(code, start, end, ktype, autype, index, retry_count,
                         pause)
