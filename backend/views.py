from django.shortcuts import render, redirect
from django.http import JsonResponse

import datetime
import json
import pandas as pd
import numpy as np
from stock import get_annual_report, get_tick_data, pct_change, get_level0_report, get_szzs
from stock.fundamental import LEVEL1_REPORT_INDEX, LEVEL_REPORT_DICT
from stock import get_bdi, get_shibor
from storage.stock import (get_stock_basics, get_basic_info, get_k_data,
                        get_level1_report, get_stock_money_flow,
                        get_day_all)
from stock.downloader import load_tick_data, load_notices
from storage.models import Interest, Position, Comments

# Create your views here.


def annual_report(request, code):
    recent = request.GET.get('recent')

    report = get_annual_report(code)
    if recent:
        report = report[report.columns.tolist()[-int(recent)-1:]]

    report.rename(columns=lambda x: str(x)[:10], inplace=True)

    year_yoy = pct_change(report, axis=1)
    year_yoy = (year_yoy * 100).round(2)

    # replace numpy.NaN to '-'
    report = report.astype(str).where(pd.notnull(report), "-")
    year_yoy = year_yoy.astype(str).where(pd.notnull(year_yoy), "-")

    data_list = list()
    for year in report.columns[1:]:
        data_list.append({
            'year': year,

            'income': report[year].loc['销售额'],
            'profit': report[year].loc['净利润'],
            'liability': report[year].loc['所有债务'],

            'income_yoy': year_yoy[year].loc['销售额'],
            'profit_yoy': year_yoy[year].loc['净利润'],
            'liability_yoy': year_yoy[year].loc['所有债务'],
        })

    return JsonResponse({"annual_report": data_list})


def stock_list(request):
    return JsonResponse({
        "stocks": [
            "%s %s" % (row[1].name, row[1]['name'])
            for row in get_stock_basics().iterrows()
        ]
    })


def tick_data(request, code):
    recent = request.GET.get('recent')

    #todo: 节假日
    deltaday = int(recent)+2 if datetime.date.today().isoweekday() in [6,7] else int(recent)
    start = (datetime.date.today()-datetime.timedelta(days=deltaday)).strftime("%Y-%m-%d")
    end = datetime.date.today().strftime("%Y-%m-%d")
    tick_data = load_tick_data(code, start, end)

    tick_data = tick_data[-int(recent):] if len(tick_data) > int(recent) else tick_data

    data_list = list()
    for index, data in tick_data.iterrows():
        data_list.append({
            'date': data['时间'],

            'sec1_buy': data['一区买入'],
            'sec1_sell': data['一区卖出'],

            'sec2_buy': data['二区买入'],
            'sec2_sell': data['二区卖出'],
            
            'sec3_buy': data['三区买入'],
            'sec3_sell': data['三区卖出'],

            'sec4_buy': data['四区买入'],
            'sec4_sell': data['四区卖出'],
        })

    return JsonResponse({"tick_data": data_list})


def basic_info(request, code):
    basic_info = get_basic_info(code)

    data_dict = dict()
    data_dict['code'] = basic_info['股票代码']
    data_dict['name'] = basic_info['名称']
    data_dict['industry'] = basic_info['行业']
    data_dict['close'] = basic_info['最新价']
    data_dict['nmc'] = basic_info['市值(亿)']
    data_dict['pe'] = basic_info['市盈率']
    data_dict['pb'] = basic_info['市净率']
    data_dict['eps'] = basic_info['每股收益']

    return JsonResponse(data_dict)


def level_0(request, code):
    annual_report = get_annual_report(code)
    level_report = get_level0_report(annual_report.iloc[:, -1])

    data_dict = dict()
    data_dict['Inv'] = level_report['存货大于收入']
    data_dict['AccRec'] = level_report['应收账款大于销售额']
    data_dict['AccPay'] = level_report['应付账款大于收入']
    data_dict['CurLia'] = level_report['流动负债大于流动资产']
    data_dict['ProNon'] = level_report['利润偿还非流动负债']
    data_dict['ProAll'] = level_report['利润偿还所有负债']

    return JsonResponse(data_dict)


