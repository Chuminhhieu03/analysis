# Generated by Django 5.0.1 on 2024-04-10 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_orderdetail_product_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdetail',
            name='product_price',
            field=models.FloatField(default=0),
        ),
    ]
