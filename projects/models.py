from email.policy import default
from random import choices
from tkinter import CASCADE, FLAT
from django.db import models
from users.models import Profile
# from django.db.models.fields import UUIDField
# from django.db.models.fields.related import create_many_to_many_intermediary_model
import uuid

# Create your models here.

class Project(models.Model):
    owner = models.ForeignKey(Profile, on_delete= models.SET_NULL, null= True, blank = True)
    title = models.CharField(max_length=200, null = True, blank = False)
    description = models.TextField(null=True, blank=True)
    # , max_length=200, editable=False)
    color_identity = models.CharField(null=True, blank=True, max_length=50)
    featured_image = models.ImageField(null=True, blank=True, default = "default.jpg")
    demo_link = models.CharField(null=True, blank=True, max_length=2000)
    source_link = models.CharField(null=True, blank=True, max_length=2000)
    tags = models.ManyToManyField('Tag', blank=True)
    vote_total = models.IntegerField(default = 0, null = True, blank = True)
    vote_ratio = models.IntegerField(default = 0, null = True, blank = True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default = uuid.uuid4, editable=False, primary_key=True, unique= True)
    
    def __str__(self) -> str:
        return str(self.title)
    
    @property
    def getVoteCount(self):
        reviews = self.review_set.all()
        upvote = reviews.filter(value = 'up').count()
        totalvote = reviews.count()
        
        self.vote_total = totalvote
        self.vote_ratio = (upvote / totalvote)*100
        self.save()
        
    @property
    def reviewers(self):
        allreviwers = self.review_set.all().values_list('owner__id', flat = True)
        return allreviwers

    @property
    def clients(self):
        allclients = self.permission_set.all().values_list('client__name', flat = True)
        return allclients

    @property
    def permissions(self):
        allpermission = self.permission_set.all().values_list('name', flat = True)
        return allpermission
        
    class Meta:
        # ordering = ['created']
       ordering = ['-vote_ratio', '-vote_total', 'title'] 
 

class Review(models.Model):
    VOTE_TYPE = (
        ('up','Up Vote'),
        ('down','Down Vote'),
    )
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null = True, blank = True)
    project = models.ForeignKey(Project, on_delete= models.CASCADE, null = True, blank= True)
    body = models.TextField(null=True, blank = True)
    value = models.CharField(max_length=200, choices = VOTE_TYPE)
    created = models.DateField(auto_now_add=True)
    id = models.UUIDField(default = uuid.uuid4, editable=False, primary_key=True, unique= True)
    
    
    class Meta:
        unique_together = [['owner', 'project']]
        
    def __str__(self):
        return str(self.value)

    
class Permission(models.Model):
    PERMISSION_TYPE=(
        ('Edit','Edit permission'),
        ('Share','Share permission'),
        ('Delete','Delete permission'),
    )
    sender = models.CharField(max_length=50, null = True, blank = True)
    client = models.ForeignKey(Profile, null=True, blank = False, on_delete = models.CASCADE)
    project = models.ForeignKey(Project, null= True, blank = False, on_delete = models.CASCADE)
    name = models.CharField(max_length=50, null = True, blank = False, choices= PERMISSION_TYPE)
    description = models.CharField(max_length=200, null = True, blank = True)
    created = models.DateField(auto_now_add=True)
    id = models.UUIDField(default = uuid.uuid4, editable=False, primary_key=True, unique= True)
    
    class Meta:
        unique_together = [['client', 'project']]

    def __str__(self):
        return str(self.name)
    
class Tag(models.Model):
    name= models.CharField(max_length=200)
    created = models.DateField(auto_now_add=True)
    id = models.UUIDField(default = uuid.uuid4, editable=False, primary_key=True, unique= True)
    
    def __str__(self):
        return self.name


class Task(models.Model):
    owner = models.ForeignKey(Profile, null=True, blank = True, on_delete = models.CASCADE)
    project = models.ForeignKey(Project, null= True, blank = True, on_delete= models.CASCADE)
    name = models.CharField(max_length=200, null=True, blank = False)
    description = models.TextField(null= True, blank = True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default = uuid.uuid4, editable=False, primary_key=True, unique= True)
    
    def __str__(self) -> str:
        return str(self.name)
    
    # @property
    # def getProjectId(self):
    #     project = self.project
    #     return project


# @property
    # def clients(self):
    #     allclients = self.profile_set.all().values_list('client__id', FLAT = True)
    #     return allclients

    # @property
    # def permissions(self):
    #     allpermission = self.permission_set.all().values_list('name', FLAT = True)
    #     return allpermission