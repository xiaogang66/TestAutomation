from django.db import models

# Create your models here.


class InterfaceParam(models.Model):
    param_name = models.CharField(max_length=50,verbose_name='参数名')
    param_value = models.CharField(max_length=50,verbose_name='参数值')
    belong_menu = models.CharField(max_length=50,null=True,verbose_name='所属菜单')
    description = models.CharField(max_length=256, null=True,verbose_name='描述',default='')
    build_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')


class InterfaceCase(models.Model):
    module = models.ForeignKey('sys_manager.Module',verbose_name='所属模块',null=True,on_delete=models.SET_NULL)
    case_no = models.CharField(max_length=50,verbose_name='用例编号',db_index=True,unique=True)
    case_name = models.CharField(max_length=50,verbose_name='用例名称')
    case_description = models.CharField(max_length=256,null=True,verbose_name='用例描述')
    run_flag = models.BooleanField(default=True,verbose_name='运行标志（1运行，0禁止）')
    url = models.CharField(max_length=50,verbose_name='请求地址')
    request_method = models.IntegerField(default=1,verbose_name='请求方法（1get，2post）')
    request_header = models.CharField(max_length=100000,null=True,verbose_name='请求头')
    request_cookie = models.CharField(max_length=100000,null=True,verbose_name='请求cookie')
    request_param = models.TextField(max_length=100000,null=True,verbose_name='请求参数')
    exp_result = models.TextField(max_length=100000,verbose_name='预期结果')
    asset_type = models.IntegerField(default=1,verbose_name='断言类型(1相等，2包含，3正则)')
    asset_partern = models.CharField(max_length=100000,null=True,verbose_name='断言值/表达式')
    builder = models.CharField(max_length=50,null=True,verbose_name='创建人')
    build_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    modify_time = models.DateTimeField(auto_now=True,verbose_name='修改时间')

    class Meta:
        index_together = [["module", "case_name"],]


class InterfaceSuit(models.Model):
    suit_no = models.CharField(max_length=50,verbose_name='测试集编号')
    suit_name = models.CharField(max_length=50,verbose_name='测试集名称')
    suit_description = models.CharField(max_length=256,null=True,verbose_name='测试集描述')
    build_time =  models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    modify_time = models.DateTimeField(auto_now_add=True, verbose_name='最后修改时间')
    builder = models.CharField(max_length=50,null=True,verbose_name='创建人')
    interfaceCase = models.ManyToManyField('InterfaceCase',verbose_name='测试用例')


class InterfaceSuitExecuteRecord(models.Model):
    ececute_status = models.IntegerField(default=1,verbose_name='请求方法（1未开始，2执行中，3执行结束）')
    execute_person = models.CharField(null=True,max_length=50,verbose_name='执行人')
    start_time = models.DateTimeField(auto_now_add=True, verbose_name='执行开始时间')
    end_time  = models.DateTimeField(null=True, verbose_name='执行结束时间')
    report_url = models.CharField(null=True,max_length=50,verbose_name='执行报告路径')
    interface_suit = models.ForeignKey('InterfaceSuit',verbose_name='测试用例集',on_delete=models.CASCADE)


class InterfaceSuitCaseExecuteRecord(models.Model):
    module_name = models.CharField(null=True,max_length=50,verbose_name='模块名称')
    case_no = models.CharField(max_length=50,verbose_name='用例编号',db_index=True,unique=True)
    case_name = models.CharField(max_length=50,verbose_name='用例名称')
    case_description = models.CharField(max_length=256,null=True,verbose_name='用例描述')
    run_flag = models.BooleanField(default=True,verbose_name='运行标志（1运行，0禁止）')
    url = models.CharField(max_length=50,verbose_name='请求地址')
    request_method = models.IntegerField(default=1,verbose_name='请求方法（1get，2post）')
    request_header = models.TextField(max_length=100000,null=True,verbose_name='请求头')
    request_cookie = models.TextField(max_length=100000,null=True,verbose_name='请求cookie')
    request_param = models.TextField(max_length=100000,null=True,verbose_name='请求参数')
    exp_result = models.TextField(max_length=100000,verbose_name='预期结果')
    asset_type = models.IntegerField(default=1,verbose_name='断言类型(1相等，2包含，3正则)')
    asset_partern = models.TextField(max_length=100000,verbose_name='断言值/表达式')
    builder = models.CharField(max_length=50,null=True,verbose_name='创建人')
    build_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    modify_time = models.DateTimeField(auto_now=True,verbose_name='修改时间')
    status_code = models.CharField(max_length=3,null=True,verbose_name='状态码')
    real_result = models.TextField(max_length=100000,null=True,verbose_name='实际结果')
    start_time = models.DateTimeField(auto_now_add=True, verbose_name='执行开始时间')
    end_time  = models.DateTimeField(null=True, verbose_name='执行结束时间')
    pass_flag = models.IntegerField(verbose_name='是否通过(1通过,2未通过，3异常)')
    interface_suit_execute_record = models.ForeignKey('InterfaceSuitExecuteRecord',verbose_name='测试用例集记录',on_delete=models.CASCADE)

