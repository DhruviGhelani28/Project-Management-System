from queue import Empty
from unicodedata import name
from urllib import response
from django.http import JsonResponse
from django.urls import is_valid_path
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status

from projects.views import project
from .serializers import PermissionSerializer, ProjectSerializer, UserSerializer, TaskSerializer
from projects.models import Project, Review, Permission, Task
from users.models import Profile
from django.contrib.auth.models import User

from api import serializers


@api_view(['GET'])
def getRoutes(request):
    routes = [
        {'GET' : 'api/projects'},#for projects get, create project, delete all pro
        {'POST' : 'api/projects'},
        {'DELETE': 'api/projects'},
        
        {'GET' : 'api/projects/id'},# for single project get, update pro, delete pro
        {'PUT' : 'api/projects/id'},
        {'DELETE' : 'api/projects/id'},

        # {'GET' : 'api/projects/id'},# for single project get, update pro, delete pro
        # {'PUT' : 'api/projects/id'},
        # {'DELETE' : 'api/projects/id'},
        
        {'POST' : 'api/project/id/tasks'},# for all task of project get, create task
        {'GET' : 'api/projects/id/tasks'},
        {'GET' : 'api/projects/tasks/id/id1'},# for get task of single project, update, delete
        {'PUT' : 'api/projects/tasks/id/id1'},
        {'DELETE' : 'api/projects/tasks/id'},
        
        {'POST': 'api/projects/id/vote'},# for vote update
        # {'GET': 'api/projects/id/task'},
        
        {'POST' : 'api/projects/id/id1'},# for sharing project
        
        {'POST': 'api/users/token'},# for user token
        # {'POST': 'api/users/token/refresh'},
    ]
    
    return Response(routes)
    # return JsonResponse(routes, safe=False)
    
