# Generated by Django 4.0.1 on 2022-02-14 16:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0020_rename_owner_permission_client_alter_permission_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='permissions',
        ),
        migrations.AddField(
            model_name='permission',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projects.project'),
        ),
        migrations.AlterField(
            model_name='project',
            name='title',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
