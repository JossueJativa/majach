# Generated by Django 5.0.3 on 2024-04-23 20:14

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intro', '0022_remove_sale_product_remove_sale_quantity_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
