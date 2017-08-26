from django.shortcuts import render

# Create your views here.

def tick_data(request, code):
    start = request.GET.get('start')
    end = request.GET.get('end')
    return render(request, 'tick_data.html')
