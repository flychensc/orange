from django.shortcuts import render

from stock import get_basic_info

# Create your views here.


def annual_report(request, code):
    recent = request.GET.get('recent')
    basic = get_basic_info(code)
    name = basic['名称']
    return render(request, 'annual_report.html', locals())


def tick_data(request, code):
    start = request.GET.get('start')
    end = request.GET.get('end')
    basic = get_basic_info(code)
    name = basic['名称']
    outstanding = basic['市值(亿)']
    return render(request, 'tick_data.html', locals())
