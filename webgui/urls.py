from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    url(r'^basic$', views.basic, name='basic'),
    url(r'^detail$', views.detail, name='detail'),
    url(r'^database$', views.database, name='database'),
    url(r'^(?P<code>[0-9]+)/annual_report$', views.annual_report, name='annual_report'),
    url(r'^(?P<code>[0-9]+)/tick_data$', views.tick_data, name='tick_data'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
