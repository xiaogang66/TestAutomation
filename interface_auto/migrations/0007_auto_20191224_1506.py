# Generated by Django 2.2.7 on 2019-12-24 07:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interface_auto', '0006_auto_20191224_1503'),
    ]

    operations = [
        migrations.RenameField(
            model_name='interfacesuit',
            old_name='interface_case',
            new_name='interfaceCase',
        ),
    ]
