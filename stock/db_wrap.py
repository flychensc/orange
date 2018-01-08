"""
将SQL里的数据封装为tushare的格式
"""
import pandas as pd
from storage.models import *


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
    datas = [[
        data.code,
        data.name,
        data.industry,
        data.area,
        data.pe,
        data.outstanding,
        data.totals,
        data.totalAssets,
        data.liquidAssets,
        data.fixedAssets,
        data.reserved,
        data.reservedPerShare,
        data.eps,
        data.bvps,
        data.pb,
        data.timeToMarket,
    ] for data in StockBasics.objects.all()]
    tu_data = pd.DataFrame(
        datas,
        columns=[
            'code', 'name', 'industry', 'area', 'pe', 'outstanding', 'totals',
            'totalAssets', 'liquidAssets', 'fixedAssets', 'reserved',
            'reservedPerShare', 'esp', 'bvps', 'pb', 'timeToMarket'
        ])
    tu_data.set_index('code', inplace=True)
    return tu_data


def get_report_data(year, quarter):
    """
        获取业绩报表数据
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
    datas = [[
        data.code, data.name, data.eps, data.eps_yoy, data.bvps, data.roe,
        data.epcf, data.net_profits, data.profits_yoy, data.distrib,
        data.report_date
    ] for data in ReportData.objects.all()]
    tu_data = pd.DataFrame(
        datas,
        columns=[
            'code', 'name', 'eps', 'eps_yoy', 'bvps', 'roe', 'epcf',
            'net_profits', 'profits_yoy', 'distrib', 'report_date'
        ])
    return tu_data


def get_profit_data(year, quarter):
    """
        获取盈利能力数据
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
    datas = [[
        data.code, data.name, data.roe, data.net_profit_ratio,
        data.gross_profit_rate, data.net_profits, data.eps,
        data.business_income, data.bips
    ] for data in ProfitData.objects.all()]
    tu_data = pd.DataFrame(
        datas,
        columns=[
            'code', 'name', 'roe', 'net_profit_ratio', 'gross_profit_rate',
            'net_profits', 'eps', 'business_income', 'bips'
        ])
    return tu_data


def get_operation_data(year, quarter):
    """
        获取营运能力数据
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
    datas = [[
        data.code, data.name, data.arturnover, data.arturndays,
        data.inventory_turnover, data.inventory_days,
        data.currentasset_turnover, data.currentasset_days
    ] for data in OperationData.objects.all()]
    tu_data = pd.DataFrame(
        datas,
        columns=[
            'code', 'name', 'arturnover', 'arturndays', 'inventory_turnover',
            'inventory_days', 'currentasset_turnover', 'currentasset_days'
        ])
    return tu_data


def get_growth_data(year, quarter):
    """
        获取成长能力数据
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
    datas = [[
        data.code, data.name, data.mbrg, data.nprg, data.nav, data.targ,
        data.epsg, data.seg
    ] for data in GrowthData.objects.all()]
    tu_data = pd.DataFrame(
        datas,
        columns=['code', 'name', 'mbrg', 'nprg', 'nav', 'targ', 'epsg', 'seg'])
    return tu_data


def get_debtpaying_data(year, quarter):
    """
        获取偿债能力数据
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
    datas = [[
        data.code, data.name, data.currentratio, data.quickratio,
        data.cashratio, data.icratio, data.sheqratio, data.adratio
    ] for data in DebtpayingData.objects.all()]
    tu_data = pd.DataFrame(
        datas,
        columns=[
            'code', 'name', 'currentratio', 'quickratio', 'cashratio',
            'icratio', 'sheqratio', 'adratio'
        ])
    return tu_data


def get_cashflow_data(year, quarter):
    """
        获取现金流量数据
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
    datas = [[
        data.code, data.name, data.cf_sales, data.rateofreturn, data.cf_nm,
        data.cf_liabilities, data.cashflowratio
    ] for data in CashflowData.objects.all()]
    tu_data = pd.DataFrame(
        datas,
        columns=[
            'code', 'name', 'cf_sales', 'rateofreturn', 'cf_nm',
            'cf_liabilities', 'cashflowratio'
        ])
    return tu_data
