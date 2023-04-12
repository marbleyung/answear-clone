# Generated by Django 4.1.7 on 2023-04-11 14:29

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0013_remove_cart_unique_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='unique_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, null=True),
        ),
    ]
