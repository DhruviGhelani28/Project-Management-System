from tkinter.tix import Tree
from rest_framework import serializers
from projects.models import Permission, Project, Tag, Review, Task
from users.models import Profile, User


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
        

        
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    # owner = ProfileSerializer(many = False)
    # tags = TagSerializer(many = True)
    reviews = serializers.SerializerMethodField()
    # permissions = PermissionSerializer(many = True)
    # tasks = serializers.SerializerMethodField()
    class Meta:
        model = Project
        fields = ['id','owner','title','description','color_identity','featured_image','demo_link','source_link','tags','vote_total','vote_ratio','reviews']
        
    def get_reviews(self, obj):
        reviews = obj.review_set.all()
        serializer = ReviewSerializer(reviews, many = True)
        return serializer.data

    # def get_tasks(self, obj):
    #     tasks = obj.task_set.all()
    #     serializer = TaskSerializer(tasks, many = True)
    #     return serializer.data
    
class PermissionSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(many = False)
    class Meta:
        model = Permission
        fields = ['id','sender','client','project','name','description']

class TaskSerializer(serializers.ModelSerializer):
    # project = ProjectSerializer(many = False)
    # owner = ProfileSerializer(many = False)
    # tags = TagSerializer(many = True)
    class Meta:
        model = Task
        fields = ['id','owner','project','name','description']

class UserSerializer(serializers.ModelSerializer):
    # owner = ProfileSerializer(many = False)
    
    # reviews = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = '__all__'
    