from django.contrib import admin
from . import models
# Register your models here.

class GigAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.Gig, GigAdmin)

class GSProfileAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.GSProfile, GSProfileAdmin)

class FBProfileAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.FBProfile, FBProfileAdmin)

