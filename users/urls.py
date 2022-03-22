from django.urls import path
from django.conf.urls import url
from . import views


urlpatterns = [
    path('login/', views.loginUser, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerUser, name="register"),
    path('myaccount/', views.userAccount, name="myaccount"),
    path('editaccount/', views.editAccount, name="editaccount"),
    path('create-skill/', views.createSkill, name="create-skill"),
    
    
    
    path('',views.Profiles, name='profiles'),
    path('user-profile/<str:pk>/', views.userProfile, name= 'user-profile'),
    path('update-skill/<str:pk>/', views.updateSkill, name="update-skill"),
    path('delete-skill/<str:pk>/', views.deleteSkill, name="delete-skill"),
]
