# Generated by Django 4.1.7 on 2023-04-13 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0023_alter_item_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='itembrand',
            name='slug',
            field=models.SlugField(null=True),
        ),
        migrations.AlterUniqueTogether(
            name='itemstock',
            unique_together={('item', 'size')},
        ),
    ]
