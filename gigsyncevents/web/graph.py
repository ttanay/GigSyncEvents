import requests, json, bs4, re, datetime
#from fb_id import profile_regx_accept
from .fb_credentials import access_token
from .models import GSProfile, FBProfile
from . import models

#TODO: Make API, remove occurred events


profile_regx_accept = re.compile("https:\/\/www\.facebook\.com\/.*")

accepted_page_types = {
    "Artist",
    "Band",
    "Musician/Band",
    "Musician",
    "Orchestra",
    "DJ",
    "Music Production Studio",

}

def get_user_events(fb_id):
    api_url = "https://graph.facebook.com/{}/events?access_token={}&fields=description,end_time,start_time,name,place,id,cover".format(fb_id, access_token)
    r = requests.get(api_url)
    #print(fb_id)
    #print(r.text)
    user_events_json = json.loads(r.text)
    return user_events_json


def parse_user_events(user_events_json):
    raw_json = user_events_json
    user_events = []
    try:
        for event in raw_json['data']:
            #print(event)
            event_id = event['id']
            name = event['name']
            try:
                description = event['description']
            except Exception as e:
                description = None
            #print(event['start_time'])
            try:
                print(event['end_time'])
            except Exception as e:
                print('end_time absent')
            start_dt, start_time = get_datetime_object(event['start_time'])
            try:
                end_dt, end_time = get_datetime_object(event['end_time'])
                del_time = end_dt - start_dt
                start_date = start_dt.date()
                if is_more_than_24_hrs(end_dt, start_dt):
                    end_date = end_dt.date()
                    #start_date = start_dt.date()
                else:
                    end_date = None
                    #start_date = start_dt.date()
            except Exception as e:
                print(e)
                end_date = None
                end_time = None
            venue = event['place']['name']
            city = event['place']['location']['city']
            try:
                cover_link = event['cover']['source']
            except Exception as e:
                print(e)
                cover_link = None
            place_id = event['place']['id']
            user_event = {
                "event_id": event_id,
                "name": name,
                "description": description,
                "start_date": start_date,
                "start_time": start_time,
                "end_date": end_date,
                "end_time": end_time,
                "venue": venue,
                "city": city,
                "cover_link": cover_link,
                "place_id": place_id,
                "save": is_future_event(start_dt),
            }
            user_events.append(user_event)
    except Exception as e:
        print('user_id is invalid')
    return user_events


def is_valid_event(event_id):
    #graph_event_call = "graph.facebook.com/{}?access_token={}&fields=category".format(event_id, access_token)
    event_url = "https://www.facebook.com/{}".format(event_id)
    r = requests.get(event_url)
    soup = bs4.BeautifulSoup(r.text, "lxml")
    comments = soup.find_all(string=lambda text: isinstance(text, bs4.Comment))
    hrefs = []
    for comment in comments:
        comment_soup = bs4.BeautifulSoup(str(comment), "lxml")
        anchor = comment_soup.find_all("a", {"class": "profileLink"})
        for a in anchor:
            href = a.attrs['href']
            hrefs.append(href)
    #print('hrefs: ' + str(hrefs))
    for href in hrefs:
        if is_artist(href):
            print('is_valid_event: ' + str(True))
            return True
    print('is_valid_event: ' + str(False))
    return False

def get_involved_parties(event_id):
    involved_parties = []
    event_url = "https://www.facebook.com/{}".format(event_id)
    r = requests.get(event_url)
    soup = bs4.BeautifulSoup(r.text, "lxml")
    comments = soup.find_all(string=lambda text: isinstance(text, bs4.Comment))
    hrefs = []
    for comment in comments:
        comment_soup = bs4.BeautifulSoup(str(comment), "lxml")
        anchor = comment_soup.find_all("a", {"class": "profileLink"})
        for a in anchor:
            href = a.attrs['href']
            hrefs.append(href)
    involved_parties = hrefs
    return involved_parties

def get_datetime_object(datetime_string):
    format = "%Y-%m-%dT%H:%M:%S%z"
    dt_obj = datetime.datetime.strptime(datetime_string, format)
    #date = dt_obj.date()
    time = dt_obj.time()
    return dt_obj, time

def is_more_than_24_hrs(end_dt, start_dt):
    del_time = end_dt - start_dt
    if del_time.days > 0:
        #print('is_more_than_24_hrs: ' + str(False))
        return False
    #print('is_more_than_24_hrs: ' + str(True))
    return True

def is_future_event(start_dt):
    dt_now = datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(seconds=19800)))
    if start_dt > dt_now:
        #print('is_future_event: ' + str(True))
        return True
    #print('is_future_event: ' + str(False))
    return False

def strip_uri(profile_link):
    '''
    uri = ''
    slash_count = 0
    for c in profile_link:
        if c == '/':
            slash_count += 1
            continue                                           ADD EXCEPTION HANDLER
        if slash_count == 4:
            break
        if slash_count == 3:
            uri += c
    '''
    uri = ''
    split_list = profile_link.split('/')
    try:
        if split_list[3] == 'pg':
            uri = split_list[4]
        else:
            uri = split_list[3]
    except Exception as e:
        print(e)
    print('uri:' + uri)
    return uri


def is_artist(profile_link):
    print(profile_link)
    uri = strip_uri(profile_link)
    graph_url = "https://graph.facebook.com/{}?fields=category&access_token={}".format(uri, access_token)
    #print(graph_url)
    r = requests.get(graph_url)
    raw_json = json.loads(r.text)
    #print(raw_json['category'])
    if raw_json['category'] in accepted_page_types:
        print('is_artist: ' + uri + str(True))
        return True
    else:
        print('is_artist: ' + uri + str(False))
        return False

'''def save_event(event_id, name, description, start_time, end_time, venue, city, cover_link, place_id):
    gig = models.Gig.create(event_id, name, description, start_time, end_time, venue, city, cover_link, place_id)
    gig.save()
    return'''