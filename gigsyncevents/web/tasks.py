from __future__ import absolute_import, unicode_literals
from celery import shared_task, task, Celery
from celery.exceptions import SoftTimeLimitExceeded
from django.utils.text import slugify

import requests, json, bs4, datetime
from . import models
from . import graph, utility


app = Celery('populate', broker='amqp://localhost')

search_url = "http://www.gigsync.in/search"

# POPUlATE APP
@shared_task
def save_gs_data(gs_id, title, slug, profile_pic, subcategory, city, tag, popular, entity_type): 

    
    gs_object = models.GSProfile.create(gs_id, title, slug, profile_pic, subcategory, city, tag, popular, entity_type)
    try:
        gs_object.save()
    except Exception as e:
        print(e)
        return
    '''
    print('genre: {}'.format(genres))
    for genre in genres:
        genre = slugify(genre)
        print('genre: {}'.format(genre))
        genre_obj = models.Genre.create(str(genre), gs_object)
        genre_obj.save()
    '''
    print('Saved GS Data: ' + str(gs_object.entity_type) + ' with id: ' + str(gs_object.gs_id))
    return 

@shared_task
def save_fb_data(gs_id, name, fb_profile_link, fb_id):
    uri = graph.strip_uri(fb_profile_link)
    fb_object = models.FBProfile.create(gs_id, name, fb_profile_link, uri, fb_id)
    try:
        fb_object.save()
    except Exception as e:
        print(e)
        return
    print('Saved FB data: ' + str(fb_object.gs_id) + ' with fb_id ' + str(fb_object.fb_id))
    return

@shared_task
def get_gs_data():
    print('started get_gs_data')
    try:
        for entity_type in utility.entity_types:
            i = 1
            while i:
                print(i)
                r = requests.post(url=search_url, data=utility.gen_form_data(i, entity_type))
                print('JSON Response:' + r.text)
                html = r.text
                entities = utility.parse_gs_data(html, entity_type)
                if entities == []:
                    break
                for entity in entities:
                    #genres = utility.get_artist_genre(entity["slug"])
                    #print('genres(tasks): {}'.format(genres))
                    save_gs_data(
                        gs_id=entity["gs_id"],
                        title=entity["title"],
                        slug=entity["slug"],
                        profile_pic=entity["profile_pic"],
                        subcategory=entity["subcategory"],
                        city=entity["city"],
                        tag=entity["tag"],
                        popular=entity["popular"],
                        entity_type=entity_type,
                        #genres=genres,
                    )
                    get_fb_data.delay(entity["gs_id"], entity["title"], entity["slug"])
                i += 1
    except SoftTimeLimitExceeded as e:
        print('SoftTimeLimitExceeded')
    return

@shared_task
def forward_fb_id(fb_id):
    r = requests.get("http://localhost:8000/fb/add_event/{}".format(fb_id))
    return

@shared_task(soft_time_limit=100000)
def get_fb_data(gs_id, title, slug):
    try:
        fb_data = utility.gen_fb_data(gs_id, title, slug)
        save_fb_data(
            gs_id=fb_data["gs_id"],
            name=fb_data["name"],
            fb_profile_link=fb_data["fb_profile_link"],
            fb_id=fb_data["fb_id"]
        )
        #forward_fb_id.delay(fb_data["fb_id"])
        print(fb_data["fb_id"])
        if fb_data["fb_id"] == "null" or fb_data["fb_id"] == None:
            return
        get_event_data.delay(fb_data["fb_id"])
    except SoftTimeLimitExceeded as e:
        print('SoftTimeLimitExceeded')
    return




# FB APP
@shared_task
def save_event(event_id, name, description, start_date, start_time, end_date, end_time, venue, city, cover_link, place_id, involved_parties):
    print('Task: save_event called: ' + name + str(start_date))
    gig = models.Gig.create(
        event_id=event_id, 
        name=name, 
        description=description, 
        start_date=start_date, 
        start_time=start_time, 
        end_date=end_date, 
        end_time=end_time, 
        venue=venue, 
        city=city, 
        cover_link=cover_link, 
        place_id=place_id
        )
    try:
        gig.save()
    except Exception as e:
        print(e)
        return
    #handle_involved_parties(involved_parties)
    q_set = models.GSProfile.objects.filter(title=venue)
    #print('VENUE SAVE QSET:' + str(q_set))
    if q_set:
        for gs_profile in q_set:
            gig.involved_parties.add(gs_profile)
    print('involved_parties: ' + str(involved_parties))
    for gs_id in involved_parties:
        gs_profiles = models.GSProfile.objects.filter(gs_id=gs_id)
        for gs_profile in gs_profiles:
            gig.involved_parties.add(gs_profile)
            print(gs_profile)
    '''
    if involved_parties:
        gs_profiles = utility.handle_involved_parties(involved_parties)
        print('gs_profiles: ' + str(gs_profiles))
        if not gs_profiles:
            for gs_profile in gs_profiles:
                gig.involved_parties.add(gs_profile)
    '''
    gig.save()
    print('saved event data ' + str(gig.event_id))
    return

@shared_task
def delete_event(event_id):
    q_set = models.Gig.objects.filter(event_id=event_id)
    gig_object = q_set[0].delete()
    print('Deleted Gig object with id: ' + event_id)
    return 

@shared_task
def get_event_data(fb_id):
    #print('EVENT DATA FOR: ' + str(fb_id))
    owners = models.FBProfile.objects.filter(fb_id=fb_id)
    owner_fb_profile_links = []
    for owner in owners:
        owner_fb_profile_link = owner.fb_profile_link
        owner_fb_profile_links.append(owner_fb_profile_link)
    user_events_json = graph.get_user_events(fb_id)
    user_events = graph.parse_user_events(user_events_json)
    for user_event in user_events:
        is_valid = graph.is_valid_event(user_event["event_id"])
        involved_parties = graph.get_involved_parties(user_event["event_id"])
        for owner_fb_profile_link in owner_fb_profile_links:
            involved_parties.append(owner_fb_profile_link)
        gs_ids = utility.filter_involved_parties(involved_parties)
        print('get_event_Data: ' + str(involved_parties))
        if is_valid:
            #get all involved parties' GSProfile
            #print('user_event["save"]' + str(user_event["save"]))
            if user_event["save"]:
                save_event(
                    event_id=user_event["event_id"],
                    name=user_event["name"],
                    description=user_event["description"],
                    start_date=user_event["start_date"],
                    start_time=user_event["start_time"],
                    end_date=user_event["end_date"],
                    end_time=user_event["end_time"],
                    venue=user_event["venue"],
                    city=user_event["city"],
                    cover_link=user_event["cover_link"],
                    place_id=user_event["place_id"],
                    involved_parties=gs_ids
                )
            '''    
            save_event.delay(event_id=user_event["event_id"],
            name=user_event["name"],
            description=user_event["description"],
            start_time=user_event["start_time"],
            end_time=user_event["end_time"],
            venue=user_event["venue"],
            city=user_event["city"],
            cover_link=user_event["cover_link"],
            place_id=user_event["place_id"])
            '''

@task 
def remove_past_events():
    q_set = models.Gig.objects.all()
    today_date = datetime.date.today()
    for event in q_set:
        if event.start_date < today_date:
            delete_event(event.event_id)
    
    print('Past Events Removed')
    return

