"""
对tushare的再封装，用cache提高速度

*注意：这里用到了cache, 返回的数据请勿使用inplace等操作
"""

from fastcache import lru_cache

import tushare as ts

#获取连接备用
CONS = ts.get_apis()


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
def get_k_data(code,
               start=None,
               end=None):
    """
    BAR数据
    Parameters:
    ------------
    code:证券代码，支持股票,ETF/LOF,期货/期权,港股
    con:服务器连接 ，通过ts.api()或者ts.xpi()获得
    start_date:开始日期  YYYY-MM-DD/YYYYMMDD
    end_date:结束日期 YYYY-MM-DD/YYYYMMDD
    freq:支持1/5/15/30/60分钟,周/月/季/年
    asset:证券类型 E:股票和交易所基金，INDEX:沪深指数,X:期货/期权/港股/中概美国/中证指数/国际指数
    market:市场代码，通过ts.get_markets()获取
    adj:复权类型,None不复权,qfq:前复权,hfq:后复权
    ma:均线,支持自定义均线频度，如：ma5/ma10/ma20/ma60/maN
    factors因子数据，目前支持以下两种：
        vr:量比,默认不返回，返回需指定：factor=['vr']
        tor:换手率，默认不返回，返回需指定：factor=['tor']
                    以上两种都需要：factor=['vr', 'tor']
    retry_count:网络重试次数

    Return
    ----------
    DataFrame
    code:代码
    open：开盘close/high/low/vol成交量/amount成交额/maN均价/vr量比/tor换手率

         期货(asset='X')
    code/open/close/high/low/avg_price：均价  position：持仓量  vol：成交总量
    """
    # 替换为新API
    # return ts.get_k_data(code, start, end, ktype, autype, index, retry_count,
    #                      pause)
    return ts.bar(code, conn=CONS, adj='qfq', start_date=start, end_date=end)


@lru_cache()
def get_report_data(year, quarter):
    """
        获取业绩报表数据
    Parameters
    --------
    year:int 年度 e.g:2014
    quarter:int 季度 :1、2、3、4，只能输入这4个季度
        说明：由于是从网站获取的数据，需要一页页抓取，速度取决于您当前网络速度

    Return
    --------
    DataFrame
        code,代码
        name,名称
        eps,每股收益
        eps_yoy,每股收益同比(%)
        bvps,每股净资产
        roe,净资产收益率(%)
        epcf,每股现金流量(元)
        net_profits,净利润(万元)
        profits_yoy,净利润同比(%)
        distrib,分配方案
        report_date,发布日期
    """
    return ts.get_report_data(year, quarter)


@lru_cache()
def get_profit_data(year, quarter):
    """
        获取盈利能力数据
    Parameters
    --------
    year:int 年度 e.g:2014
    quarter:int 季度 :1、2、3、4，只能输入这4个季度
        说明：由于是从网站获取的数据，需要一页页抓取，速度取决于您当前网络速度

    Return
    --------
    DataFrame
        code,代码
        name,名称
        roe,净资产收益率(%)
        net_profit_ratio,净利率(%)
        gross_profit_rate,毛利率(%)
        net_profits,净利润(万元)
        eps,每股收益
        business_income,营业收入(百万元)
        bips,每股主营业务收入(元)
    """
    return ts.get_profit_data(year, quarter)


@lru_cache()
def get_operation_data(year, quarter):
    """
        获取营运能力数据
    Parameters
    --------
    year:int 年度 e.g:2014
    quarter:int 季度 :1、2、3、4，只能输入这4个季度
        说明：由于是从网站获取的数据，需要一页页抓取，速度取决于您当前网络速度

    Return
    --------
    DataFrame
        code,代码
        name,名称
        arturnover,应收账款周转率(次)
        arturndays,应收账款周转天数(天)
        inventory_turnover,存货周转率(次)
        inventory_days,存货周转天数(天)
        currentasset_turnover,流动资产周转率(次)
        currentasset_days,流动资产周转天数(天)
    """
    return ts.get_operation_data(year, quarter)


@lru_cache()
def get_growth_data(year, quarter):
    """
        获取成长能力数据
    Parameters
    --------
    year:int 年度 e.g:2014
    quarter:int 季度 :1、2、3、4，只能输入这4个季度
        说明：由于是从网站获取的数据，需要一页页抓取，速度取决于您当前网络速度

    Return
    --------
    DataFrame
        code,代码
        name,名称
        mbrg,主营业务收入增长率(%)
        nprg,净利润增长率(%)
        nav,净资产增长率
        targ,总资产增长率
        epsg,每股收益增长率
        seg,股东权益增长率
    """
    return ts.get_growth_data(year, quarter)


