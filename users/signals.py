from django.db.models.signals import post_save, post_delete
from .models import Profile
from django.contrib.auth.models import User
from django.dispatch import receiver

# @receiver(post_save, sender = "Profile")
def createProfile(sender, instance, created, **kwargs):
    print("Profile triger")
    if created:
        user = instance
        profile = Profile.objects.create(
            user = user,
            username = user.username,
            email = user.email,
            name = user.first_name,
            
        )
        
def deleteUser(sender, instance, **kwargs):
    # print("Deleting user")
    user = instance.user
    user.delete()

def updateUser(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user
    if created == False:
        user.first_name = profile.name
        user.email = profile.email
        user.username = profile.username
        user.save()
        

post_save.connect(createProfile, sender = User)
post_delete.connect(deleteUser, sender = Profile)
post_save.connect(updateUser, sender= Profile)

def updateProfile(sender, instance, created, **kwargs):
    print("Profile Updated")
    print("Instance:", instance)
    print("Created:", created)
    
post_save.connect(updateProfile, sender = Profile)