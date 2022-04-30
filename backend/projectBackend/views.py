
from distutils.sysconfig import get_makefile_filename
import encodings
import re

import csv
import json
import os
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import auth

from projectBackend.models import CustomUser, Game , Profile

# from django.contrib.auth.models import User

from django.http import JsonResponse
from django.http.response import HttpResponseBadRequest
from django.contrib.auth import authenticate, login ,logout
from django.contrib import auth
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework import viewsets
from rest_framework.response import Response

from django.views.decorators.csrf import csrf_exempt

from rest_framework import permissions
from rest_framework import views
from rest_framework.response import Response

from . import serializers

# Create your views here.

def getuser(request):
    userlist = []
    for user in CustomUser.objects.all():
        userlist.append(user.to_dict())
    return JsonResponse({
        'users': userlist
    })

@csrf_exempt
def signin(request):
    if request.user.is_authenticated:
        # Do something for authenticated users.
        print("Already logged in")
        return JsonResponse({"Message":"Already logged in","isLoggedIn": True ,"username":request.user.username}) 

    if request.method=="POST":
            username= request.POST.get("userName")
            password = request.POST.get("password")
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                print("Logged in")
                response = JsonResponse({"Message":"You are now logged in","isLoggedIn": True,"username":user.username})
                return response
            else:
                # Do something for anonymous users.
                print("user not found")
                return JsonResponse({"Message":"User cannot be found","isLoggedIn": False,"username":""})
    else:
        # Return an 'invalid login' error message.
        print("ERROR")
        return HttpResponseBadRequest("Invalid method")
    

@csrf_exempt
def signout(request):

    if request.user.is_authenticated:
        # Do something for authenticated users.
        logout(request)
        print("Signed Out!")
        response = HttpResponse('res')
        response.set_cookie('access_token', "")
        return JsonResponse({"Message":"Signed out","isLoggedIn": False})
    else:
        print("Not authenticated")
        return JsonResponse({"Message":"Not authenticated","isLoggedIn": False})
    
@csrf_exempt    
def createUser(request):
    if request.user.is_authenticated:
        return (redirect('/members'))


    if request.method == 'POST':
        
            username= request.POST.get("userName")
            firstName = request.POST.get("firstName")
            lastName = request.POST.get("lastName")
            email = request.POST.get("email")
            password = request.POST.get("password")

           # Here we do comparision to check if username exists 
            try:
                user= CustomUser.objects.get(username=username)  
                print(user)
                return JsonResponse({"Message":"User exists"})
            
            except CustomUser.DoesNotExist:
                
                    #create a profile
                    new_profile = Profile.objects.create(profile_username=username)
                    new_profile.save()
                    # create a new user
                    new_user = CustomUser.objects.create_user(username=username,email=email, password=password,profile=new_profile)

                    # set user's password
                    # new_user.set_password(password)
                    new_user.save()

                    # authenticate user
                    # establishes a session, will add user object as attribute
                    # on request objects, for all subsequent requests until logout
                    user = auth.authenticate(username=username, password=password)
                    if user is not None:
                        auth.login(request, user)
                        return JsonResponse({"Message":"User is logged iin"})

    return HttpResponseBadRequest("Invalid method")



def make_json(request):
    csvFilePath = os.path.dirname(os.path.abspath(__file__)) + '/datasets/vg.csv'
    with open(csvFilePath) as csvf:
         csvReader = csv.DictReader(csvf)
         data= {"gameList":[]}
         for rows in csvReader:
            data["gameList"].append(rows)
    return JsonResponse(data)

@csrf_exempt
def addToFavorite(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        platform = request.POST.get("platform")
        year = request.POST.get("year")
        if year == "":
            year = None
        genre = request.POST.get("genre")
        publisher = request.POST.get("publisher")

        user = ""
        if user == "admin1":
            gameList = CustomUser.objects.get(username=user).game_set.all()
            try:
                x1 = Game.objects.get(name=name)
                if x1 in gameList:
                    pass
                else:
                    CustomUser.objects.get(username="admin1").game_set.add(x1)
                
            except Game.DoesNotExist:
                x1 = Game.objects.create(name=name,platform=platform,year=year,genre=genre,publisher=publisher)
                if x1 not in gameList:
                    CustomUser.objects.get(username="admin1").game_set.add(x1)
        else:
            print("You need to be logged in first")
            return HttpResponse('Error handler content', status=403)

    return JsonResponse({})



@csrf_exempt
def removeFromFavorite(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        user = "admin1"
        gameList = CustomUser.objects.get(username=user).game_set.all()
        try:
            x1 = Game.objects.get(name=name)
            if x1 in gameList:
                CustomUser.objects.get(username=user).game_set.remove(x1)
                print("removed from list")
            else:
                print("not in list")
        except Game.DoesNotExist:
            print("does not exist")
        gameList = CustomUser.objects.get(username="admin1").game_set.all()
        print(gameList)

    return JsonResponse({})

def getLikedGame(request):
    response = {"games":[]}
    user = request.user
    try:
        gameList = CustomUser.objects.get(username=user).game_set.all()
        for x in gameList:
            print(x.to_dict())
            response["games"].append(x.to_dict())
    except CustomUser.DoesNotExist:
            print("user does not exist")
    # else:
    #     return JsonResponse(response)
    return JsonResponse(response)


@csrf_exempt
def profile(request):

    if request.user.is_authenticated:
        print(request.user)
        profile = Profile.objects.get(customuser=request.user)
        json = profile.to_dict()
        password = CustomUser.objects.get(username=request.user).password    

        json["password"] = password
        return JsonResponse(
            json
        )

    return JsonResponse({})
