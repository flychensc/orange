from django.shortcuts import render
from django.http import JsonResponse

import datetime
import json
import pandas as pd
from stock import get_annual_report, get_tick_data, pct_change, get_level0_report
from stock.fundamental import LEVEL1_REPORT_INDEX, LEVEL_REPORT_DICT
from storage.stock import get_stock_basics, get_basic_info, get_level1_report
from stock.downloader import load_tick_data, load_notices

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