@lru_cache()
def get_debtpaying_data(year, quarter):
    """
        获取偿债能力数据
    Parameters
    --------
    year:int 年度 e.g:2014
    quarter:int 季度 :1、2、3、4，只能输入这4个季度
        说明：由于是从网站获取的数据，需要一页页抓取，速度取决于您当前网络速度

    Return
    --------
    DataFrame
        code,代码
        name,名称
        currentratio,流动比率
        quickratio,速动比率
        cashratio,现金比率
        icratio,利息支付倍数
        sheqratio,股东权益比率
        adratio,股东权益增长率
    """
    return ts.get_debtpaying_data(year, quarter)


@lru_cache()
def get_cashflow_data(year, quarter):
    """
        获取现金流量数据
    Parameters
    --------
    year:int 年度 e.g:2014
    quarter:int 季度 :1、2、3、4，只能输入这4个季度
        说明：由于是从网站获取的数据，需要一页页抓取，速度取决于您当前网络速度

    Return
    --------
    DataFrame
        code,代码
        name,名称
        cf_sales,经营现金净流量对销售收入比率
        rateofreturn,资产的经营现金流量回报率
        cf_nm,经营现金净流量与净利润的比率
        cf_liabilities,经营现金净流量对负债比率
        cashflowratio,现金流量比率
    """
    return ts.get_cashflow_data(year, quarter)


@lru_cache()
def sh_margin_details(date='',
                      symbol='',
                      start='',
                      end=''):
    """
    获取沪市融资融券明细列表
    Parameters
    --------
    date:string
                明细数据日期 format：YYYY-MM-DD 默认为空''
    symbol：string
                标的代码，6位数字e.g.600848，默认为空
    start:string
                  开始日期 format：YYYY-MM-DD 默认为空''
    end:string
                  结束日期 format：YYYY-MM-DD 默认为空''
    retry_count : int, 默认 3
                 如遇网络等问题重复执行的次数
    pause : int, 默认 0
                重复请求数据过程中暂停的秒数，防止请求间隔时间太短出现的问题

    Return
    ------
    DataFrame
    opDate:信用交易日期
    stockCode:标的证券代码
    securityAbbr:标的证券简称
    rzye:本日融资余额(元)
    rzmre: 本日融资买入额(元)
    rzche:本日融资偿还额(元)
    rqyl: 本日融券余量
    rqmcl: 本日融券卖出量
    rqchl: 本日融券偿还量
    """
    return ts.sh_margin_details(date, symbol, start, end)


@lru_cache()
def sz_margin_details(date=''):
    """
    获取深市融资融券明细列表
    Parameters
    --------
    date:string
                明细数据日期 format：YYYY-MM-DD 默认为空''
    retry_count : int, 默认 3
                 如遇网络等问题重复执行的次数
    pause : int, 默认 0
                重复请求数据过程中暂停的秒数，防止请求间隔时间太短出现的问题

    Return
    ------
    DataFrame
    opDate:信用交易日期
    stockCode:标的证券代码
    securityAbbr:标的证券简称
    rzmre: 融资买入额(元)
    rzye:融资余额(元)
    rqmcl: 融券卖出量
    rqyl: 融券余量
    rqye: 融券余量(元)
    rzrqye:融资融券余额(元)
    """
    return ts.sz_margin_details(date)


@lru_cache()
def get_tick_data(code, date=''):
    """
    tick数据
    Parameters:
    ------------
    code:证券代码，支持股票,ETF/LOF,期货/期权,港股
    conn:服务器连接 ，通过ts.api()或者ts.xpi()获得
    date:日期
    asset:证券品种，E:沪深交易所股票和基金, INDEX:沪深交易所指数， X:其他证券品种
    market:市场代码，通过ts.get_markets()获取

    Return
    ----------
    DataFrame
    date:日期
    time:时间
    price:成交价
    vol:成交量
    type:买卖方向，0-买入 1-卖出 2-集合竞价成交
            期货  0:开仓  1:多开   -1:空开
         期货多一列数据oi_change:增仓数据

    """
    # 替换为新API
    # return ts.get_tick_data(code, date, retry_count, pause, src)
    return ts.tick(code=code, conn=CONS, date=date)


#不使用cache
def get_notices(code=None, date=None):
    '''
        获取个股信息
    Parameters
    --------
        code:股票代码
        date:信息公布日期
    Return
    --------
        DataFrame，属性列表：
        title:信息标题
        type:信息类型
        date:公告日期
        url:信息内容URL
    '''
    return ts.get_notices(code, date)


#不使用cache
def notice_content(url):
    '''
        获取信息地雷内容
    Parameter
    --------
        url:内容链接
    Return
    --------
        string:信息内容
    '''
    return ts.notice_content(url)
