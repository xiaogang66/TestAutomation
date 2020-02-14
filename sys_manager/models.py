from django.db import models

# Create your models here.


class ManagerUser(models.Model):
    user_name = models.CharField(max_length=50,verbose_name='姓名')
    gender = models.BooleanField(default=True,verbose_name='性别（1男，0女）')
    account = models.CharField(max_length=50,verbose_name='账号')
    password = models.CharField(max_length=50,verbose_name='密码')
    comment = models.CharField(max_length=256,null=True,verbose_name='备注',default='')
    build_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')


class SysParam(models.Model):
    param_name = models.CharField(max_length=50,verbose_name='参数名')
    param_value = models.CharField(max_length=50,verbose_name='参数值')
    belong_menu = models.CharField(max_length=50,null=True,verbose_name='所属菜单')
    description = models.CharField(max_length=256, null=True,verbose_name='描述',default='')
    build_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')


class Module(models.Model):
    module_number = models.CharField(max_length=50, verbose_name='模块编码')
    parent_module = models.ForeignKey('self',null=True,verbose_name='父模块编码',on_delete=models.SET_NULL)
    module_name = models.CharField(max_length=50,verbose_name='模块名')
    module_type = models.BooleanField(default=True,verbose_name='模块类型（1业务模块，0接口模块）')
    module_desc = models.CharField(max_length=256,null=True,verbose_name='模块描述',default='')
    manager = models.CharField(max_length=50,null=True,verbose_name='负责人',default='')
    builder = models.CharField(max_length=50,null=True,verbose_name='创建人',default='')
    build_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')


class Task(models.Model):
    task_no = models.CharField(max_length=50, verbose_name='任务编号')
    task_name = models.CharField(max_length=50,verbose_name='任务名')
    task_type = models.IntegerField(verbose_name='任务类型（1：接口任务，2：UI任务）')
    task_desc = models.CharField(max_length=256,null=True,verbose_name='任务描述',default='')
    task_partern = models.CharField(max_length=256,verbose_name='任务定时表达式')
    run_flag = models.BooleanField(default=True,verbose_name='运行标志（1是，0否）')
    manager = models.CharField(max_length=50,null=True,verbose_name='负责人',default='')
    builder = models.CharField(max_length=50,null=True,verbose_name='创建人',default='')
    build_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    modify_time = models.DateTimeField(auto_now=True,verbose_name='修改时间')
    suit_id = models.IntegerField(verbose_name='用例集id')



