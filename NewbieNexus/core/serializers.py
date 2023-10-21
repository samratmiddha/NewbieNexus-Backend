from rest_framework import serializers
from core.models import Club,Interest


class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        model=Club
        fields='__all__'

class InterestSerializer(serializers.ModelSerializer):
    club=ClubSerializer()
    class Meta:
        fields='__all__'
        model=Interest

class CSVFileSerializer(serializers.Serializer):
    csv_file = serializers.FileField()