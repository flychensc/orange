import logging
import datetime
import tushare as ts
import numpy as np
from .models import StockBasics

#获取连接备用
CONS = ts.get_apis()

logger = logging.getLogger("orange.storage")


def _stock_basics():
    stock_basics = ts.get_stock_basics()
    # START
    if stock_basics['esp'].dtype == np.dtype('float64'):
        # rename 'eps' to 'esp'
        stock_basics["eps"] = stock_basics["esp"]
    else:
        # convert 'eps'
        # as I found 'esp' field was '0.147㈡' at Feb.26.2016
        # It cause SQL server error.
        logger.warn(u"'esp'非浮点类型")
        def _atof(str):
            try:
                return float(str)
            except ValueError:
                # I found 'esp' field was '0.000㈣' at Nov.8.2016
                return float(str[:-1])
        stock_basics["eps"] = stock_basics["esp"].apply(_atof)
    stock_basics = stock_basics.drop("esp", axis=1)
    # drop timeToMarket is zero
    stock_basics = stock_basics[stock_basics['timeToMarket']!=0]
    # change sql type
    stock_basics['timeToMarket'] = stock_basics['timeToMarket'].apply(lambda x:datetime.datetime.strptime(str(x), "%Y%m%d").date())
    # END

    stock_basics_list = [StockBasics(
            code = code,
            name = data['name'],
            industry = data['industry'],
            area = data['area'],
            pe = data['pe'],
            outstanding = data['outstanding'],
            totals = data['totals'],
            totalAssets = data['totalAssets'],
            liquidAssets = data['liquidAssets'],
            fixedAssets = data['fixedAssets'],
            reserved = data['reserved'],
            reservedPerShare = data['reservedPerShare'],
            eps = data['eps'],
            bvps = data['bvps'],
            pb = data['pb'],
            timeToMarket = str(data['timeToMarket']),
        ) for code, data in stock_basics.iterrows()]
    StockBasics.objects.bulk_create(stock_basics_list)

