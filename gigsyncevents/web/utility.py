import json
import requests, re, bs4
#import
from . import models
from django.utils.text import slugify
from web import graph
entity_types = ('Artist', 'Venue', 'Agency')

id_regx_accept = re.compile("fb://page\/\?id=.*?\d*")

profile_regx_accept = re.compile("(https:\/\/?)(www\.?)facebook\.com\/.*")

defined_genres = [
    "Acoustic",
    "Alternative Rock",
    "Ambient Music",
    "Art Music",
    "Baroque Music",
    "Blues",
    "Bollywood",
    "Classical Music",
    "Country Music",
    "Covers",
    "Death Metal",
    "Dee House",
    "Deep Soul House",
    "Disco",
    "Dream Pop",
    "Drum And Bass",
    "Dub",
    "Dubstep",
    "Electro",
    "Electronic Dance Music",
    "Electronica",
    "Folk music",
    "Funk",
    "Fusion",
    "Garage Rock",
    "Gipsy Jazz",
    "Gospel Music",
    "Grunge",
    "Hardcore",
    "Punk",
    "Heavy Metal",
    "Hip Hop Music",
    "House Music",
    "Indie",
    "Indie Rock",
    "Instrumental",
    "Jazz",
    "Nu Disco",
    "Opera",
    "Orchestra",
    "Pop Music",
    "Popular Music",
    "Post Punk Revival",
    "Progressive House",
    "Progressive Rock",
    "Psychedelic Rocl",
    "Punk Rock",
    "Rap",
    "Reggae",
    "Rhythm n Blues",
    "Rock",
    "Singing",
    "Ska",
    "Soul",
    "Soul Music",
    "Sufi",
    "Sufi Rock",
    "Tech House",
    "Techno",
    "Traditional Sufi",
    "Trance",
    "Waltz World",
]

'''def store_fb_data(fb_data):
    if fb_data == None:
        return
    fb_profile = models.FBProfile.create(gs_id=fb_data["gs_id"],
                                         name=fb_data["name"],
                                         profile_link=fb_data["fb_profile_link"],
                                         fb_id=fb_data["fb_id"])
    fb_profile.save()
    return
'''

def gen_fb_data(gs_id, slug, name):
    #print('normal_slug: ' + slug)
    slug = slugify(slug)
    #print('slugified_slug: ' + slug)
    gigsync_profile_link = "http://www.gigsync.in/page/" + slug
    #print(gigsync_profile_link)
    fb_profile_link = get_fb_profile_link(gigsync_profile_link)
    try:
        fb_id = graph.get_fb_id(fb_profile_link)
    except Exception as e:
        fb_id = get_fb_id(fb_profile_link)
    if fb_id == 'null':
        fb_id = None
    fb_data = {
        "gs_id": gs_id,
        "name": name,
        "fb_profile_link": fb_profile_link,
        "fb_id": fb_id,
    }
    #print(fb_data)
    return fb_data


'''
def get_gigsync_profile_link(gs_id, slug):
    gs_id = str(gs_id)
    #sql_statement = "SELECT slug FROM profiles WHERE id=?"
    gigsync_profile_link = "http://www.gigsync.in/page/{}"
    #query_result = models.GSProfile.objects.filter(gs_id=gs_id)
    #slug = query_result[0].slug
    gigsync_profile_link = gigsync_profile_link.format(slug)
    #with conn:
        #cur = conn.cursor()
        #cur.execute(sql_statement, [id])
        #slug = cur.fetchone()
        #gigsync_profile_link = gigsync_profile_link.format(slug[0])
    #print(gigsync_profile_link)
    return gigsync_profile_link
'''


def get_fb_profile_link(gigsync_profile_link):
    r = requests.get(gigsync_profile_link)
    soup = bs4.BeautifulSoup(r.text, "lxml")
    #print(r.text)
    a = soup.find("a", {"href": profile_regx_accept})
    #print("get_fb_profile_link: " + str(a))
    if a == None:
        fb_profile_link = "null"
    else:
        fb_profile_link = a.attrs['href']
    if fb_profile_link == "https://www.facebook.com/Gigsyncindia/":
        fb_profile_link = "null"
    #print(fb_profile_link)
    return fb_profile_link


def get_fb_id(fb_profile_link):
    print(fb_profile_link)
    fb_id = str()
    if fb_profile_link == "null":
        fb_id = "null"
    else:
        r = requests.get(fb_profile_link)
        soup = bs4.BeautifulSoup(r.text, "lxml")
        meta = soup.find("meta", {"content":id_regx_accept})
        print(meta)
        if meta == None:
            fb_id = "null"
        else:
            #print(meta)
            #print(meta.attrs['content'])
            fb_id = strip_id(meta.attrs['content'])
    print(fb_id)
    return fb_id

