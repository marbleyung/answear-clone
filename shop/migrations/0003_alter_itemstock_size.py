# Generated by Django 4.1.7 on 2023-04-11 11:48

from django.db import migrations
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_alter_itemstock_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemstock',
            name='size',
            field=smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='item_type', chained_model_field='itemtype', on_delete=django.db.models.deletion.CASCADE, show_all=True, to='shop.itemsize'),
        ),
    ]
