from tkinter import Widget
from  django.forms import CheckboxSelectMultiple, ModelForm, widgets

from .models import Project, Permission, Review, Task
from django import forms
# 

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        # fields = '__all__' #you can add fileds individually which you want to add
        fields = ['title', 'description', 'featured_image', 'color_identity', 'demo_link','source_link', 'tags', 'vote_total', 'vote_ratio']
        widgets =  {
            'tags': forms.CheckboxSelectMultiple(),
            'permissions': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(ProjectForm,self).__init__(*args, **kwargs)
        
        # self.fields['title'].widget.attrs.update({'class': 'input', 'placeholder':'Add Title'})
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

# , 'permissions'      
class PermissionForm(ModelForm):
    class Meta:
        model = Permission
        fields = ['client','project','name','description']
        
    def __init__(self, *args, **kwargs):
        super(PermissionForm,self).__init__(*args, **kwargs)
        
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
            
class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description']
        
    def __init__(self, *args, **kwargs):
        super(TaskForm,self).__init__(*args, **kwargs)
        
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
            
class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['value', 'body']
        labels = {
            'value' : "Place Your Vote",
            'body': "Add Comment With Your Vote",
        }
        
    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})