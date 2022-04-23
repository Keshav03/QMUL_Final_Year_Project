
from getpass import getuser
from django.contrib import admin
from django.urls import path,include
from projectBackend import views as apiView

from rest_framework.authtoken import views as authView

from projectBackend.viewsets import userviewsets , customuserviewsets
from rest_framework import routers

router = routers.DefaultRouter()
router.register('users', userviewsets,)
# router.register('getUsers', customuserviewsets,)



urlpatterns = [  
    path('createUser/', apiView.createUser, name='createUser'),
    path('login/', apiView.signin, name='login'),
    path('logout/', apiView.signout, name='logout'),
    path('getUsers/',apiView.getuser,name="getuser"),
    path('', include(router.urls)),
    path('api-token-auth/', authView.obtain_auth_token, name='api-token-auth'),

]