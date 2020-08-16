# Generated by Django 2.2 on 2020-08-15 23:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parent', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='ordered_date',
            new_name='event_date',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='start_date',
            new_name='order_date',
        ),
        migrations.AddField(
            model_name='orderitem',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]