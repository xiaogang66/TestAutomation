# Generated by Django 2.2.7 on 2019-12-23 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interface_auto', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='interfacecase',
            name='builder',
            field=models.CharField(max_length=50, null=True, verbose_name='创建人'),
        ),
    ]