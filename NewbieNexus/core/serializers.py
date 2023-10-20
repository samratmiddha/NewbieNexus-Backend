from rest_framework import serializers
from core.models import Club,Interest


class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        model=Club

class InterestSerializer(serializers.ModelSerializer):
    club=ClubSerializer()
    class Meta:
        model=Interest