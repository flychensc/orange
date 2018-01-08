from django.shortcuts import render
from django.http import JsonResponse

from . import tu_update

# Create your views here.


def update_stock_info(request):
    resp_dict = {}
    if request.method == 'POST' and request.is_ajax():
        resp_dict['status'] = '成功'
        tu_update.stock_basics()
    else:
        resp_dict['status'] = '失败'
    return JsonResponse(resp_dict)


def update_report_data(request):
    _tu_update_handle = {
        'report_data': tu_update.report_data,
        'profit_data': tu_update.profit_data,
        'operation_data': tu_update.operation_data,
        'growth_data': tu_update.growth_data,
        'debtpaying_data': tu_update.debtpaying_data,
        'cashflow_data': tu_update.cashflow_data,
    }
    resp_dict = {}
    if request.method == 'POST' and request.is_ajax():
        db = request.POST.get('db')
        year = request.POST.get('year')
        quarter = request.POST.get('quarter')
        resp_dict['status'] = '成功'
        _tu_update_handle[db](year, quarter)
    else:
        resp_dict['status'] = '失败'
    return JsonResponse(resp_dict)
