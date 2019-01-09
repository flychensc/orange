from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<code>[0-9]+)/annual_report$', views.annual_report, name='annual_report'),
    url(r'^stock_list$', views.stock_list, name='stock_list'),
    url(r'^(?P<code>[0-9]+)/tick_data$', views.tick_data, name='tick_data'),
    url(r'^(?P<code>[0-9]+)/basic_info$', views.basic_info, name='basic_info'),
    url(r'^(?P<code>[0-9]+)/level_0$', views.level_0, name='level_0'),
    url(r'^(?P<code>[0-9]+)/level_1$', views.level_1, name='level_1'),
    url(r'^(?P<code>[0-9]+)/notices$', views.notices, name='notices'),
    url(r'^money_flow$', views.money_flow, name='money_flow'),
    url(r'^money_flow_percent$', views.money_flow_percent, name='money_flow_percent'),

    url(r'^join_interest$', views.join_interest, name='join_interest'),
    url(r'^leave_interest$', views.leave_interest, name='leave_interest'),
    url(r'^interest_list$', views.interest_list, name='interest_list'),

    url(r'^join_position$', views.join_position, name='join_position'),
    url(r'^leave_position$', views.leave_position, name='leave_position'),
    url(r'^position_list$', views.position_list, name='position_list'),

    url(r'^rise_fail_stats$', views.rise_fail_stats, name='rise_fail_stats'),
    url(r'^szzs$', views.szzs, name='szzs'),
    url(r'^bdi$', views.bdi, name='bdi'),
    url(r'^shibor$', views.shibor, name='shibor'),
]
