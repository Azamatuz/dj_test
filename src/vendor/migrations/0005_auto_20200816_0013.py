# Generated by Django 2.2 on 2020-08-16 00:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0004_remove_menuitem_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitem',
            name='label',
            field=models.CharField(choices=[('-', 'None'), ('P', 'Pork'), ('V', 'Veggie'), ('N', 'Nuts')], default='P', max_length=1),
        ),
    ]
