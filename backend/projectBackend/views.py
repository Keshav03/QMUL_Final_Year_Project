
import re
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import auth

from projectBackend.models import User , customUser 
from django.http import JsonResponse
from django.http.response import HttpResponseBadRequest
from django.contrib.auth import authenticate, login ,logout

from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework import viewsets
from .serializers import userSerializers , customUserSerializers
from rest_framework.response import Response

from django.views.decorators.csrf import csrf_exempt

from projectBackend.serializers import serializers


# Create your views here.

def getuser(request):
    userlist = []
    for user in customUser.objects.all():
        userlist.append(user.to_dict())
    return JsonResponse({
        'users': userlist
    })





class userviewsets(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = userSerializers
    print("hello world")






class customuserviewsets(viewsets.ModelViewSet):
    queryset = customUser.objects.all()
    serializer_class = customUserSerializers
    print("hello world")




@csrf_exempt
def signin(request):
    if request.user.is_authenticated:
        # Do something for authenticated users.
            print("Already logged in")
            return JsonResponse({"Message":"Already logged in","isLoggedIn": True ,"username":request.user.username}) 

    if request.method=="POST":

            username= request.POST.get("userName")
            print(username)
            password = request.POST.get("password")
            print(password)
            user = authenticate(username=username, password=password)

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
    if request.method == 'POST':
        username= request.POST.get("userName")
        firstName = request.POST.get("firstName")
        lastName = request.POST.get("lastName")
        email = request.POST.get("email")
        password = request.POST.get("password")
           # Here we do comparision to check if username exists 
        try:
            user= User.objects.get(username=username)  
            return JsonResponse({"Message":"User Exists"})
        except User.DoesNotExist:
            # create a new user
            new_user = User.objects.create(username=username)

            # set user's password
            new_user.set_password(password)
            new_user.save()
         

            print("User created")
            return JsonResponse({"Message":"User Created"})
        
    return HttpResponseBadRequest("Invalid method")
    

