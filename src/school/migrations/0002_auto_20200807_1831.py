# Generated by Django 2.2 on 2020-08-07 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventitem',
            name='date',
            field=models.DateField(),
        ),
    ]
