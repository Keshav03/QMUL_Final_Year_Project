
from distutils.sysconfig import get_makefile_filename
import email
from email.header import Header
import encodings
from pickletools import read_uint1
import re

import pandas as pd

import csv
import json
import os
from webbrowser import get
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



# def get_game_rated(request):
#     '''Function to get game rated by user  '''
#     gamecsvFilePath = os.path.dirname(os.path.abspath(__file__)) + '/datasets/vg.csv'

#     ratingcsvFilePath = os.path.dirname(os.path.abspath(__file__)) + 'gameUserRatings.csv'

   

#     with open(gamecsvFilePath) as csvf:
#          csvReader = csv.DictReader(csvf)
#          data= {"gameList":[]}
#          for rows in csvReader:
#             data["gameList"].append(rows)
#     return JsonResponse(data)



@csrf_exempt
def rateGame(request):

    if request.method == "POST":
        gameid = request.POST.get("gameid")
        print(gameid)
        rating =  request.POST.get("rating")
        print(rating)

        if request.user.is_authenticated:
            ratingcsvFilePath = os.path.dirname(os.path.abspath(__file__)) + '/datasets/gameUserRatings.csv'
            user = request.user
            user= CustomUser.objects.get(username = user)
            userid = user.to_dict()["id"]
            data = []
            data.append(userid)
            data.append(gameid)
            data.append(rating)

            with open(ratingcsvFilePath) as csvf:
                ratingcsvReader = csv.DictReader(csvf)
                i= 0
                for rows in ratingcsvReader:
                    if(int(rows["gameid"])==int(gameid) and int(rows["userid"]) == int(userid) ):
                        print("in here")
                        df =  pd.read_csv(ratingcsvFilePath)
                        df.loc[i,"rating"] = rating
                        df.to_csv(ratingcsvFilePath,index=False)
                        return JsonResponse({})
                    i +=1
            
            with open(ratingcsvFilePath,'a',encoding='UTF-8',newline='') as f:
                writer = csv.writer(f) 
                writer.writerow(data)

    return JsonResponse({})

def make_json(request):

    if request.user.is_authenticated:
        gamecsvFilePath = os.path.dirname(os.path.abspath(__file__)) + '/datasets/vg.csv'        
        ratingcsvFilePath = os.path.dirname(os.path.abspath(__file__)) + '/datasets/gameUserRatings.csv'

        user = request.user
        user= CustomUser.objects.get(username = user)
        userid = user.to_dict()["id"]
        print(userid)

        data= {"gameList":[]}

        with open(gamecsvFilePath) as csvf:
                gamecsvReader = csv.DictReader(csvf)
                temp = 0
                for rows1 in gamecsvReader:

                    with open(ratingcsvFilePath) as csvf:
                        ratingcsvReader = csv.DictReader(csvf)
                        for rows2 in ratingcsvReader:
                            if(userid == int(rows2["userid"])):
                                if(int(rows2["gameid"])==int((rows1["gameid"]))):
                                    temp = int(rows2["rating"])
                                    print("ratings :" + str(rows2["rating"]))

                    rows1["rating"] = temp
                    data["gameList"].append(rows1)
                    temp = 0

        # with open(gamecsvFilePath) as csvf:
        #     csvReader = csv.DictReader(csvf)
        #     data= {"gameList":[]}
        #     for rows in csvReader:
        #         print(rows["gameid"])
        #         data["gameList"].append(rows)
        
    return JsonResponse(data)

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

    if request.method == "GET":

        if request.user.is_authenticated:
            profile = Profile.objects.get(customuser=request.user)
            json = profile.to_dict()
            return JsonResponse(
                json
            )

    if request.method == "POST":

        if request.user.is_authenticated:
            username = request.POST.get("name")
            gender = request.POST.get("gender")

            try:
                profile = Profile.objects.get(customuser=request.user)
                profile.profile_username = username
                profile.profile_gender = gender
                profile.save()
                
                return JsonResponse(
                    profile.to_dict()
                )
            except:
                return HttpResponseBadRequest()

    return JsonResponse({"test":"test"})
