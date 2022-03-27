from distutils.command.upload import upload
from email.policy import default
from pyexpat import model
from unicodedata import name
from django.db import models
from django.contrib.auth.models import User
import uuid

# import projects.models 
# Project = "projects.Project"

# from projects.models import Project

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True, blank= True)
    name = models.CharField(max_length=200, null=True, blank = True)
    email  = models.EmailField(null = True, blank= True)
    username = models.CharField(max_length=200, null=True, blank = False)
    short_intro = models.CharField(max_length=200, null= True, blank= True)
    bio = models.TextField(null= True, blank= True)
    profile_image = models.ImageField(null = True, blank = True, upload_to = "profiles/", default = "profiles/user-default.png")
    location = models.CharField(max_length=200, blank = True, null = True)
    social_github = models.CharField(max_length=200, null=True, blank = True)
    social_twitter = models.CharField(max_length=200, null=True, blank = True)
    social_linkedin = models.CharField(max_length=200, null=True, blank = True)
    social_youtube = models.CharField(max_length=200, null=True, blank = True)
    social_website = models.CharField(max_length=200, null=True, blank = True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default = uuid.uuid4, editable=False, primary_key=True, unique= True)

    def __str__(self) -> str:
        return str(self.name)
    
class Skill(models.Model):
    owner = models.ForeignKey(Profile, null=True, blank = True, on_delete = models.CASCADE)
    name = models.CharField(max_length=200, null=True, blank = False)
    description = models.TextField(null= True, blank = True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default = uuid.uuid4, editable=False, primary_key=True, unique= True)
    
    def __str__(self) -> str:
        return str(self.name)
    
    
# class Permission(models.Model):
#     # owner = models.ForeignKey(Profile, null=True, blank = True, on_delete = models.CASCADE)
#     project = models.ForeignKey(Project, on_delete = models.CASCADE, null= True, blank = True)
#     name = models.CharField(max_length=50, null = True, blank = True)
#     description = models.CharField(max_length=200, null = True, blank = True)
#     created = models.DateField(auto_now_add=True)
#     id = models.UUIDField(default = uuid.uuid4, editable=False, primary_key=True, unique= True)
    
#     def __str__(self):
#         return str(self.name)


class Roll(models.Model):
    ROLL_TYPE=(
        ('Supplier','Supplier'),
        ('Worker','Worker'),
        ('Customer','Customer'),
        ('Agency','Agency'),
        ('Model','Model'),
    )
    name = models.CharField( max_length=100 , blank=False, null=True, choices=ROLL_TYPE )
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True )
    
    def __str__(self) -> str:
        return str(self.name)

class Registration(models.Model):
    roll = models.ForeignKey(Roll, on_delete=models.SET_NULL, null=True, blank=False)
    
