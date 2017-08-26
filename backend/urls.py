from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<code>[0-9]+)/tick_data$', views.tick_data, name='tick_data'),
]
