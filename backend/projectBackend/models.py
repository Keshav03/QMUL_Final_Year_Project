from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    def to_dict(self):
        return { 
            'id':self.id,
            'username':self.username, 
        }

class Profile(models.Model):
    fullname = models.CharField(max_length=50, unique=True)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    gender = models.CharField(max_length=30,unique=True)
    username = models.CharField(max_length=30,unique=True)
    interest = models.CharField(max_length=30,unique=True)


    def to_dict(self):
        return { 
            'id':self.id,
            'fullname': self.fullname,
            'username':self.username, 
        }

class Game(models.Model):
    name = models.CharField(max_length=75, unique=True)
    platform = models.CharField(max_length=10,null=True)
    year= models.IntegerField(null=True)
    genre = models.CharField(max_length=50,null=True)
    publisher = models.CharField(max_length=50,null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def to_dict(self):
        return { 
            'id':self.id,
            'name': self.name,
            'platform': self.platform,
            'year':self.year,
            'genre': self.genre,
            'publisher':self.publisher 
        }