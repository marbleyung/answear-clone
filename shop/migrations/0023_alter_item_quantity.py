# Generated by Django 4.1.7 on 2023-04-13 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0022_alter_itemincart_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='quantity',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
