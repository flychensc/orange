from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<code>[0-9]+)/annual_report$', views.annual_report, name='tick_data'),
    url(r'^(?P<code>[0-9]+)/tick_data$', views.tick_data, name='tick_data'),
]
