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
    genres = []
    for gig in gigs:
        if gig.city not in cities:
            cities.append(gig.city)
        for party in gig.involved_parties.all():
            party_genres = party.get_genres()
            for genre in party_genres:
                if genre not in genres:
                    genres.append(genre)
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
    #print(genres)
    #print(cities)
    return render(request, 'web/index.html', {'gigs': gigs, 'cities': cities, 'genres': genres})


def event(request, event_id):
    gig = models.Gig.objects.get(event_id=event_id)
    involved_parties = gig.involved_parties.all()
    related_events = []
    genres = []
    excess_genres = 0
    for party in involved_parties:
        party_genres = party.get_genres()
        for genre in party_genres:
            if genre not in genres:
                genres.append(genre)
        events = models.Gig.objects.filter(involved_parties__gs_id=party.gs_id)
        for event in events:
            if event.event_id == gig.event_id:
                pass
            else:
                print(event_id)
                print(event.event_id)
                related_events.append(event)
    if len(genres) > 5:
        excess_genres = len(genres) - 5
        genres = genres[:5]
    return render(request, 'web/event.html', {
        "gig": gig,
        "involved_parties": involved_parties,
        "related_events": related_events[:3],
        "genres": genres,
        "excess_genres": excess_genres,
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
'''OLD FILTER VIEW FUNCTION
def filter(request):
    genres = set(request.GET['genres'].split(','))
    city = request.GET['city']
    all_events = models.Gig.objects.all()
    result_list = []
    filtered_list = []
    cities = []
    for event in all_events:
        if event.city not in cities:
            cities.append(event.city)
    if city is not None or city is not 'null' or city is not '':
        for event in all_events:
            city_slug = slugify(event.city)
            if city_slug == city:
                result_list.append(event)
    else:
        result_list = all_events
    if genres:
        for event in result_list:
            for party in event.involved_parties.all():
                party_genres = [slugify(genre) for genre in party.get_genres()]
                party_genres = set(party_genres)
                print(party_genres.intersection(genres))
                if party_genres.intersection(genres):
                    filtered_list.append(event)
                    break
    return render(request, 'web/index.html', {'gigs': filtered_list, 'cities': cities})
'''

def filter(request):
    all_events = models.Gig.objects.order_by('start_date').all()
    genre_list = []
    city_list = []
    try:
        genres = set(request.GET["genres"].split(','))
        for event in all_events:
            for party in event.involved_parties.all():
                if party.entity_type != 'Venue':
                    party_genres = [slugify(genre) for genre in party.get_genres()]
                    party_genres = set(party_genres)
                    if party_genres.intersection(genres):
                        genre_list.append(event)
    except Exception as e:
        print(e)
    try:
        city = request.GET["city"]
        for event in all_events:
            city_slug = slugify(event.city)
            if city_slug == city:
                city_list.append(event)
    except Exception as e:
        print(e)
    if city_list and genre_list:
        result = set(city_list).intersection((set(genre_list)))
    elif city_list and not genre_list:
        result = set(city_list)
    elif genre_list and not city_list:
        result = set(genre_list)
    else:
        result = set()
    ##get all cities and genres to display
    cities = []
    for event in result:
        if event.city not in cities:
            cities.append(event.city)
    genres = []
    for event in result:
        for party in event.involved_parties.all():
            party_genres = party.get_genres()
            for genre in party_genres:
                if genre not in genres:
                    genres.append(genre)
    result = list(result)
    return render(request, 'web/index.html', {'gigs': result, 'cities': cities, 'genres': genres})

def add_event(request, fb_id):
    tasks.get_event_data.delay(fb_id)
    return HttpResponse('Validating event')

def today(request):
    today = datetime.date.today()
    q_set = models.Gig.objects.filter(start_date=today)
    cities = []
    genres = []
    for event in q_set:
        if event.city not in cities:
            cities.append(event.city)
        for party in event.involved_parties.all():
            party_genres = party.get_genres()
            for genre in party_genres:
                if genre not in genres:
                    genres.append(genre)
    return render(request, 'web/today.html', {'gigs': q_set, 'cities': cities, 'genres': genres})

'''OLD TODAY FILTER
def today_filter(request):
    city = request.GET['city']
    today = datetime.date.today()
    result_list = []
    q_set = models.Gig.objects.filter(start_date=today)
    cities = []
    for event in q_set:
        if event.city not in cities:
            cities.append(event.city)    
    if city is not None or city is not 'null' or city is not '':
        for event in q_set:
            city_slug = slugify(event.city)
            if city_slug == city:
                result_list.append(event)
    else:
        result_list = q_set
    return render(request, 'web/today.html', {'gigs': result_list, 'cities': cities})
'''

def today_filter(request):
    today = datetime.date.today()
    today_events = models.Gig.objects.filter(start_date=today)
    genre_list = []
    city_list = []
    try:
        genres = set(request.GET["genres"].split(','))
        for event in today_events:
            for party in event.involved_parties.all():
                if party.entity_type != 'Venue':
                    party_genres = [slugify(genre) for genre in party.get_genres()]
                    party_genres = set(party_genres)
                    if party_genres.intersection(genres):
                        genre_list.append(event)
    except Exception as e:
        print(e)
    try:
        city = request.GET["city"]
        for event in today_events:
            city_slug = slugify(event.city)
            if city_slug == city:
                city_list.append(event)
    except Exception as e:
        print(e)
    if city_list and genre_list:
        result = set(city_list).intersection((set(genre_list)))
    elif city_list and not genre_list:
        result = set(city_list)
    elif genre_list and not city_list:
        result = set(genre_list)
    else:
        result = set()
    ##get all cities and genres to display
    cities = []
    for event in result:
        if event.city not in cities:
            cities.append(event.city)
    genres = []
    for event in result:
        for party in event.involved_parties.all():
            party_genres = party.get_genres()
            for genre in party_genres:
                if genre not in genres:
                    genres.append(genre)
    result = list(result)
    return render(request, 'web/today.html', {'gigs': result, 'cities': cities, 'genres': genres})



def tomorrow(request):
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    q_set = models.Gig.objects.filter(start_date=tomorrow)
    cities = []
    genres = []
    for event in q_set:
        if event.city not in cities:
            cities.append(event.city)
        for party in event.involved_parties.all():
            party_genres = party.get_genres()
            for genre in party_genres:
                if genre not in genres:
                    genres.append(genre)
    return render(request, 'web/tomorrow.html', {'gigs': q_set, 'cities': cities, 'genres': genres})

'''OLD TOMORROW FILTER
def tomorrow_filter(request):
    city = request.GET['city']
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    q_set = models.Gig.objects.filter(start_date=tomorrow)
    cities = []
    result_list = []
    for event in q_set:
        if event.city not in cities:
            cities.append(event.city)
    if city is not None or city is not 'null' or city is not '':
        for event in q_set:
            city_slug = slugify(event.city)
            if city_slug == city:
                result_list.append(event)
    else:
        result_list = q_set
    return render(request, 'web/tomorrow.html', {'gigs': result_list, 'cities': cities})
'''

def tomorrow_filter(request):
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    tomorrow_events = models.Gig.objects.filter(start_date=tomorrow)
    genre_list = []
    city_list = []
    try:
        genres = set(request.GET["genres"].split(','))
        for event in tomorrow_events:
            for party in event.involved_parties.all():
                if party.entity_type != 'Venue':
                    party_genres = [slugify(genre) for genre in party.get_genres()]
                    party_genres = set(party_genres)
                    if party_genres.intersection(genres):
                        genre_list.append(event)
    except Exception as e:
        print(e)
    try:
        city = request.GET["city"]
        for event in tomorrow_events:
            city_slug = slugify(event.city)
            if city_slug == city:
                city_list.append(event)
    except Exception as e:
        print(e)
    if city_list and genre_list:
        result = set(city_list).intersection((set(genre_list)))
    elif city_list and not genre_list:
        result = set(city_list)
    elif genre_list and not city_list:
        result = set(genre_list)
    else:
        result = set()
    ##get all cities and genres to display
    cities = []
    for event in result:
        if event.city not in cities:
            cities.append(event.city)
    genres = []
    for event in result:
        for party in event.involved_parties.all():
            party_genres = party.get_genres()
            for genre in party_genres:
                if genre not in genres:
                    genres.append(genre)
    result = list(result)
    return render(request, 'web/today.html', {'gigs': result, 'cities': cities, 'genres': genres})



def date(request, year, month, day):
    year = int(year)
    month = int(month)
    day = int(day)
    date = datetime.date(year=year, month=month, day=day)
    q_set = models.Gig.objects.filter(start_date=date)
    cities = []
    genres = []
    for event in q_set:
        if event.city not in cities:
            cities.append(event.city)
        for party in event.involved_parties.all():
            party_genres = party.get_genres()
            for genre in party_genres:
                if genre not in genres:
                    genres.append(genre)
    return render(request, 'web/date.html', {'gigs': q_set, 'cities': cities, 'year': int(year), 'month': int(month), 'day': int(day), 'genres': genres})

'''OLD DATE FILTER
def date_filter(request, year, month, day):
    city = request.GET['city']
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
    if city is not None or city is not 'null' or city is not '':
        for event in q_set:
            city_slug = slugify(event.city)
            if city_slug == city:
                result_list.append(event)
    else:
        result_list = q_set
    return render(request, 'web/date.html', {'gigs': result_list, 'cities': cities, 'year': int(year), 'month': int(month), 'day': int(day)})
'''

def date_filter(request, year, month, day):
    year = int(year)
    month = int(month)
    day = int(day)
    date = datetime.date(year=year, month=month, day=day)
    date_events = models.Gig.objects.filter(start_date=date)
    genre_list = []
    city_list = []
    try:
        genres = set(request.GET["genres"].split(','))
        for event in date_events:
            for party in event.involved_parties.all():
                if party.entity_type != 'Venue':
                    party_genres = [slugify(genre) for genre in party.get_genres()]
                    party_genres = set(party_genres)
                    if party_genres.intersection(genres):
                        genre_list.append(event)
    except Exception as e:
        print(e)
    try:
        city = request.GET["city"]
        for event in date_events:
            city_slug = slugify(event.city)
            if city_slug == city:
                city_list.append(event)
    except Exception as e:
        print(e)
    if city_list and genre_list:
        result = set(city_list).intersection((set(genre_list)))
    elif city_list and not genre_list:
        result = set(city_list)
    elif genre_list and not city_list:
        result = set(genre_list)
    else:
        result = set()
    ##get all cities and genres to display
    cities = []
    for event in result:
        if event.city not in cities:
            cities.append(event.city)
    genres = []
    for event in result:
        for party in event.involved_parties.all():
            party_genres = party.get_genres()
            for genre in party_genres:
                if genre not in genres:
                    genres.append(genre)
    result = list(result)
    return render(request, 'web/today.html', {'gigs': result, 'cities': cities, 'genres': genres})

def about(request):
    return render(request, 'web/about.html')

def howto(request):
    return render(request, 'web/howto.html')