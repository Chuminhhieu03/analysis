# Generated by Django 5.0.1 on 2024-04-10 04:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_rename_update_date_order_updated_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdetail',
            name='product_name',
            field=models.CharField(default='', max_length=100),
        ),
    ]