def get_artist_genre(slug):
    gigsync_profile_link = "http://www.gigsync.in/page/{}".format(slug)
    #print(gigsync_profile_link)
    genres = []
    r = requests.get(gigsync_profile_link)
    soup = bs4.BeautifulSoup(r.text, "lxml")
    divs = soup.find_all("div", {"class": "avataarName"})
    for div in divs:
        if div.text in defined_genres:
            genres.append(div.text)
    #print('genres: {}'.format(str(genres)))
    return genres


def strip_id(uri):
    ID = ''
    uri = uri[::-1]
    for c in uri:
        if c == '=' or c == '/':
            break
        else:
            ID += c
    ID = ID[::-1]
    #print('strip_id: ' + ID)
    return ID


'''def store_GS_data(GS_data):
    if GS_data == None:
        return
    GS_profile = models.GSProfile.create(ID=GS_data.ID,
                                         title=GS_data.title,
                                         slug=GS_data.slug,
                                         profile_pic=GS_data.profile_pic,
                                         subcategory=GS_data.subcategory,
                                         city=GS_data.city,
                                         tag=GS_data.tag,
                                         popular=GS_data.popular,
                                         entity_type=GS_data.entity_type)
    GS_profile.save()
    return'''


def gen_form_data(page, entity_type):
    if entity_type == 'Artist':
        data = {
            "data[0][field]": "min",
            "data[0][value]": "0",
            "data[1][field]": "max",
            "data[1][value]": "1000",
            "category": "artists",
            "page": str(page),
        }
    elif entity_type == 'Venue':
        data = {
            "category": "venues",
            "page": str(page),
        }
    else:
        data = {
            "category": "agencies",
            "page": str(page),
            }
    #logging.info('Form page: ' + str(page))
    return data


def parse_gs_data(json_data, entity_type):
    #print(json_data)
    raw_data = json.loads(json_data)
    entities = []
    for data in raw_data["pages"]:
        entity = {
            "gs_id": data["id"],
            "title": data["title"],
            "slug": data["slug"],
            "profile_pic": data["profile_pic"],
            "subcategory": data["subcategory"],
            "city": data["city"],
            "tag": data["tag"],
            "popular": data["popular"],
        }
        '''object = models.GSProfile(
            gs_id=int(entity["id"]),
            title=entity["title"],
            slug=entity["slug"],
            profile_pic=entity["profile_pic"],
            subcategory=entity["subcategory"],
            city=entity["city"],
            tag=entity["tag"],
            popular=entity["popular"],
            entity_type=entity_type
        )
        object.save()'''
        entities.append(entity)
        #logging.info('Parsed : ' + entity.__str__())
    #logging.info('Parsed ' + str(len(entities)) + ' ' + str(entity_type) + ' data')
        #print(entity["gs_id"])
    return entities


'''
    def load_entities():
    entities = models.GSProfile.objects.all()
    return entities
'''

def gen_tuple(entities):
    batch_data = []
    for entity in entities:
        data = (
            entity.gs_id,
            entity.title,
            entity.slug,
            entity.profile_pic,
            entity.subcategory,
            entity.city,
            entity.tag,
            entity.popular,
            entity.entity_type
        )
        batch_data.append(data)
        #logging.info('Created tuple: ' + str(data[0]))
    #logging.info('Batched ' + str(len(batch_data)) + ' ' + str(entity_type) + ' data')
    return batch_data

def cleanse_fb_profile_link(fb_profile_link):
    uri = graph.strip_uri(fb_profile_link)
    clean_fb_profile_link = 'https://www.facebook.com/{}'.format(uri)
    return clean_fb_profile_link

def party_exists_in_db(uri):
    q_set = models.FBProfile.objects.filter(uri=uri)
    if q_set:
        return q_set[0]
    else:
        return False

def handle_involved_parties(involved_parties):
    #print('~~~~~~~~~~~~~~~~~~~~')
    #print(involved_parties)
    #print('~~~~~~~~~~~~~~~~~~~~')
    gs_profiles = []
    for fb_profile_link in involved_parties:
        #fb_profile_link = cleanse_fb_profile_link(fb_profile_link)
        #print('cleanse: ' + fb_profile_link)
        uri = graph.strip_uri(fb_profile_link)
        #print('handle URI: ' + uri)
        fb_profile = party_exists_in_db(uri)
        if fb_profile:
            q_set = models.GSProfile.objects.filter(gs_id=fb_profile.gs_id)
            #print(q_set)
            gs_profiles.append(q_set[0])
    #print(gs_profiles)
    return gs_profiles

def filter_involved_parties(involved_parties):
    gs_ids = []
    for fb_profile_link in involved_parties:
        uri = graph.strip_uri(fb_profile_link)
        q_set = models.FBProfile.objects.filter(uri=uri)
        for result in q_set:
            gs_ids.append(result.gs_id)
    return gs_ids