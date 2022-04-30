
from getpass import getuser
from django.contrib import admin
from django.urls import path,include
from projectBackend import views as apiView

from projectBackend import recommendation_contentBased

from rest_framework.authtoken import views as authView

# from projectBackend.viewsets import userviewsets 
from rest_framework import routers

router = routers.DefaultRouter()
# router.register('users', userviewsets,)
# router.register('getUsers', customuserviewsets,)



urlpatterns = [  
    path('createUser/', apiView.createUser, name='createUser'),
    path('login/', apiView.signin, name='login'),
    path('logout/', apiView.signout, name='logout'),
    path('getUsers/',apiView.getuser,name="getuser"),
    path('', include(router.urls)),
    path('api-token-auth/', authView.obtain_auth_token, name='api-token-auth'),
    path('csvToJson/', apiView.make_json, name='csv-to-json'),
    path('addToFavorite/', apiView.addToFavorite, name='addToFavorite'),
    path('getLikedGame/', apiView.getLikedGame, name='getLikedGame'),
    path('removeFromFavorite/', apiView.removeFromFavorite, name='removeFromFavorite'),
    path('profile/', apiView.profile, name='profile'),
    path('recommend/', recommendation_contentBased.recommendationContentBased, name='recommend'),

]

