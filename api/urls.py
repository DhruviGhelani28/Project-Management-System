from django.urls import path
from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)



urlpatterns = [
    
    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('',views.getRoutes),
    path('projects/',views.getpostdeleteProjects),
    path('projects/<str:pk>/',views.getputdeleteProject),
    
    path('projects/<str:pk>/tasks/',views.getpostTasks),
    path('projects/tasks/<str:pk>/<str:pk1>/',views.getputdeleteTask),
    
    path('projects/<str:pk>/<str:pk1>/',views.shareProject),
    
    path('users/',views.getUsers),
    path('users/<str:pk>/',views.getUser),
    path('projects/<str:pk>/vote/',views.projectvote),
    # path('projects/<str:pk>/task/',views.projecttask),
    # path('projects/',views.createProject),
    
]
