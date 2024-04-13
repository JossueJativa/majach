# Generated by Django 5.0.3 on 2024-04-04 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intro', '0002_user_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='is_buyer',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='user',
            name='is_seller',
            field=models.BooleanField(default=False),
        ),
    ]
