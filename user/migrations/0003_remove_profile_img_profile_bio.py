# Generated by Django 5.1.7 on 2025-03-21 04:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_profile_img'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='img',
        ),
        migrations.AddField(
            model_name='profile',
            name='bio',
            field=models.TextField(blank=True, null=True),
        ),
    ]
