"""
从stock里获取网络数据，存放在数据库里
"""

import datetime
import socket
import pandas as pd
from stock import (get_stock_basics, get_k_data,
                    get_report_data, get_profit_data,
                    get_operation_data, get_growth_data,
                    get_debtpaying_data, get_cashflow_data,
                    get_tick_data)
from stock.downloader import load_historys
from navel.celery import app
from .models import *
from .stock import get_stock_basics as get_local_stock_basics

@app.task(ignore_result=True)
def update_stock_basics():
    stock_basics = get_stock_basics()

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
    # 先清空
    StockBasics.objects.all().delete()
    # 再保存
    StockBasics.objects.bulk_create(stock_basics_list)

 
@app.task(ignore_result=True)
def update_history():
    """
    deprecated
    耗时大约8分钟
    """
    start_date = (datetime.date.today()-datetime.timedelta(days=30*6)).strftime("%Y-%m-%d")
    historys = load_historys(start_date)

    history_list = []
    for history in historys:
        for day, data in history.iterrows():
            history_list.append(History(
                code = data['code'],
                day = str(day),
                open = data['open'],
                close = data['close'],
                high = data['high'],
                low = data['low'],
                vol = data['volume'],
            ))
    # 先清空
    History.objects.all().delete()
    # 再保存
    History.objects.bulk_create(history_list)

 
@app.task(ignore_result=True)
def update_one_history(code, start):
    try:
        print("Get %(code)s history data" % locals())
        # 获取历史数据
        history = get_k_data(code, start)
        history.set_index(["date"], inplace=True)
    
        history_list = [History(
                code = data['code'],
                day = str(day),
                open = data['open'],
                close = data['close'],
                high = data['high'],
                low = data['low'],
                vol = data['volume'],
            ) for day, data in history.iterrows()]
        # 先清空
        # History.objects.filter(code=code).delete()
        # 再保存
        History.objects.bulk_create(history_list)
    except socket.timeout:
        print("%(code)s as socket.timeout" % locals())
        self.retry(countdown=5, max_retries=3, exc=e)
    except Exception as e:
        print("%(code)s exception as %(e)s" % locals())
        return

 
@app.task(ignore_result=True)
def update_all_history():
    start_date = (datetime.date.today()-datetime.timedelta(days=30*6)).strftime("%Y-%m-%d")
    # 先清空
    History.objects.all().delete()
    # all stocks' code
    for code in get_local_stock_basics().index:
        update_one_history.delay(code, start_date)


@app.task(ignore_result=True)
def update_report_data(year, quarter):
    report_data = get_report_data(year, quarter)

    # django.db.utils.OperationalError: (1054, "Unknown column 'nane0' in 'field list'")
    report_data = report_data.astype(object).where(pd.notnull(report_data), None)

    report_data_list = [ReportData(
            code = data['code'],
            name = data['name'],
            eps = data['eps'],
            eps_yoy = data['eps_yoy'],
            bvps = data['bvps'],
            roe = data['roe'],
            epcf = data['epcf'],
            net_profits = data['net_profits'],
            profits_yoy = data['profits_yoy'],
            distrib = data['distrib'],
            report_date = data['report_date'],
        ) for index, data in report_data.iterrows()]
    # 先清空
    ReportData.objects.all().delete()
    # 再保存
    ReportData.objects.bulk_create(report_data_list)


@app.task(ignore_result=True)
def update_profit_data(year, quarter):
    profit_data = get_profit_data(year, quarter)

    # django.db.utils.OperationalError: (1054, "Unknown column 'nane0' in 'field list'")
    profit_data = profit_data.astype(object).where(pd.notnull(profit_data), None)

    profit_data_list = [ProfitData(
            code = data['code'],
            name = data['name'],
            roe = data['roe'],
            net_profit_ratio = data['net_profit_ratio'],
            gross_profit_rate = data['gross_profit_rate'],
            net_profits = data['net_profits'],
            eps = data['eps'],
            business_income = data['business_income'],
            bips = data['bips'],
        ) for index, data in profit_data.iterrows()]
    # 先清空
    ProfitData.objects.all().delete()
    # 再保存
    ProfitData.objects.bulk_create(profit_data_list)


@app.task(ignore_result=True)
def update_operation_data(year, quarter):
    operation_data = get_operation_data(year, quarter)

    # django.db.utils.OperationalError: (1054, "Unknown column 'nane0' in 'field list'")
    operation_data = operation_data.astype(object).where(pd.notnull(operation_data), None)

    operation_data_list = [OperationData(
            code = data['code'],
            name = data['name'],
            arturnover = data['arturnover'],
            arturndays = data['arturndays'],
            inventory_turnover = data['inventory_turnover'],
            inventory_days = data['inventory_days'],
            currentasset_turnover = data['currentasset_turnover'],
            currentasset_days = data['currentasset_days'],
        ) for index, data in operation_data.iterrows()]
    # 先清空
    OperationData.objects.all().delete()
    # 再保存
    OperationData.objects.bulk_create(operation_data_list)


