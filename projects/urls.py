from unicodedata import name
from . import views
from django.urls import path


urlpatterns = [
    path('', views.projects, name="projects"),
    path('project/<str:pk>/', views.project, name="project"),
    
    path('create-project/', views.createProject, name="create-project"),
    path('update-project/<str:pk>/', views.updateProject, name="update-project"),  
    path('delete-project/<str:pk>/', views.deleteProject, name="delete-project"),
    
    path('add-task/<str:pk>/',views.addTask, name="add-task"),
    path('update-task/<str:pk>/<str:pk1>/', views.updateTask, name="update-task"),  
    path('delete-task/<str:pk>/<str:pk1>/', views.deleteTask, name="delete-task"),
    
    path('create-permission/<str:pk>/',views.createPermission, name="create-permission"),
    path('update-permission/<str:pk>/<str:pk1>/', views.updatePermission, name="update-permission"),  
    path('delete-permission/<str:pk>/<str:pk1>/', views.deletePermission, name="delete-permission"),
]
