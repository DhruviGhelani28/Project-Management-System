# Generated by Django 4.0.1 on 2022-02-14 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0019_alter_project_options_permission_owner'),
    ]

    operations = [
        migrations.RenameField(
            model_name='permission',
            old_name='owner',
            new_name='client',
        ),
        migrations.AlterField(
            model_name='permission',
            name='name',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='name',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
