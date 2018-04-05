from django.shortcuts import render
from django.http import HttpResponse
from django.utils.text import slugify
from . import tasks
from . import models

import json, datetime
# Create your views here.


#HELPER FUNCTIONS

def populate(request):
    tasks.get_gs_data.delay()
    return HttpResponse('Populating DB')

def delete(request):
    tasks.remove_past_events.delay()
    return HttpResponse('Deleting Past Events')

def home(request):
    gigs = models.Gig.objects.order_by('start_date').all()
    cities = []
    for gig in gigs:
        if gig.city not in cities:
            cities.append(gig.city)
    '''events = []
    count = 0
    for event in all_events:
        event_context = {
            "cover": event.cover_link,
            "start_month": event.get_start_month_abb(),
            "start_date": event.get_start_date(),
            "name": event.name,
            "venue": event.venue,
            "id": event.event_id,
        }
        events.append(event_context)'''
    print(cities)
    return render(request, 'web/index.html', {'gigs': gigs, 'cities': cities})


def event(request, event_id):
    gig = models.Gig.objects.get(event_id=event_id)
    involved_parties = gig.involved_parties.all()
    related_events = []
    for party in involved_parties:
        events = models.Gig.objects.filter(involved_parties__gs_id=party.gs_id)
        for event in events:
            if event.event_id == gig.event_id:
                pass
            else:
                print(event_id)
                print(event.event_id)
                related_events.append(event)
    
    return render(request, 'web/event.html', {
        "gig": gig,
        "involved_parties": involved_parties,
        "related_events": related_events[:3],
    })

def all(request):
    all_events = models.Gig.objects.order_by('start_date').all()
    for event in all_events:
        print(event.name)
    #print(all_events)
    return render(request, 'web/all.html', {"all_events": all_events})

#def filter_category(request, category):
 #   q_set = Gig.objects.filter(subcategory=category)
  #  pass

def filter_by_city(request, city):
    all_events = models.Gig.objects.all()
    result_list = []
    for event in all_events:
        city_slug = slugify(event.city)
        if city_slug == city:
            result_list.append(event)
    return render(request, 'web/index.html', {'gigs': result_list})

def add_event(request, fb_id):
    tasks.get_event_data.delay(fb_id)
    return HttpResponse('Validating event')

def today(request):
    today = datetime.date.today()
    q_set = models.Gig.objects.filter(start_date=today)
    cities = []
    for event in q_set:
        if event.city not in cities:
            cities.append(event.city)
    return render(request, 'web/today.html', {'gigs': q_set, 'cities': cities})

def today_by_city(request, city):
    today = datetime.date.today()
    result_list = []
    q_set = models.Gig.objects.filter(start_date=today)
    cities = []
    for event in q_set:
        if event.city not in cities:
            cities.append(event.city)
    for event in q_set:
        city_slug = slugify(event.city)
        if city_slug == city:
            result_list.append(event)
    return render(request, 'web/today.html', {'gigs': result_list, 'cities': cities})

def tomorrow(request):
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    q_set = models.Gig.objects.filter(start_date=tomorrow)
    cities = []
    for event in q_set:
        if event.city not in cities:
            cities.append(event.city)
    return render(request, 'web/tomorrow.html', {'gigs': q_set, 'cities': cities})

def tomorrow_by_city(request, city):
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    q_set = models.Gig.objects.filter(start_date=tomorrow)
    cities = []
    result_list = []
    for event in q_set:
        if event.city not in cities:
            cities.append(event.city)
    for event in q_set:
        city_slug = slugify(event.city)
        if city_slug == city:
            result_list.append(event)
    return render(request, 'web/tomorrow.html', {'gigs': result_list, 'cities': cities})

def date(request, year, month, day):
    year = int(year)
    month = int(month)
    day = int(day)
    date = datetime.date(year=year, month=month, day=day)
    q_set = models.Gig.objects.filter(start_date=date)
    cities = []
    for event in q_set:
        if event.city not in cities:
            cities.append(event.city)
    return render(request, 'web/date.html', {'gigs': q_set, 'cities': cities, 'year': int(year), 'month': int(month), 'day': int(day)})

def date_by_city(request, year, month, day, city):
    year = int(year)
    month = int(month)
    day = int(day)
    date = datetime.date(year=year, month=month, day=day)
    q_set = models.Gig.objects.filter(start_date=date)
    cities = []
    result_list = []
    for event in q_set:
        if event.city not in cities:
            cities.append(event.city)
    for event in q_set:
        city_slug = slugify(event.city)
        if city_slug == city:
            result_list.append(event)
    return render(request, 'web/date.html', {'gigs': result_list, 'cities': cities, 'year': int(year), 'month': int(month), 'day': int(day)})

