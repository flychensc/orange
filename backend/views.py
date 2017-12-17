from django.shortcuts import render
from django.http import JsonResponse

import json
from stock import get_annual_report, get_tick_data, pct_change, get_basic_info
from stock.tu_wrap import get_stock_basics

# Create your views here.


def annual_report(request, code):
    recent = request.GET.get('recent')

    report = get_annual_report(code)
    if recent:
        report = report[report.columns.tolist()[-int(recent):]]

    report.rename(columns=lambda x: str(x)[:10], inplace=True)

    year_yoy = pct_change(report, axis=1)
    year_yoy = (year_yoy * 100).round(2)

    report.fillna(0, inplace=True)
    year_yoy.fillna(0, inplace=True)

    data_dict = dict()
    data_dict['date'] = report.columns.tolist()

    data_dict['income'] = report.loc['销售额'].values.tolist()
    data_dict['profit'] = report.loc['净利润'].values.tolist()
    data_dict['liability'] = report.loc['所有债务'].values.tolist()

    data_dict['income_yoy'] = year_yoy.loc['销售额'].values.tolist()
    data_dict['profit_yoy'] = year_yoy.loc['净利润'].values.tolist()
    data_dict['liability_yoy'] = year_yoy.loc['所有债务'].values.tolist()

    return JsonResponse(data_dict)


def stock_list(request):
    return JsonResponse({
        "stocks": [
            "%s %s" % (row[1].name, row[1]['name'])
            for row in get_stock_basics().iterrows()
        ]
    })


def tick_data(request, code):
    start = request.GET.get('start')
    end = request.GET.get('end')
    tick_data = get_tick_data(code, start, end)

    data_dict = dict()
    data_dict['buy'] = [[
        row[1]['时间'],
        row[1]['成交额'],
    ] for row in tick_data[tick_data['买卖类型'] == 0].iterrows()]
    data_dict['sell'] = [[
        row[1]['时间'],
        row[1]['成交额'],
    ] for row in tick_data[tick_data['买卖类型'] == 1].iterrows()]

    return JsonResponse(data_dict)


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
    data_dict['esp'] = basic_info['每股收益']

    data_array = list()
    data_array.append(data_dict)
    return JsonResponse(data_array, safe=False)
