from django.db import models
from django.contrib.auth.models import User


class Club(models.Model):
    profile_picture=models.ImageField(upload_to="images/",blank=True,null=True)
    name=models.CharField(max_length=255)
    description=models.TextField(blank=True,null=True)
    verticals=models.TextField(blank=True,null=True)
    prerequisites=models.TextField(blank=True,null=True)
    time_devotion=models.IntegerField(blank=True,null=True)

class Interest(models.Model):
    is_user_interest=models.BooleanField()
    name=models.CharField(max_length=255)
    weight=models.IntegerField()
    club=models.ForeignKey(Club,on_delete=models.CASCADE,related_name='interesets',null=True,blank=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='interests',null=True,blank=True)









    






