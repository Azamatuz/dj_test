# Generated by Django 2.2 on 2020-08-15 19:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='menuitem',
            old_name='lable',
            new_name='label',
        ),
    ]