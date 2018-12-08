from django.shortcuts import render
from django.http import JsonResponse

from . import updater

# Create your views here.


def update_stock_info(request):
    resp_dict = {}
    if request.method == 'POST' and request.is_ajax():
        resp_dict['status'] = '成功'
        updater.stock_basics()
    else:
        resp_dict['status'] = '失败'
    return JsonResponse(resp_dict)


def update_history(request):
    resp_dict = {}
    if request.method == 'POST' and request.is_ajax():
        resp_dict['status'] = '成功'
        updater.history()
    else:
        resp_dict['status'] = '失败'
    return JsonResponse(resp_dict)


def update_fundamental(request):
    _updater_handle = {
        'report_data': updater.report_data,
        'profit_data': updater.profit_data,
        'operation_data': updater.operation_data,
        'growth_data': updater.growth_data,
        'debtpaying_data': updater.debtpaying_data,
        'cashflow_data': updater.cashflow_data,
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
