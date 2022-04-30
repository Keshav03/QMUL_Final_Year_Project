from telnetlib import GA
from django.contrib import admin
from projectBackend.models import CustomUser, Profile, Game

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Profile)
admin.site.register(Game)