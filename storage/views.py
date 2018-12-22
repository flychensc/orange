from django.shortcuts import render
from django.http import JsonResponse

from . import tasks
import storage.rcache as rcache

# Create your views here.


def update_stock_info(request):
    resp_dict = {}
    if request.method == 'POST' and request.is_ajax():
        resp_dict['status'] = '成功'
        tasks.update_stock_basics.delay()
    else:
        resp_dict['status'] = '失败'
    return JsonResponse(resp_dict)


def update_history(request):
    resp_dict = {}
    if request.method == 'POST' and request.is_ajax():
        resp_dict['status'] = '成功'
        tasks.update_all_history.delay()
    else:
        resp_dict['status'] = '失败'
    return JsonResponse(resp_dict)


def update_tick_data(request):
    resp_dict = {}
    if request.method == 'POST' and request.is_ajax():
        resp_dict['status'] = '成功'
        tasks.update_tick.delay()
    else:
        resp_dict['status'] = '失败'
    return JsonResponse(resp_dict)


def update_fundamental(request):
    _updater_handle = {
        'report_data': tasks.update_report_data.delay,
        'profit_data': tasks.update_profit_data.delay,
        'operation_data': tasks.update_operation_data.delay,
        'growth_data': tasks.update_growth_data.delay,
        'debtpaying_data': tasks.update_debtpaying_data.delay,
        'cashflow_data': tasks.update_cashflow_data.delay,
    }
    _month_to_quarter = {
        1:1, 2:1, 3:1,
        4:2, 5:2, 6:2,
        7:3, 8:3, 9:3,
        10:4, 11:4, 12:4,
    }
    resp_dict = {}
    if request.method == 'POST' and request.is_ajax():
        db = request.POST.get('db')
        year = int(request.POST.get('year'))
        month = int(request.POST.get('month'))
        quarter = _month_to_quarter[month]
        resp_dict['status'] = '成功'
        _updater_handle[db](year, quarter)
    else:
        resp_dict['status'] = '失败'
    return JsonResponse(resp_dict)


def update_time(request):
    return JsonResponse({
            "basic_info": rcache.get_timestamp(rcache.KEY_TS_BASIC_INFO),
            "history": rcache.get_timestamp(rcache.KEY_TS_HISTORY),
            "tick_data": rcache.get_timestamp(rcache.KEY_TS_TICK_DATA),

            "report_data": rcache.get_timestamp(rcache.KEY_TS_REPORT_DATA),
            "profit_data": rcache.get_timestamp(rcache.KEY_TS_PROFIT_DATA),
            "operation_data": rcache.get_timestamp(rcache.KEY_TS_OPERATION_DATA),
            "growth_data": rcache.get_timestamp(rcache.KEY_TS_GROWTH_DATA),
            "debtpaying_data": rcache.get_timestamp(rcache.KEY_TS_DEBTPAYING_DATA),
            "cashflow_data": rcache.get_timestamp(rcache.KEY_TS_CASHFLOW_DATA),
        })
