# Generated by Django 4.2.15 on 2024-09-01 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_order_orderitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='discount',
            field=models.BooleanField(default=True),
        ),
    ]
