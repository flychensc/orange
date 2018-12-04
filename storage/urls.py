from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^update/stock_info$', views.update_stock_info, name='update_stock_info'),
    url(r'^update/history$', views.update_history, name='update_history'),
    url(r'^update/fundamental$', views.update_fundamental, name='update_fundamental'),
]
