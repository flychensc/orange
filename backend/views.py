from django.shortcuts import render
from django.http import HttpResponse

from stock import get_tick_data

# Create your views here.

def tick_data(request, code):
    start = request.GET.get('start')
    end = request.GET.get('end')
    tick_data = get_tick_data(code, start, end)
    return HttpResponse("%(tick_data)s" % locals())
