from rest_framework import viewsets
from core.models import Club,Interest
from core.serializers import ClubSerializer,InterestSerializer,CSVFileSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
import pandas
from django.contrib.auth.models import User
from rest_framework import status



class ClubViewSet(viewsets.ModelViewSet):
    model=Club
    # permission_classes=[IsAuthenticated]
    queryset=Club.objects.all()
    serializer_class=ClubSerializer

    @action( methods=['POST'],detail=False ,url_name='upload_data_through_file/')
    def upload_data_through_file(self, request,*args,**kwargs):
        print(request.data)
        serializer =  CSVFileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        csv_file = serializer.validated_data['csv_file']
        csv_reader = pandas.read_csv(csv_file,keep_default_na=False)
        for _, row in csv_reader.iterrows():
            if(row['name']==''):
                row['name']=None
            if(row['verticals']==''):
                row['verticals']=None
            if(row['prerequisites']==''):
                row['prerequisites']=None
            if(row['description']==''):
                row['description']=None
            if(row['time']==''):
                row['time']=None

            club=Club.objects.create(name=row['name'],description=row['description'],verticals=row['verticals'],prerequisites=row['prerequisites'],time_devotion=row['time'])
            print(club)
            interests=row['interests'].split(',')
            for interest in interests:
                interest.strip()
                interest_name=interest.split('-')[0]
                interest_weight=interest.split('-')[1]
                interest=Interest.objects.create(is_user_interest=False,name=interest_name,weight=interest_weight,club=club,user=None)
        return Response("done")





class InterestViewSet(viewsets.ModelViewSet):
    model=Interest
    permission_classes=[IsAuthenticated]
    serializer_class=InterestSerializer
    queryset=Interest.objects.all()

    @action(methods=['GET'],detail=False,url_name='get_user_interests')
    def get_user_interests(self,request):
        user=request.GET.get('user')
        user=User.objects.get(id=user)
        interests=Interest.objects.filter(is_user_interest=True,user=user)
        serializer=InterestSerializer(interests,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    @action(methods=['GET'],detail=False,url_name='get_club_interests')
    def get_club_interests(self,request):
        club=request.GET.get('club')
        club=Club.objects.get(id=club)
        interests=Interest.objects.filter(is_user_interest=False,club=club)
        serializer=InterestSerializer(interests,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
        



# Create your views here.
