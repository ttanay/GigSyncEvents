from django.conf.urls import url
from . import views

app_name = 'web'

urlpatterns = [
    url(r'^populate/$', views.populate, name='populate'),
    url(r'^add_event/(?P<fb_id>[0-9]+)/$', views.add_event, name='add_event'),
    url(r'^$', views.home, name='home'),
    url(r'^filter', views.filter, name='filter'),
    url(r'^event/(?P<event_id>[0-9]+)/$', views.event, name='event'),
    url(r'^all/$', views.all, name='all'),
    url(r'^today/$', views.today, name='today'),
    url(r'^today/filter', views.today_filter, name='today_filter'),
    url(r'^tomorrow/$', views.tomorrow, name='tomorrow'),
    url(r'^tomorrow/filter', views.tomorrow_filter, name='tomorrow_filter'),
    url(r'^date/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/$', views.date, name='date'),
    url(r'^date/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/filter', views.date_filter, name='date_filter'),
    url(r'^delete/', views.delete, name='delete'),
    url(r'^about/', views.about, name='about'),
    url(r'^howto/', views.howto, name='howto'),
]