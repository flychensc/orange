from django.shortcuts import render
from django.http import JsonResponse

from . import tu_update

# Create your views here.


def update_stock_info(request):
    resp_dict = {}
    if request.method == 'POST' and request.is_ajax():
        resp_dict['status'] = '成功'
        tu_update._stock_basics()
    else:
        resp_dict['status'] = '失败'
    return JsonResponse(resp_dict)


def update_report_data(request):
    resp_dict = {}
    if request.method == 'POST' and request.is_ajax():
        resp_dict['status'] = '成功'
        tu_update._report_data(2017, 3)
    else:
        resp_dict['status'] = '失败'
    return JsonResponse(resp_dict)
