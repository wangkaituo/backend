# Generated by Django 5.1.7 on 2025-04-28 03:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='empuser',
            name='is_active',
        ),
    ]
