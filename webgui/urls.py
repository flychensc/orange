from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    url(r'^(?P<code>[0-9]+)/tick_data$', views.tick_data, name='tick_data'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
