from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<code>[0-9]+)/annual_report$', views.annual_report, name='annual_report'),
    url(r'^stock_list$', views.stock_list, name='stock_list'),
    url(r'^(?P<code>[0-9]+)/tick_data$', views.tick_data, name='tick_data'),
]
