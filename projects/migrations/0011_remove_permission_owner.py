# Generated by Django 4.0.1 on 2022-02-10 06:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0010_permission'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='permission',
            name='owner',
        ),
    ]
