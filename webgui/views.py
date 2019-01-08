from django.http import HttpResponseRedirect
from django.shortcuts import render

from stock import get_basic_info
from storage.models import Interest

# Create your views here.


def home(request):
    return render(request, 'home.html', locals())


def basic(request):
    return render(request, 'basic.html', locals())


def detail(request):
    code = request.GET.get('code')
    stock_interest = Interest.objects.filter(code=code)
    if code and len(code) > 6:
        return HttpResponseRedirect(f"/stock/detail?code={code:{6}.{6}}")
    return render(request, 'detail.html', locals())


def database(request):
    return render(request, 'database.html', locals())


def pool(request):
    return render(request, 'pool.html', locals())


def screener(request):
    return render(request, 'screener.html', locals())


def backtest(request):
    return render(request, 'backtest.html', locals())
