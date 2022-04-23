from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    username = models.CharField(max_length=50, unique=True)
    # firstName = models.CharField(max_length=50)
    # lastName = models.CharField(max_length=50)
    # email = models.CharField(max_length=30,unique=True)

    # profile = models.OneToOneField(
    #     to=Profile,
    #     blank=True,
    #     null=True,
    #     on_delete=models.CASCADE
    # )

    def to_dict(self):
        return { 
            'id':self.id,
            'username':self.username, 
        }


class customUser(models.Model):
    username = models.CharField(max_length=50, unique=True)
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    email = models.CharField(max_length=30,unique=True)

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
    name = models.CharField(max_length=50, unique=True)
    year_of_release = models.IntegerField()
    genre = models.CharField(max_length=50)
    publisher = models.CharField(max_length=50)
    developer = models.CharField(max_length=50)


    def to_dict(self):
        return { 
            'id':self.id,
            'name': self.name,
            'year':self.year_of_release,
            'genre': self.genre,
            'publisher': self.publisher,
            'developer':self.developer 
        }