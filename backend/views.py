from django.shortcuts import render
from django.http import JsonResponse

import json
from stock import get_tick_data

# Create your views here.

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
