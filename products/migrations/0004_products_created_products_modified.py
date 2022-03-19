# Generated by Django 4.0.2 on 2022-03-18 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_products_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='products',
            name='modified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]