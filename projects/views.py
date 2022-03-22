from tkinter import CASCADE, FLAT
from asyncio import tasks
from django.contrib import messages
# import profile
from django.shortcuts import render,redirect

# Create your views here.
from django.http import HttpResponse
from django.template import context 
from .models import Project, Permission
from .forms import ProjectForm, TaskForm, ReviewForm, PermissionForm
from django.contrib.auth.decorators import login_required
#  PermissionForm,
"""
projectsList = [
    {
      'id':'1',
      'title': "Ecommerce website",
      'description' : 'Fully functional ecommerce website' 
    },
    {
      'id':'2',
      'title': "Portfoliyo website",
      'description' : 'This was a project where I built out my portfoliyo'  
    },
    {
      'id':'3',
      'title': "Social Network",
      'description' : 'Awesome open source project I am still working'  
    },
]
"""
def projects(request):
  # msg = 'Hello, you are on the projects page'
  # number = 10    context = {'message': msg, 'number': number, 'projects': projectsList}
  projects = Project.objects.all()

  context = {'projects' : projects}
  return render(request, 'projects/projects.html', context)

def project(request,pk):
  projectObj = Project.objects.get(id = pk)
  form = ReviewForm()
  tasks = projectObj.task_set.all()
  # tasks = projectObj.owner.task_set.all()
  
  if request.method == 'POST' :
    form = ReviewForm(request.POST)
    review = form.save(commit=False)
    review.project = projectObj
    review.owner = request.user.profile
    review.save()
      
    #getvotecount
    projectObj.getVoteCount
    messages.success(request, "Review has added successfully")
    return redirect('project', pk = projectObj.id)
  
  context = {'form' : form, 'project' : projectObj, 'tasks' : tasks}
  return render(request, 'projects/single-project.html', context )

# tasks = projectObj.task_set.all()
  # 'tasks' : tasks, 
  
  


@login_required(login_url = "login")
def createProject(request):
  profile = request.user.profile
  form = ProjectForm()
  
  if request.method == 'POST':
    form = ProjectForm(request.POST, request.FILES)
    if form.is_valid():
      project = form.save(commit=False)
      project.owner = profile
      project.save()
      
      return redirect("myaccount")
  context = {'form' : form}
  return render(request, "projects/project_form.html", context)


@login_required(login_url = "login")
def updateProject(request, pk):
  profile = request.user.profile
  
  project = Project.objects.get(id=pk)
  form = ProjectForm(instance=project)
  
  if request.method == 'POST':
    form = ProjectForm(request.POST, request.FILES, instance=project)
    if form.is_valid():
      form.save()
      messages.success(request, "Project has updated successfully")
      return redirect("myaccount")
  context = {'form' : form}
  return render(request, "projects/project_form.html", context)


@login_required(login_url = "login") 
def deleteProject(request,pk):
  profile = request.user.profile
  project = Project.objects.get(id=pk)
  
  if request.method == 'POST':
    project.delete()
    messages.success(request, "Project has deleted successfully")
    return redirect("myaccount")
  
  context = {'object': project}
  return render(request,"delete_object.html",context)


@login_required(login_url = "login") 
def addTask(request, pk):
  profile = request.user.profile
  project = Project.objects.get(id = pk)
  form = TaskForm()
  
  
  if request.method == 'POST':
    form = TaskForm(request.POST)
    if form.is_valid():
      task = form.save(commit=False)
      # pk = task.project.id
      # pk = task.getProjectId
      # project = profile.project_set.get(id == pk)
      task.project = project
      task.owner = profile
      task.save()
      # print(task.getProjectId)
      return redirect("myaccount")
  # print(form.getProjectId)
  # project = form.getProjectId
  
  context = {'form' : form}
  return render(request,"projects/task_form.html", context)  


@login_required(login_url="login")
def updateTask(request,pk,pk1):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    task = project.task_set.get(id=pk1)
    form = TaskForm(instance=task)
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance = task)
        if form.is_valid():
          task = form.save(commit=False)
          task.project = project
          task.save()
          messages.success(request, "Task has updated successfully")
          return redirect("myaccount")
            
    context = {'form' : form}
    return render(request, 'projects/task_form.html', context)
  
  
@login_required(login_url="login")
def deleteTask(request,pk, pk1):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    task = project.task_set.get(id=pk1)
    
    if request.method == 'POST':
        task.delete()   
        messages.success(request, "Task has deleted successfully") 
        return redirect("myaccount")
        
    context = {'object' : task}
    return render(request, 'delete_object.html', context)


@login_required(login_url = "login") 
def createPermission(request,pk):
  profile = request.user.profile
  project = profile.project_set.get(id = pk)
  projects = profile.project_set.all()
  form = PermissionForm()
  
  if request.method == 'POST':
    form = PermissionForm(request.POST)
    if form.is_valid():
      permission = form.save(commit = False)
      # permission.sender = profile
      if permission.project in projects:
        permission.sender = profile.name
        permission.project = project
        permission.save()
        messages.success(request, "permission has given successfully") 
        return redirect("myaccount")
      else:
        messages.error(request, "Please select your own project!!!")
      
    
  context = {'form': form}
  return render(request,'projects/permission_form.html', context)

@login_required(login_url="login")
def updatePermission(request,pk,pk1):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    permission = project.permission_set.get(id=pk1)
    form = PermissionForm(instance=permission)
    
    if request.method == 'POST':
        form = PermissionForm(request.POST, instance = permission)
        if form.is_valid():
          permission = form.save(commit=False)
          permission.name = permission.name
          permission.project = project
          permission.sender = profile.name
          permission.save()
          messages.success(request, "Permission has updated successfully")
          return redirect("myaccount")
            
    context = {'form' : form}
    return render(request, 'projects/permission_form.html', context)

@login_required(login_url = "login") 
def deletePermission(request,pk,pk1):
  profile = request.user.profile
  project = profile.project_set.get(id = pk)
  # projects = profile.project_set.all()
  permission = project.permission_set.get(id = pk1)
  
  if request.method == 'POST':
    permission.delete()
    messages.success(request, "permission has deleted successfully") 
    return redirect("myaccount")

  context = {'object': permission}
  return render(request,'delete_object.html', context)
  