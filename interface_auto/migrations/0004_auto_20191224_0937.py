# Generated by Django 2.2.7 on 2019-12-24 01:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interface_auto', '0003_auto_20191223_1701'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interfacecase',
            name='asset_partern',
            field=models.CharField(max_length=100000, null=True, verbose_name='断言值/表达式'),
        ),
        migrations.AlterField(
            model_name='interfacecase',
            name='request_cookie',
            field=models.CharField(max_length=100000, null=True, verbose_name='请求cookie'),
        ),
        migrations.AlterField(
            model_name='interfacecase',
            name='request_header',
            field=models.CharField(max_length=100000, null=True, verbose_name='请求头'),
        ),
    ]