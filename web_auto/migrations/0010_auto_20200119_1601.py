# Generated by Django 2.2.7 on 2020-01-19 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_auto', '0009_uisuitcaseexecuterecord'),
    ]

    operations = [
        migrations.RenameField(
            model_name='uicasestep',
            old_name='type',
            new_name='step_type',
        ),
        migrations.AlterField(
            model_name='uicasestep',
            name='operate_type',
            field=models.IntegerField(null=True, verbose_name='操作类型(1:点击,2:输入,3:双击,4:悬停,5:右击,6:窗体切换)'),
        ),
    ]