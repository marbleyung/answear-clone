# Generated by Django 4.1.7 on 2023-04-11 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_itemsize_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='items',
            field=models.ManyToManyField(default=None, to='shop.itemstock'),
        ),
    ]
