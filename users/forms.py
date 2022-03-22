from cProfile import label
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import Profile, Skill
# , Permission


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','email','username','password1','password2']
        labels = {
            'first_name' : 'Name',
        }
        
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm,self).__init__(*args, **kwargs)
        
        
        # self.fields['title'].widget.attrs.update({'class': 'input', 'placeholder':'Add Title'})
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
            
            
class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'email', 'username', 'short_intro', 'bio', 'profile_image', 'location', 'social_github', 'social_twitter', 'social_linkedin', 'social_youtube' ,'social_website']
        
    def __init__(self, *args, **kwargs):
        super(ProfileForm,self).__init__(*args, **kwargs)
        
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
            
#  , 'required' : 'True'}           

class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'description']
        
    def __init__(self, *args, **kwargs):
        super(SkillForm,self).__init__(*args, **kwargs)
        
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
            

# class PermissionForm(ModelForm):
#     class Meta:
#         model = Permission
#         fields = ['name', 'description']
        
#     def __init__(self, *args, **kwargs):
#         super(PermissionForm,self).__init__(*args, **kwargs)
        
#         for name, field in self.fields.items():
#             field.widget.attrs.update({'class': 'input'})