from django.http import HttpResponseRedirect
from django.shortcuts import render

from stock import get_basic_info

# Create your views here.


def home(request):
    return render(request, 'home.html', locals())


def basic(request):
    return render(request, 'basic.html', locals())


def detail(request):
    code = request.GET.get('code')
    if code and len(code) > 6:
        return HttpResponseRedirect(f"/stock/detail?code={code:{6}.{6}}")
    return render(request, 'detail.html', locals())


def database(request):
    return render(request, 'database.html', locals())


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