@app.task(ignore_result=True)
def update_growth_data(year, quarter):
    growth_data = get_growth_data(year, quarter)

    # django.db.utils.OperationalError: (1054, "Unknown column 'nane0' in 'field list'")
    growth_data = growth_data.astype(object).where(pd.notnull(growth_data), None)

    growth_data_list = [GrowthData(
            code = data['code'],
            name = data['name'],
            mbrg = data['mbrg'],
            nprg = data['nprg'],
            nav = data['nav'],
            targ = data['targ'],
            epsg = data['epsg'],
            seg = data['seg'],
        ) for index, data in growth_data.iterrows()]
    # 先清空
    GrowthData.objects.all().delete()
    # 再保存
    GrowthData.objects.bulk_create(growth_data_list)


@app.task(ignore_result=True)
def update_debtpaying_data(year, quarter):
    debtpaying_data = get_debtpaying_data(year, quarter)

    # django.db.utils.OperationalError: (1054, "Unknown column 'nane0' in 'field list'")
    debtpaying_data = debtpaying_data.astype(object).where(pd.notnull(debtpaying_data), None)

    debtpaying_data_list = [DebtpayingData(
            code = data['code'],
            name = data['name'],
            currentratio = data['currentratio'],
            quickratio = data['quickratio'],
            cashratio = data['cashratio'],
            icratio = data['icratio'],
            sheqratio = data['sheqratio'],
            adratio = data['adratio'],
        ) for index, data in debtpaying_data.iterrows()]
    # 先清空
    DebtpayingData.objects.all().delete()
    # 再保存
    DebtpayingData.objects.bulk_create(debtpaying_data_list)


@app.task(ignore_result=True)
def update_cashflow_data(year, quarter):
    cashflow_data = get_cashflow_data(year, quarter)

    # django.db.utils.OperationalError: (1054, "Unknown column 'nane0' in 'field list'")
    cashflow_data = cashflow_data.astype(object).where(pd.notnull(cashflow_data), None)

    cashflow_data_list = [CashflowData(
            code = data['code'],
            name = data['name'],
            cf_sales = data['cf_sales'],
            rateofreturn = data['rateofreturn'],
            cf_nm = data['cf_nm'],
            cf_liabilities = data['cf_liabilities'],
            cashflowratio = data['cashflowratio'],
        ) for index, data in cashflow_data.iterrows()]
    # 先清空
    CashflowData.objects.all().delete()
    # 再保存
    CashflowData.objects.bulk_create(cashflow_data_list)


@app.task(ignore_result=True)
def update_one_tick(code, day):
    try:
        print("Get %(code)s tick data" % locals())
        # 获取分笔数据
        tick = get_tick_data(code, day)
    
        tick_list = [Tick(
                code = code,
                day = str(day),
                sec1_buy = data['一区买入'],
                sec1_sell = data['一区卖出'],
                sec2_buy = data['二区买入'],
                sec2_sell = data['二区卖出'],
                sec3_buy = data['三区买入'],
                sec3_sell = data['三区卖出'],
                sec4_buy = data['四区买入'],
                sec4_sell = data['四区卖出'],
            ) for index, data in tick.iterrows()]
        # 保存
        Tick.objects.bulk_create(tick_list)
    except socket.timeout:
        print("%(code)s as socket.timeout" % locals())
        self.retry(countdown=5, max_retries=3, exc=e)
    except Exception as e:
        print("%(code)s exception as %(e)s" % locals())
        return

 
@app.task(ignore_result=True)
def update_all_tick():
    """
    deprecated
    太费时间，1天的分笔大约13分钟，1天大概就要3～4小时
    """
    days = [(datetime.date.today()-datetime.timedelta(days=offset)).strftime("%Y-%m-%d") for offset in range(15)]
    # 先清空
    Tick.objects.all().delete()
    # all stocks' code
    for code in get_local_stock_basics().index:
        for day in days:
            update_one_tick.delay(code, day)

 
@app.task(ignore_result=True)
def update_tick():
    day = datetime.date.today().strftime("%Y-%m-%d")
    # 先清空
    Tick.objects.all().delete()
    # all stocks' code
    for code in get_local_stock_basics().index:
        update_one_tick.delay(code, day)
