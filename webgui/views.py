from django.shortcuts import render

from stock import get_basic_info

# Create your views here.

def tick_data(request, code):
    start = request.GET.get('start')
    end = request.GET.get('end')
    basic = get_basic_info(code)
    name = basic['名称']
    outstanding = basic['市值(亿)']
    return render(request, 'tick_data.html', locals())
