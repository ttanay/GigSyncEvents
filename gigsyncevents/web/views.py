from django.shortcuts import render
from django.http import HttpResponse
from . import tasks
from . import models

import json, datetime
# Create your views here.


#HELPER FUNCTIONS



def populate(request):
    tasks.get_gs_data.delay()
    return HttpResponse('Populating DB')

def home(request):
    gigs = models.Gig.objects.order_by('start_date').all()
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
    return render(request, 'web/index.html', {'gigs': gigs})


def event(request, event_id):
    gig = models.Gig.objects.get(event_id=event_id)
    involved_parties = gig.involved_parties.all()
    related_events = []
    for party in involved_parties:
        events = models.Gig.objects.filter(involved_parties__gs_id=party.gs_id)
        for event in events[:3]:
            if event.event_id != event_id:
                related_events.append(event)
    
    return render(request, 'web/event.html', {
        "gig": gig,
        "involved_parties": involved_parties,
        "related_events": related_events,
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

def add_event(request, fb_id):
    tasks.get_event_data.delay(fb_id)
    return HttpResponse('Validating event')

def today(request):
    today = datetime.date.today()
    q_set = models.Gig.objects.filter(start_date=today)
    return render(request, 'api/today.html', {'events': q_set})

def tomorrow(request):
    tomorrow = datetime.date.today() - datetime.timedelta(days=1)
    q_set = models.Gig.objects.filter(start_date=tomorrow)
    return render(request, 'api/tomorrow.html', {'events': q_set})

def date(request, year, month, day):
    date = datetime.date(year=year, month=month, day=day)
    q_set = models.Gig.objects.filter(start_Date=date)
    return render(request, 'api/date.html', {'events': q_set})

def filter_by_city(request, city):
    q_set = models.Gig.objects.filter(city=city)
    return render(request, 'api/city.html', {'events': q_set})

def filter_by_category(request, subcategory):
    q_set = models.Gig.objects.filter(involved_parties__subcategory=subcategory)
    return render(request, 'api/filter_cat.html', {'events': q_set})

