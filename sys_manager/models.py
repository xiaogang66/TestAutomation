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
    parent_module_number = models.ForeignKey('self',null=True,verbose_name='父模块编码',on_delete=models.SET_NULL)
    module_name = models.CharField(max_length=50,verbose_name='模块名')
    module_type = models.BooleanField(default=True,verbose_name='模块类型（1业务模块，0接口模块）')
    module_desc = models.CharField(max_length=256,null=True,verbose_name='模块描述',default='')
    manager = models.CharField(max_length=50,null=True,verbose_name='负责人',default='')
    builder = models.CharField(max_length=50,null=True,verbose_name='创建人',default='')
    build_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')


class InterfaceCase(models.Model):
    product_id = models.ForeignKey('Module',verbose_name='所属模块',null=True,on_delete=models.SET_NULL)
    case_no = models.CharField(max_length=50,verbose_name='用例编号',db_index=True)
    case_name = models.CharField(max_length=50,verbose_name='用例名称')
    case_description = models.CharField(max_length=256,null=True,verbose_name='用例描述')
    run_flag = models.BooleanField(default=True,verbose_name='运行标志（1运行，0禁止）')
    url = models.CharField(max_length=50,verbose_name='请求地址')
    request_method = models.IntegerField(default=1,verbose_name='请求方法（1get，2post）')
    request_header = models.CharField(max_length=256,null=True,verbose_name='请求头')
    request_cookie = models.CharField(max_length=256,null=True,verbose_name='请求cookie')
    request_param = models.TextField(max_length=100000,null=True,verbose_name='请求参数')
    exp_result = models.TextField(max_length=100000,verbose_name='预期结果')
    asset_type = models.IntegerField(default=1,verbose_name='断言类型(1相等，2包含，3正则)')
    asset_partern = models.CharField(max_length=256,null=True,verbose_name='断言表达式')
    build_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    modify_time = models.DateTimeField(auto_now=True,verbose_name='修改时间')
    class Meta:
        index_together = [["product_id", "case_name"],]


