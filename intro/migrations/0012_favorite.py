# Generated by Django 5.0.3 on 2024-04-17 19:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intro', '0011_sale'),
    ]

    operations = [
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='intro.client')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='intro.product')),
            ],
        ),
    ]
