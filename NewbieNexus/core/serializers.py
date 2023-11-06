from rest_framework import serializers
from core.models import Club,Interest
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    interests=serializers.SerializerMethodField()
    class Meta:
        model=User
        fields=['id','username','email','first_name','last_name','interests']

    def get_interests(self,obj):
        interests=Interest.objects.filter(is_user_interest=True,user=obj)
        serializer=InterestSerializer(interests,many=True)
        return serializer.data


class ClubSerializer(serializers.ModelSerializer):
    interests=serializers.SerializerMethodField()
    class Meta:
        model=Club
        fields='__all__'

    def get_interests(self,obj):
        interests=Interest.objects.filter(is_user_interest=False,club=obj)
        serializer=InterestSerializer(interests,many=True)
        return serializer.data


class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        fields='__all__'
        model=Interest

class InterestDetailSerializer(serializers.ModelSerializer):
    user=UserSerializer
    class Meta:
        fields='__all__'
        model=Interest

class CSVFileSerializer(serializers.Serializer):
    csv_file = serializers.FileField()