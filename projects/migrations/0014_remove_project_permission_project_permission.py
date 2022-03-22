# Generated by Django 4.0.1 on 2022-02-11 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0013_remove_permission_project_project_permission_task'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='permission',
        ),
        migrations.AddField(
            model_name='project',
            name='permission',
            field=models.ManyToManyField(blank=True, to='projects.Permission'),
        ),
    ]