@api_view(['GET', 'POST','DELETE'])
@permission_classes([IsAuthenticated])
def getpostdeleteProjects(request):
    client = request.user.profile
    # print('User:', request.user)
    if request.method == 'GET':
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many = True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        data = request.data
        project = Project(owner = client)
        serializer = ProjectSerializer(project, data = data)
        if serializer.is_valid():
            serializer.owner = client
            print(serializer.owner)
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        
    # if request.method == 'DELETE':
    #     if client == IsAdminUser:
    #         count = Project.objects.all().delete()
    #         return Response({'message' : '{} Projects were deleted successfully!'.format(count[0]) }, status= status.HTTP_204_NO_CONTENT)
    #     else:
    #        return Response({'message' : 'Sorry, You can\'t delete projects!'})

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def getputdeleteProject(request, pk):
    client = request.user.profile
    project = Project.objects.get(id=pk)
    # permission = Permission.objects.get(id = pk)
    # print(permission)
    if request.method == 'GET':
        serializer = ProjectSerializer(project, many=False)
        return Response(serializer.data)
    
    if request.method == 'PUT':
        # project = Project.objects.get(id=pk)
        # project.owner = project.owner
        if client==project.owner or client.name in project.clients:
            # print(project.owner.name)
            # print(project.clients)
            data = request.data
            if "Edit" in project.permissions:
               
                serializer = ProjectSerializer(project, data = data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message' : 'Sorry, You have no permission to update project!'})
        else:
            return Response({'message' : 'Sorry, You can\'t update project!'})
        
        
    if request.method == 'DELETE':  
        if client == project.owner or client in project.clients:
            project.delete()
            return Response({'message' : 'Project was deleted successfully!'}, status = status.HTTP_204_NO_CONTENT)   
        else:
            return Response({'message' : 'Sorry, You can\'t delete project! because you are nor owner of roject and and permitted user'})     

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUsers(request):
    # print('User:', request.user)
    users = User.objects.all()
    serializer = UserSerializer(users, many = True)
    return Response(serializer.data)

@api_view(['GET'])
def getUser(request, pk):
    user = User.objects.get(id=pk)
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def projectvote(request, pk):
    project = Project.objects.get(id = pk)
    user = request.user.profile
    data = request.data
    print("DATA: ", data)
    
    review, created = Review.objects.get_or_create(
        owner  = user,
        project = project,
    )
    
    review.value = data['value']
    review.save()
    project.getVoteCount
    
    serializer = ProjectSerializer(project, many = False)
    return Response(serializer.data)

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def projecttask(request, pk):
#     project = Project.objects.get(id = pk)
#     user = request.user.profile
#     data = request.data
#     print("DATA: ", data)
    
#     task = Task.objects.get(
#         owner  = user,
#         project = project,
#     )
    
#     task.name = data['name']
#     task.save()
#     # project.clients
    
#     serializer = TaskSerializer(task, many = False)
#     return Response(serializer.data)

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def getpostTasks(request,pk):
    client = request.user.profile
    project = Project.objects.get(id =pk)
    # print(tasks)
    
    if request.method == 'GET':
        tasks = Task.objects.filter(project = project)
        serializer = TaskSerializer(tasks,many = True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        if client == project.owner or client.name in project.clients:
            data = request.data
            task = Task(project=project)
            serializer = TaskSerializer(task, data = data)
            if serializer.is_valid():
                if client == project.owner:
                    task.owner = project.owner
                else:
                    task.owner = client
                serializer.save()
                return Response(serializer.data, status = status.HTTP_201_CREATED)
            return Response(serializer.data, status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message' : 'Sorry, You can\'t create task because authorisation has given to project owner and permitted user!'})
    
@api_view(['GET','PUT','DELETE'])
@permission_classes([IsAuthenticated])
def getputdeleteTask(request, pk,pk1):
    client = request.user.profile
    project = Project.objects.get(id = pk)
    task = Task.objects.get(id = pk1)
    print(task.project)
    print(task)
    data = request.data

    if request.method == 'GET':
        serializer = TaskSerializer(task, many = False)
        return Response(serializer.data)
    
    if request.method == 'PUT':
        if client == project.owner or client.name in project.clients:
            if "Edit" in project.permissions:
                # task = Task.objects.get(id=pk)
                serializer = TaskSerializer(task, data = data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.data, status = status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message' : 'Sorry, You have no permission to update project!'})
        else:
            return Response({'message' : 'Sorry, You can\'t update project and also its tasks!'},status = status.HTTP_401_UNAUTHORIZED)
        
    if request.method == 'DELETE':
        if client == project.owner or client.name in project.clients:
            task.delete()
            tasks = project.task_set.all()
            serializer = TaskSerializer(tasks, many = True)
            return Response(serializer.data)
        else:
            return Response({'message' : 'Sorry, You can\'t delete the task because authorisation has given to project owner and permitted user!!'}, status = status.HTTP_401_UNAUTHORIZED)




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def shareProject(request, pk, pk1): #1st arg = project.id, 2nd arg = profile.id
    client = request.user.profile
    project = Project.objects.get(id=pk)
    reciever = Profile.objects.get(id=pk1)
    data  = request.data
    permissions = project.permissions
    print(permissions)

    if request.method == 'POST':
        if client == project.owner:
            return Response({'message' : 'You can share project!!'})
                   
        elif  client.name in project.clients:
            permission = project.permission_set.filter(client= client)
            print(permission)
            permission1 = client.permission_set.all().values_list('name', flat=True)
            print(permission1)
            if "Share" in permission1:
                print("share is there for client")
                # permission.name = "Share"
                # permission.sender = project.owner
                # permission.project = project
                # permission.client = client
                serializer = PermissionSerializer(permission, data = data)
                if serializer.is_valid():    
                    serializer.save()
                    return Response(serializer.data)
                return Response({'message':'Share permission has given'})

            else:
                # permission = project.permission_set.get(client = client)
                permission.delete()
                # permission.name =  "Share"
                print("share is not there so deleted it for client")
                permission = Permission.objects.create(
                    sender = project.owner,
                    project = project,
                    client = client,
                    name = "Share"
                )
                
                serializer = PermissionSerializer(permission, data=data)

                if serializer.is_valid():
                    print("project owner permission create for client")
                    serializer.save()
                    return Response(serializer.data)
                return Response({'message':'Share permission has given'})
                
        else:
            # if permissions is Empty:
            #     print(project.permissions)
            print("client has no any permission so create")
            # permission = Permission(project=project)
            
                # permission.name = "share"
                # permission.sender = client
                # permission.project = project
                # permission.client = reciever

            permission = Permission.objects.create(
                    sender = project.owner,
                    project = project,
                    client = client,
                    name = "Share"
                )
            serializer = PermissionSerializer(permission, data=data)
            print(serializer,"-----------------")
            print("permission created")
            if serializer.is_valid():
                print("---------here")
                serializer.save()
                return Response(serializer.data)
            return Response({'message':'There was not any permisson, so created it for client!!!'})
    

# @api_view(['GET', 'PUT', 'DELETE'])
# @permission_classes([IsAuthenticated])
# def getputdeletePermission(request, pk, pk1):
#     client = request.user.profile
#     project = Project.objects.get(id=pk)
#     permission = Permission.objects.get(id = pk1)
#     # print(permission)
#     if request.method == 'GET':
#         serializer = PermissionSerializer(permission, many=False)
#         return Response(serializer.data)
    
#     if request.method == 'PUT':
#         # project = Project.objects.get(id=pk)
#         # project.owner = project.owner
#         if client==project.owner or client.name in project.clients:
#             # print(project.owner.name)
#             # print(project.clients)
#             data = request.data
#             if "Edit" in project.permissions:
               
#                 serializer = ProjectSerializer(project, data = data)
#                 if serializer.is_valid():
#                     serializer.save()
#                     return Response(serializer.data)
#                 return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
#             else:
#                 return Response({'message' : 'Sorry, You have no permission to update project!'})
#         else:
#             return Response({'message' : 'Sorry, You can\'t update project!'})
        
        
#     if request.method == 'DELETE':  
#         if client == project.owner or client in project.clients:
#             project.delete()
#             return Response({'message' : 'Project was deleted successfully!'}, status = status.HTTP_204_NO_CONTENT)   
#         else:
#             return Response({'message' : 'Sorry, You can\'t delete project! because you are nor owner of roject and and permitted user'}) 
