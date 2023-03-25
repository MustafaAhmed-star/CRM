from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    is_oraganisor = models.BooleanField(default=True)
    is_agent = models.BooleanField(default=False)  



class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    def __str__(self) :
        return self.user.username
class Lead(models.Model):
    source_choices =(
        ('YouTube','YouTube'),
        ('Google', 'Google'),
        ('Newsletter', 'Newsletter'),
    )
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    age = models.IntegerField(default=0)
    #realtion
    agent = models.ForeignKey("Agent",null=True,blank=True,on_delete=models.SET_NULL)
    oraganisation = models.ForeignKey(UserProfile,on_delete=models.CASCADE) 

    phoned = models.BooleanField(default =False)
    source = models.CharField(choices=source_choices ,max_length=100)
    profile_picture=models.ImageField(blank=True ,null=True)
    special_files = models.FileField(blank=True ,null=True)
    category = models.ForeignKey("Category",related_name="leads" , null=True,blank = True,on_delete=models.SET_NULL)
    def __str__(self)  :
        return  f"{self.first_name}  {self.last_name}"

    
class Agent(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    oraganisation = models.ForeignKey(UserProfile,on_delete=models.CASCADE)


    def __str__(self)  :
        return  self.user.username


class Category(models.Model):
    
    name=models.CharField(max_length=30) #new ,contacted ,converted,unconv
    oraganisation = models.ForeignKey(UserProfile,on_delete=models.CASCADE)


    def __str__(self):
        return self.name
    