def level_1(request, code):
    today = datetime.date.today()
    year = today.year if today.month > 4 else today.year - 1
    level_report = get_level1_report(code, year, 4)
    # replace numpy.NaN to '-'
    level_report = level_report.astype(str).where(pd.notnull(level_report), "-")

    data_dict = dict()
    for idx in LEVEL1_REPORT_INDEX:
        data_dict.setdefault(LEVEL_REPORT_DICT[idx], [])

        data_dict[LEVEL_REPORT_DICT[idx]].append({
            'item': idx,
            'value': level_report[idx],
        })

    return JsonResponse(data_dict)


def notices(request, code):
    recent = request.GET.get('recent')

    #todo: 节假日
    deltaday = int(recent)+2 if datetime.date.today().isoweekday() in [6,7] else int(recent)
    start = (datetime.date.today()-datetime.timedelta(days=deltaday)).strftime("%Y-%m-%d")
    end = datetime.date.today().strftime("%Y-%m-%d")
    notices_info = load_notices(code, start, end)

    notices_info = notices_info[-int(recent):] if len(notices_info) > int(recent) else notices_info

    data_list = list()
    for index, data in notices_info.iterrows():
        data_list.append({
            'no': index+1,
            'date': data['日期'],
            'type': data['类型'],
            'title': data['标题'],
            'URL': data['URL'],
        })

    return JsonResponse({"notices": data_list})


def money_flow(request):
    top = request.GET.get('top')
    stock_info = get_stock_basics()
    money_flow = get_stock_money_flow()

    buy_list = list()
    no = 0
    for index, data in money_flow[:int(top)].iterrows():
        no+=1
        buy_list.append({
            'no': no,
            'code': data.code,
            'name': stock_info['name'][data.code],
            'sum': data['sum'],
        })

    sell_list = list()
    for index, data in money_flow[-int(top):].iterrows():
        sell_list.append({
            'no': no,
            'code': data.code,
            'name': stock_info['name'][data.code],
            'sum': data['sum'],
        })
        no-=1
    sell_list.reverse()

    return JsonResponse({
            "date": money_flow.iloc[0].day,
            "buy_top": buy_list,
            "sell_top": sell_list,
        })


def money_flow_percent(request):
    """
    感觉没什么用，可能是换手率的一个体现吧
    """
    top = request.GET.get('top')

    stock_info = get_stock_basics()
    money_flow = get_stock_money_flow().set_index(['code'])
    day = money_flow.iloc[0].day
    all_history = get_day_all(day)

    money_flow = money_flow.join(all_history, how='inner').join(stock_info, how='inner')
    # 亿元 -> 万元
    money_flow['nmc'] = money_flow['close'] * money_flow['outstanding'] * 10000
    money_flow['p_sum'] = money_flow['sum'] / money_flow['nmc'] * 100

    money_flow.sort_values(['p_sum'], ascending=False, inplace=True)

    buy_list = list()
    no = 0
    for code, data in money_flow[:int(top)].iterrows():
        no+=1
        buy_list.append({
            'no': no,
            'code': code,
            'name': data['name'],
            'sum': data['sum'],
            'nmc': data.nmc,
            'p_sum': data.p_sum,
        })

    sell_list = list()
    for code, data in money_flow[-int(top):].iterrows():
        sell_list.append({
            'no': no,
            'code': code,
            'name': data['name'],
            'sum': data['sum'],
            'nmc': data.nmc,
            'p_sum': data.p_sum,
        })
        no-=1
    sell_list.reverse()

    return JsonResponse({
            "date": day,
            "buy_top": buy_list,
            "sell_top": sell_list,
        })


def rise_fail_stats(request):
    recent = request.GET.get('recent')
    recent = int(recent) if recent else 5

    stats_list = []
    delta = 0
    while recent > 0:
        day = (datetime.date.today()-datetime.timedelta(days=delta)).strftime("%Y-%m-%d")
        delta += 1
        all_history = get_day_all(day)
        if len(all_history) == 0:
            continue

        recent -= 1

        stats_list.append({
            'date': day,
            'rise': len(all_history[ all_history.open < all_history.close]),
            'fail': len(all_history[ all_history.open > all_history.close]),
            'nochange': len(all_history[ all_history.open == all_history.close]),
        })
    stats_list.reverse()

    return JsonResponse({"data": stats_list})


