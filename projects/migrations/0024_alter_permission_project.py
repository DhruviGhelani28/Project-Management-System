# Generated by Django 4.0.1 on 2022-02-15 01:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0023_alter_permission_project_alter_permission_sender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='permission',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='projects.project'),
        ),
    ]
