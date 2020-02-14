# Generated by Django 2.2.7 on 2019-12-31 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interface_auto', '0011_interfacesuitexecuterecord_log_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interfacecase',
            name='builder',
            field=models.CharField(max_length=256, null=True, verbose_name='创建人'),
        ),
        migrations.AlterField(
            model_name='interfacecase',
            name='case_name',
            field=models.CharField(max_length=256, verbose_name='用例名称'),
        ),
        migrations.AlterField(
            model_name='interfacecase',
            name='case_no',
            field=models.CharField(db_index=True, max_length=250, unique=True, verbose_name='用例编号'),
        ),
        migrations.AlterField(
            model_name='interfacecase',
            name='url',
            field=models.CharField(max_length=256, verbose_name='请求地址'),
        ),
        migrations.AlterField(
            model_name='interfaceparam',
            name='belong_menu',
            field=models.CharField(max_length=256, null=True, verbose_name='所属菜单'),
        ),
        migrations.AlterField(
            model_name='interfaceparam',
            name='param_name',
            field=models.CharField(max_length=256, verbose_name='参数名'),
        ),
        migrations.AlterField(
            model_name='interfaceparam',
            name='param_value',
            field=models.CharField(max_length=256, verbose_name='参数值'),
        ),
        migrations.AlterField(
            model_name='interfacesuit',
            name='builder',
            field=models.CharField(max_length=256, null=True, verbose_name='创建人'),
        ),
        migrations.AlterField(
            model_name='interfacesuit',
            name='suit_name',
            field=models.CharField(max_length=256, verbose_name='测试集名称'),
        ),
        migrations.AlterField(
            model_name='interfacesuit',
            name='suit_no',
            field=models.CharField(max_length=256, verbose_name='测试集编号'),
        ),
        migrations.AlterField(
            model_name='interfacesuitcaseexecuterecord',
            name='builder',
            field=models.CharField(max_length=256, null=True, verbose_name='创建人'),
        ),
        migrations.AlterField(
            model_name='interfacesuitcaseexecuterecord',
            name='case_name',
            field=models.CharField(max_length=256, verbose_name='用例名称'),
        ),
        migrations.AlterField(
            model_name='interfacesuitcaseexecuterecord',
            name='case_no',
            field=models.CharField(db_index=True, max_length=250, verbose_name='用例编号'),
        ),
        migrations.AlterField(
            model_name='interfacesuitcaseexecuterecord',
            name='module_name',
            field=models.CharField(max_length=256, null=True, verbose_name='模块名称'),
        ),
        migrations.AlterField(
            model_name='interfacesuitcaseexecuterecord',
            name='url',
            field=models.CharField(max_length=256, verbose_name='请求地址'),
        ),
        migrations.AlterField(
            model_name='interfacesuitexecuterecord',
            name='execute_person',
            field=models.CharField(max_length=256, null=True, verbose_name='执行人'),
        ),
        migrations.AlterField(
            model_name='interfacesuitexecuterecord',
            name='log_url',
            field=models.CharField(max_length=256, null=True, verbose_name='日志路径'),
        ),
        migrations.AlterField(
            model_name='interfacesuitexecuterecord',
            name='report_url',
            field=models.CharField(max_length=256, null=True, verbose_name='执行报告路径'),
        ),
    ]
