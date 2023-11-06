
from django.urls import path, include
from core.views import *
from rest_framework import routers

router = routers.SimpleRouter() 
router.register(r'clubs',ClubViewSet,basename='ClubViewSet')
router.register(r'interests',InterestViewSet,basename='InterestViewSet')
urlpatterns = [
    path('',include(router.urls)),
    path('whoami/',check_login),
    path('login/',login_view),
    path('get_club_recommendations/',get_club_recommendations),
    path('logout/',logout_user)
]
