from re import T
from django.db import models
from django.contrib.auth.models import AbstractUser


class Profile(models.Model):

    profile_username = models.CharField(max_length=50)
    profile_image = models.ImageField(null=True, blank=True)
    profile_email = models.EmailField(max_length=254)
    profile_gender =  models.CharField(max_length=6, blank=True)

    def to_dict(self):
        return{
            'id': self.id,
            'name': self.profile_username,
            'image': self.profile_image.url if self.profile_image else None,
            'email': self.profile_email,
            'gender': self.profile_gender,
        }

class CustomUser(AbstractUser):
    # username = models.CharField(max_length=50, unique=True)
    # email = models.EmailField(unique=True,verbose_name="Email Address")
    username = models.CharField(max_length=50, unique=True,primary_key=True)
    profile = models.OneToOneField(
        to=Profile,
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )

    # USERNAME_FIELD = "email"
    # REQUIRED_FIELDS = ["username"]

    def to_dict(self):
        return { 
            'id':self.id,
            'username':self.username, 
        }



class Game(models.Model):
    name = models.CharField(max_length=75, unique=True)
    platform = models.CharField(max_length=10,null=True)
    year= models.IntegerField(null=True)
    genre = models.CharField(max_length=50,null=True)
    publisher = models.CharField(max_length=50,null=True)

    def to_dict(self):
        return { 
            'id':self.id,
            'name': self.name,
            'platform': self.platform,
            'year':self.year,
            'genre': self.genre,
            'publisher':self.publisher 
        }