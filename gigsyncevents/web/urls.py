from django.conf.urls import url
from . import views

app_name = 'web'

urlpatterns = [
    url(r'^populate/$', views.populate, name='populate'),
    url(r'^add_event/(?P<fb_id>[0-9]+)/$', views.add_event, name='add_event'),
    url(r'^$', views.home, name='home'),
    url(r'^city/(?P<city>[\w-]+)/$', views.filter_by_city, name='filter_by_city'),
    url(r'^event/(?P<event_id>[0-9]+)/$', views.event, name='event'),
    url(r'^all/$', views.all, name='all'),
    url(r'^today/$', views.today, name='today'),
    url(r'^today/(?P<city>[\w-]+)/$', views.today_by_city, name='today_by_city'),
    url(r'^tomorrow/$', views.tomorrow, name='tomorrow'),
    url(r'^tomorrow/(?P<city>[\w-]+)/$', views.tomorrow_by_city, name='tomorrow_by_city'),
    url(r'^date/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/$', views.date, name='date'),
    url(r'^date/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/(?P<city>[\w-]+)/$', views.date_by_city, name='date_by_city'),
    url(r'^delete/', views.delete, name='delete'),
]