# Generated by Django 2.2 on 2020-07-22 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0006_auto_20200722_0636'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitem',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
