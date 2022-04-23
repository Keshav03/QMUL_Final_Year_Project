from rest_framework import serializers
from projectBackend.models import User , customUser
 
class userSerializers(serializers.ModelSerializer):
 
    class Meta:
        model = User
        # fields =  '__all__'  
        fields = ['id','username']


class customUserSerializers(serializers.ModelSerializer):
 
    class Meta:
        model = customUser
        # fields =  '__all__'  
        fields = ['id','username']