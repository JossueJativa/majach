# Generated by Django 5.0.3 on 2024-04-23 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intro', '0024_sale_is_done'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sale',
            name='is_done',
        ),
        migrations.AddField(
            model_name='clientsellerrelation',
            name='done_sale',
            field=models.BooleanField(default=False),
        ),
    ]