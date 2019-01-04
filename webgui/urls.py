from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    url(r'^basic$', views.basic, name='basic'),
    url(r'^detail$', views.detail, name='detail'),
    url(r'^database$', views.database, name='database'),
    url(r'^pool$', views.pool, name='pool'),
    url(r'^screener$', views.screener, name='screener'),
    url(r'^backtest$', views.backtest, name='backtest'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
