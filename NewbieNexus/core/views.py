from rest_framework import viewsets
from core.models import Club,Interest
from core.serializers import ClubSerializer,InterestSerializer,CSVFileSerializer,UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action,api_view,permission_classes
from rest_framework.response import Response
import pandas
from django.contrib.auth.models import User
from rest_framework import status
from django.contrib.auth import login,authenticate,logout
from django.shortcuts import redirect
from django.http import HttpResponse
from core.constants import INTEREST_OPTIONS
from core.utils.getClubRecommendations import getClubRecommendations
from core.utils.getMostSimilarInterest import getMostSimilarInterest


@api_view(('GET',))
@permission_classes([])
def check_login(request):
    content = {'Logged_In': False}
    if request.user.is_authenticated:
        serializer = UserSerializer(request.user)
        content = {'Logged_In': True, 'user': serializer.data}

    return Response(content)


@api_view(('POST',))
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse('Login successful')
        else:
            return HttpResponse('Login failed')
    return HttpResponse('Login failed')

@api_view(('GET',))
def get_club_recommendations(request):
    user=request.GET.get('user')
    ans=getClubRecommendations(user)
    return Response(ans,status=status.HTTP_200_OK)


@api_view(('GET',))
def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        return Response("user logged out Successfully")
    




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
    # permission_classes=[IsAuthenticated]
    serializer_class=InterestSerializer
    queryset=Interest.objects.all()

    def create(self,request,*args, **kwargs):
        try:
             interest_string=request.data["interests"]
        except:
            response = super().create(request, *args, **kwargs)
            return Response({"msg":"done"},status=status.HTTP_201_CREATED)

        interests=interest_string.split(',')
        interests=[obj.strip() for obj in interests]
        interests=[getMostSimilarInterest(obj) for obj in interests]
        user_interests=Interest.objects.filter(is_user_interest=True,user=request.data["user"])
        serializer=InterestSerializer(user_interests,many=True)
        user_interests_names=[obj["name"] for obj in serializer.data]
        new_interests=[interest for interest in interests if interest not in user_interests_names]
        for interest in new_interests:
            Interest.objects.create(name=interest,is_user_interest=True,user=request.user,weight=2)
        
        return Response("Successyfully Created",status=status.HTTP_201_CREATED)
        
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
    
    @action(methods=['GET'],detail=False,url_name='get_all_interests')
    def get_all_interests(self,request):
        user=request.GET.get('user')
        user=User.objects.get(id=user)
        interests=Interest.objects.filter(is_user_interest=True,user=user)
        serializer=InterestSerializer(interests,many=True)
        user_interests = [obj["name"] for obj in serializer.data]
        interest_array=[]
        for interest in serializer.data:
            interest_array.append({
                    'id':interest["id"],
                    'name':interest["name"],
                    'user_interest':True,
                })
        for interest in INTEREST_OPTIONS:
            if(interest not in user_interests):
                interest_array.append({
                    'name':interest,
                    'user_interest':False,
                })

        return Response(interest_array,status=status.HTTP_200_OK)


        



# Create your views here.
