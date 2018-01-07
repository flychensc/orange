from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^update/stock_info$', views.update_stock_info, name='update_stock_info'),
    url(r'^update/report_data$', views.update_report_data, name='update_report_data'),
]
