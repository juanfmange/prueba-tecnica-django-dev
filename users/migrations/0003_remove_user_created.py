# Generated by Django 4.0.2 on 2022-03-18 18:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_user_date_joined_remove_user_last_login_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='created',
        ),
    ]
