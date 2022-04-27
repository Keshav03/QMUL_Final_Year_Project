from telnetlib import GA
from django.contrib import admin
from projectBackend.models import User ,Profile, Game


# Register your models here.
admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Game)