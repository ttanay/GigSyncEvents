from django.conf.urls import url
from . import views

app_name = 'web'

urlpatterns = [
    url(r'^populate/$', views.populate, name='populate'),
    url(r'^add_event/(?P<fb_id>[0-9]+)/$', views.add_event, name='add_event'),
    url(r'^$', views.home, name='populate'),
    url(r'^event/(?P<event_id>[0-9]+)/$', views.event, name='event'),
    url(r'^all/$', views.all, name='all'),
    url(r'^today/$', views.today, name='today'),
    url(r'^tomorrow/$', views.tomorrow, name='tomorrow'),
    url(r'^date/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/$', views.date, name='date'),
]