def szzs(request):
    recent = request.GET.get('recent')
    recent = int(recent) if recent else 22*6

    start = (datetime.date.today()-datetime.timedelta(days=recent)).strftime("%Y-%m-%d")
    historys = get_szzs(start)
    historys.set_index('date', inplace=True)

    his_list = []
    for date, data in historys.iterrows():
        his_list.append({
            'date': date,
            'open': data['open'],
            'high': data['high'],
            'close': data['close'],
            'low': data['low'],
        })

    return JsonResponse({"data": his_list})


def bdi(request):
    history = get_bdi()

    his_list = []
    for date, data in history.iterrows():
        his_list.append({
            'date': date.date(),
            'value': int(data['index']),
        })

    return JsonResponse({"bdi": his_list})


def shibor(request):
    history = get_shibor()

    his_list = []
    for date, data in history.iterrows():
        his_list.append({
            'date': date,
            'O/N': float(data['O/N']),
            '1W': float(data['1W']),
            '2W': float(data['2W']),
            '1M': float(data['1M']),
            '3M': float(data['3M']),
            '6M': float(data['6M']),
            '9M': float(data['9M']),
            '1Y': float(data['1Y']),
        })

    return JsonResponse({"shibor": his_list})


def join_interest(request):
    stock = request.POST.get('stock')
    item = Interest(code=stock, createDay=datetime.datetime.today())
    item.save()
    return redirect(request.META['HTTP_REFERER'], locals())


def leave_interest(request):
    stock = request.POST.get('stock')
    Interest.objects.filter(code=stock).delete()
    return redirect(request.META['HTTP_REFERER'], locals())


def interest_list(request):
    interests = []
    for item in Interest.objects.all():
        basic = get_stock_basics().loc[item.code]
        history = get_k_data(item.code)
        growth = history['close'][0] - history['open'][0]
        interests.append({
            'code': item.code,
            'name': basic.loc['name'],
            'industry': basic.loc['industry'],
            'price': history['close'][0],
            'growth': round(growth/history['open'][0]*100, 2),
            'created': item.createDay,
        })

    return JsonResponse({"interests": interests})


def join_position(request):
    stock = request.POST.get('stock')
    priceToSell = request.POST.get('priceToSell')
    priceToStop = request.POST.get('priceToStop')
    item = Position(code=stock, priceToSell=priceToSell, priceToStop=priceToStop, createDay=datetime.datetime.today())
    item.save()
    return redirect(request.META['HTTP_REFERER'], locals())


def leave_position(request):
    stock = request.POST.get('stock')
    Position.objects.filter(code=stock).delete()
    return redirect(request.META['HTTP_REFERER'], locals())


def position_list(request):
    holds = []
    for item in Position.objects.all():
        basic = get_stock_basics().loc[item.code]
        history = get_k_data(item.code)
        growth = history['close'][0] - history['open'][0]
        holds.append({
            'code': item.code,
            'name': basic.loc['name'],
            'industry': basic.loc['industry'],
            'price': history['close'][0],
            'growth': round(growth/history['open'][0]*100, 2),
            'costprice': item.codePrice,
            'priceToSell': item.priceToSell,
            'priceToStop': item.priceToStop,
            'created': item.createDay,
        })

    return JsonResponse({"holds": holds})


def add_comments(request):
    stock = request.POST.get('stock')
    day = request.POST.get('day')
    policy = request.POST.get('policy')
    comments = request.POST.get('comments')
    item = Comments(code=stock, day=day, policy=policy, comments=comments)
    item.save()
    return redirect(request.META['HTTP_REFERER'], locals())


def update_comments(request):
    stock = request.POST.get('stock')
    day = request.POST.get('day')
    policy = request.POST.get('policy')
    comments = request.POST.get('comments')
    item = Comments.objects.get(code=stock, day=day)
    item.policy = policy
    item.comments = comments
    item.save()
    return redirect(request.META['HTTP_REFERER'], locals())


def del_comments(request):
    stock = request.POST.get('stock')
    day = request.POST.get('day')
    Comments.objects.filter(code=stock, day=day).delete()
    return redirect(request.META['HTTP_REFERER'], locals())


def comments_list(request):
    stock = request.GET.get('stock')
    holds = []
    for item in Comments.objects.order_by('day').filter(code=stock):
        holds.append({
            'code': item.code,
            'day': item.day,
            'policy': item.policy,
            'comments': item.comments,
        })

    return JsonResponse({"comments": holds})
