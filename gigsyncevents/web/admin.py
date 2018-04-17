from django.contrib import admin
import requests, json
from . import models
# Register your models here.

class AccessTokenAdmin(admin.ModelAdmin):
    ''''
    def save_model(self, request, obj, form, change):
        at = obj.access_token
        call = "https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id={}&client_secret={}&fb_exchange_token={}".format(obj.app_id, obj.app_secret, obj.access_token)
        r = requests.get(call)
        access_json = json.loads(r.text)
        try:
            print('got new access_token')
            access_token = access_json["access_token"]
            obj.access_token = access_token
            super(AccessTokenAdmin, self).save_model(request, obj, form, change)
        except Exception as e:
            print("An error occurred")
'''
admin.site.register(models.AccessToken, AccessTokenAdmin)

class GigAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.Gig, GigAdmin)

class GSProfileAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.GSProfile, GSProfileAdmin)

class FBProfileAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.FBProfile, FBProfileAdmin)

