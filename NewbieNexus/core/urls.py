
from django.urls import path, include
from core.views import *
from rest_framework import routers

router = routers.SimpleRouter() 
router.register(r'club',ClubViewSet,basename='ClubViewSet')
router.register(r'interests',InterestViewSet,basename='InterestViewSet')
urlpatterns = [
    path('',include(router.urls))
]
