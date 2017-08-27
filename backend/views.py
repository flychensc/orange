from django.shortcuts import render
from django.http import JsonResponse

import json
from stock import get_annual_report, get_tick_data, pct_change

# Create your views here.


def annual_report(request, code):
    annual_report = get_annual_report(code)
    annual_report.rename(columns=lambda x: str(x)[:10], inplace=True)
    year_yoy = pct_change(annual_report, axis=1)
    year_yoy = (year_yoy * 100).round(2)

    data_dict = dict()
    data_dict['date'] = annual_report.columns.tolist()[-5:]

    data_dict['income'] = annual_report.loc['销售额'].values.tolist()[-5:]
    data_dict['profit'] = annual_report.loc['净利润'].values.tolist()[-5:]
    data_dict['liability'] = annual_report.loc['所有债务'].values.tolist()[-5:]

    data_dict['income_yoy'] = year_yoy.loc['销售额'].values.tolist()[-5:]
    data_dict['profit_yoy'] = year_yoy.loc['净利润'].values.tolist()[-5:]
    data_dict['liability_yoy'] = year_yoy.loc['所有债务'].values.tolist()[-5:]

    return JsonResponse(data_dict)


def tick_data(request, code):
    start = request.GET.get('start')
    end = request.GET.get('end')
    tick_data = get_tick_data(code, start, end)

    data_dict = dict()
    data_dict['buy'] = [[
        row[1]['日期'] + ' ' + row[1]['时间'],
        row[1]['成交额'],
    ] for row in tick_data[tick_data['买卖类型'] == '买盘'].iterrows()]
    data_dict['sell'] = [[
        row[1]['日期'] + ' ' + row[1]['时间'],
        row[1]['成交额'],
    ] for row in tick_data[tick_data['买卖类型'] == '卖盘'].iterrows()]

    return JsonResponse(data_dict)
