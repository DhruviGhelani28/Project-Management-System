# Generated by Django 3.2.12 on 2022-02-17 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_alter_skill_name'),
        ('projects', '0024_alter_permission_project'),
    ]

    operations = [
        migrations.AlterField(
            model_name='permission',
            name='name',
            field=models.CharField(choices=[('Edit', 'Edit permission'), ('Read', 'Read permission'), ('Delete', 'Delete permission')], max_length=50, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='permission',
            unique_together={('client', 'project')},
        ),
    ]
