# Generated by Django 2.2.7 on 2019-12-20 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sys_manager', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='module',
            name='module_number',
            field=models.CharField(default=1, max_length=50, verbose_name='模块编码'),
            preserve_default=False,
        ),
    ]
