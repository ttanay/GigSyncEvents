from django.db import models
from django.utils.text import slugify
import json
import requests
import datetime
# Create your models here.

class GSProfile(models.Model):
    """
    Schema:
        gs_id INTEGER,
        title TEXT,
        slug TEXT,
        profile_pic TEXT,
        subcategory TEXT,
        city TEXT,
        tag TEXT,
        popular TEXT
        entity_type TEXT
    """
    gs_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    profile_pic = models.TextField(null=True)
    subcategory = models.CharField(max_length=255)
    city = models.CharField(max_length=255, null=True)
    tag = models.TextField(null=True)
    popular = models.TextField(null=True)
    entity_type = models.CharField(max_length=255)

    @classmethod
    def create(cls, gs_id, title, slug, profile_pic, subcategory, city, tag, popular, entity_type):
        gs_object = cls(gs_id=gs_id, title=title, slug=slug, profile_pic=profile_pic, subcategory=subcategory, city=city, tag=tag, popular=popular, entity_type=entity_type)

        '''
        self.gs_id = gs_id
        self.title = title
        self.slug = slug
        self.profile_pic = profile_pic
        self.subcategory = subcategory
        self.city = city
        self.tag = tag
        self.popular = popular
        self.entity_type = entity_type
       # logging.info('Creating ' + str(self.entity_type) + ' object with id = ' + str(self.ID))'''
        return gs_object

    def get_slug(self):
        return slugify(self.slug)

    def get_profile_pic_url(self):
        profile_pic_url = 'http://www.gigsync.in/uploads/profile/natural/{}'
        url = profile_pic_url.format(self.profile_pic)
        return url

    @staticmethod
    def jsonify_genres(genres):
        genres_json = json.dumps(genres)
        return genres_json

    '''def get_genres(self):
        genres = json.loads(self.genres)
        return genres'''

    def __str(self):
        print("id: " + str(self.gs_id) + "| title: " + str(self.title))
        return

'''
class Genre(models.Model):
    name = models.CharField(max_length=255)
    gs_profile = models.ForeignKey(GSProfile, on_delete=models.CASCADE)

    @classmethod
    def create(cls, name, gs_profile):
        print('Creating Genre object with name{}'.format(name))
        genre = cls(name, gs_profile)
        return genre
'''

class FBProfile(models.Model):

    gs_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=255)
    fb_profile_link = models.URLField(null=True)
    uri = models.TextField(null=True)
    fb_id = models.IntegerField(null=True)

    def __str__(self):
        return "id: {} | name: {} | URI: {} | fb_id: {}".format(self.gs_id, self.name, self.uri, self.fb_id)

    @classmethod
    def create(cls, gs_id, name, profile_link, uri, fb_id):
        fb_object = cls(gs_id=gs_id, name=name, fb_profile_link=profile_link, uri=uri, fb_id=fb_id)
        return fb_object
'''
    def __init__(self, id, name, profile_link, fb_id):
        self.id = id
        self.name = name
        self.profile_link = profile_link
        self.fb_id = fb_id
        return
'''

class Gig(models.Model):
    """
    id
    name
    place_id
    cover
    description
    start_date
    start_time
    end_date
    end_time
    city
    """
    event_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True)
    start_date = models.DateField()
    start_time = models.TimeField()
    end_date = models.DateField(default=None, null=True)
    end_time = models.TimeField(null=True)
    venue = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    cover_link = models.URLField(null=True)
    place_id = models.IntegerField(null=True)
    involved_parties = models.ManyToManyField(GSProfile)
        

    def get_start_month_abb(self):
        format = "%b"
        start_month_abb = self.start_date.strftime(format)
        return start_month_abb

    def get_start_month(self):
        format = "%B"
        start_month = self.start_date.stftime(format)
        return start_month

    def get_end_month_abb(self):
        format = "%b"
        end_month_abb = self.end_month.strftime(format)
        return end_month_abb

    def get_end_month(self):
        format = "%B"
        end_month = self.end_month.strftime(format)
        return end_month

    def get_start_date(self):
        date = self.start_date.day
        date_string = str(date)
        if date == 1:
            date_string += 'st'
        elif date == 2:
            date_string += 'nd'
        elif date == 3:
            date_string += 'rd'
        elif date >= 4 and date <= 20:
            date_string += 'th'
        elif date == 21:
            date_string += 'st'
        elif date == 22:
            date_string += 'nd'
        elif date == 23:
            date_string += 'rd'
        elif date >= 24 and date <= 30:
            date_string += 'th'
        elif date == 31:
            date_string += 'st'
        return date_string

    def get_end_date(self):
        date = self.end_date.day
        date_string = str(date)
        if date == 1:
            date_string += 'st'
        elif date == 2:
            date_string += 'nd'
        elif date == 3:
            date_string += 'rd'
        elif date >= 4 and date <= 20:
            date_string += 'th'
        elif date == 21:
            date_string += 'st'
        elif date == 22:
            date_string += 'nd'
        elif date == 23:
            date_string += 'rd'
        elif date >= 24 and date <= 30:
            date_string += 'th'
        elif date == 31:
            date_string += 'st'
        return date_string
        

    @classmethod
    def create(cls, event_id, name, description, start_date, start_time, end_date, end_time, venue, city, cover_link, place_id):
        gig = cls(
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
            place_id=place_id)
        return gig

    def __str__(self):
        return "id: {} | name: {} | date: {}".format(self.event_id, self.name, self.start_date)
        #return self.jsonify()

    def jsonify(self):
        json_obj = {
            "event_id": self.event_id,
            "name": self.name,
            "description": self.description,
            "start_date": str(self.start_date),
            "start_time": str(self.start_time),
            "end_date": str(self.end_date),
            "end_time": str(self.end_time),
            "venue": self.venue,
            "city": self.city,
            "cover_link": self.cover_link,
            "place_id": self.place_id,
        }
        json_string = json.dumps(json_obj)
        return json_string


