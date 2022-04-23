from rest_framework import viewsets
from .serializers import userSerializers ,customUserSerializers
from projectBackend.models import User ,customUser
 
 
class userviewsets(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = userSerializers


class customuserviewsets(viewsets.ModelViewSet):
    queryset = customUser.objects.all()
    serializer_class = customUserSerializers
    print("hello world")