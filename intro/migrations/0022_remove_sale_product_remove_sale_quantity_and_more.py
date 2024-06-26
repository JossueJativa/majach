# Generated by Django 5.0.3 on 2024-04-23 19:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intro', '0021_delete_client_cart'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sale',
            name='product',
        ),
        migrations.RemoveField(
            model_name='sale',
            name='quantity',
        ),
        migrations.CreateModel(
            name='Product_Quantity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='intro.product')),
            ],
        ),
        migrations.AddField(
            model_name='sale',
            name='Product_Quantity',
            field=models.ManyToManyField(blank=True, to='intro.product_quantity'),
        ),
    ]
