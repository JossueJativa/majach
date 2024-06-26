# Generated by Django 5.0.3 on 2024-04-15 21:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intro', '0010_product_stars_comment_product_comments'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('quantity', models.IntegerField()),
                ('total', models.FloatField()),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='intro.client')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='intro.product')),
            ],
        ),
    ]
