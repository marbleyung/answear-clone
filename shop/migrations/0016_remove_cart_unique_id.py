# Generated by Django 4.1.7 on 2023-04-12 10:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0015_alter_cart_unique_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='unique_id',
        ),
    ]
