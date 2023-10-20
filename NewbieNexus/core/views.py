from rest_framework import viewsets
from core.models import Club,Interest
from core.serializers import ClubSerializer,InterestSerializer
from rest_framework.permissions import IsAuthenticated



class ClubViewSet(viewsets.ModelViewSet):
    model=Club
    permission_classes=[IsAuthenticated]
    serializer_class=ClubSerializer



class InterestViewSet(viewsets.ModelViewSet):
    model=Interest
    permission_classes=[IsAuthenticated]
    serializer_class=InterestSerializer



# Create your views here.
