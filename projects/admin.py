from django.contrib import admin
from .models import Project, Review, Tag, Permission, Task
# Register your models here.

admin.site.register(Project)
admin.site.register(Review)
admin.site.register(Tag)
admin.site.register(Permission)
admin.site.register(Task)