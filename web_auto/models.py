from django.db import models

# Create your models here.


class UiParam(models.Model):
    param_name = models.CharField(max_length=256,verbose_name='参数名')
    param_value = models.CharField(max_length=256,verbose_name='参数值')
    belong_menu = models.CharField(max_length=256,null=True,verbose_name='所属菜单',default='')
    description = models.CharField(max_length=256, null=True,verbose_name='描述',default='')
    build_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')


class UiElement(models.Model):
    element_name =  models.CharField(max_length=256,verbose_name='页面名称')
    locate_type = models.IntegerField(default=1,verbose_name='定位方式(1:id,2:name,3:css表达式,4:xpath,5:class,6:tag,7:linktext,8:frame,9:window)')
    locate_partern = models.CharField(max_length=256,verbose_name='定位表达式')
    description = models.CharField(max_length=256,null=True,verbose_name='描述信息')
    module = models.ForeignKey('sys_manager.Module', null=True, verbose_name='所属模块', on_delete=models.SET_NULL)


class UiCase(models.Model):
    case_no = models.CharField(max_length=50,verbose_name='用例编号')
    case_name = models.CharField(max_length=256,verbose_name='用例名称')
    case_description = models.CharField(max_length=256,null=True,verbose_name='用例描述')
    run_flag = models.BooleanField(default=True,verbose_name='运行标志（1运行，0禁止）')
    module = models.ForeignKey('sys_manager.Module', null=True, verbose_name='所属模块', on_delete=models.SET_NULL)
    builder = models.CharField(max_length=256,null=True,verbose_name='创建人',default='')
    build_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    modify_time = models.DateTimeField(auto_now=True,verbose_name='修改时间')


class UiCaseStep(models.Model):
    step_no = models.IntegerField(verbose_name='步骤编号')
    step_name = models.CharField(max_length=256,verbose_name='步骤名称')
    step_type = models.IntegerField(default=1,verbose_name='步骤类型(1操作，2断言)')
    element = models.ForeignKey('UiElement',null=True,verbose_name='对应元素',on_delete=models.SET_NULL)
    operate_type = models.IntegerField(null=True,verbose_name='操作类型(1:点击,2:输入,3:双击,4:悬停,5:右击,6:窗体切换)')
    content = models.CharField(default='',max_length=256,null=True,verbose_name='操作内容')
    assert_type = models.IntegerField(null=True,verbose_name='断言类型(1:相等2:包含3:正则)')
    assert_partern = models.CharField(max_length=256,null=True,verbose_name='断言表达式')
    case = models.ForeignKey('UiCase',verbose_name='所属用例',db_index=True,on_delete=models.CASCADE)


class UiSuit(models.Model):
    suit_no = models.CharField(max_length=256,verbose_name='测试集编号')
    suit_name = models.CharField(max_length=256,verbose_name='测试集名称')
    suit_description = models.CharField(max_length=256,null=True,verbose_name='测试集描述')
    build_time =  models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    modify_time = models.DateTimeField(auto_now=True, verbose_name='最后修改时间')
    builder = models.CharField(max_length=256,null=True,verbose_name='创建人')
    ui_case = models.ManyToManyField('UiCase',verbose_name='测试用例')


class UiSuitExecuteRecord(models.Model):
    ececute_status = models.IntegerField(default=1,verbose_name='执行状态（1未开始，2执行中，3执行结束）')
    execute_person = models.CharField(null=True,max_length=256,verbose_name='执行人')
    start_time = models.DateTimeField(auto_now_add=True, verbose_name='执行开始时间')
    end_time  = models.DateTimeField(null=True, verbose_name='执行结束时间')
    report_url = models.CharField(null=True,max_length=256,verbose_name='执行报告路径')
    log_url = models.CharField(null=True, max_length=256, verbose_name='日志路径')
    ui_suit = models.ForeignKey('UiSuit',verbose_name='测试用例集',on_delete=models.CASCADE)


class UiSuitCaseExecuteRecord(models.Model):
    module_name = models.CharField(null=True,max_length=256,verbose_name='模块名称')
    case_no = models.CharField(max_length=250,verbose_name='用例编号',db_index=True)
    case_name = models.CharField(max_length=256,verbose_name='用例名称')
    case_description = models.CharField(max_length=256,null=True,verbose_name='用例描述')
    run_flag = models.BooleanField(default=True,verbose_name='运行标志（1运行，0禁止）')
    element_name = models.CharField(max_length=256,verbose_name='断言元素')
    assert_type = models.IntegerField(default=1,verbose_name='断言类型(1值相等，2值包含，3值正则，4文本相等，5文本包含，6文本正则)')
    assert_partern = models.TextField(max_length=100000,verbose_name='断言值/表达式')
    real_result = models.TextField(max_length=100000, null=True, verbose_name='断言实际值')
    pass_flag = models.IntegerField(null=True,verbose_name='是否通过(1通过,2未通过，3异常)')
    exception_msg = models.TextField(max_length=100000, null=True, verbose_name='异常信息')
    builder = models.CharField(max_length=256,null=True,verbose_name='创建人')
    build_time = models.DateTimeField(null=True,verbose_name='创建时间')
    modify_time = models.DateTimeField(null=True,verbose_name='修改时间')
    start_time = models.DateTimeField(null=True, verbose_name='执行开始时间')
    end_time  = models.DateTimeField(null=True, verbose_name='执行结束时间')
    ui_suit_execute_record = models.ForeignKey('UiSuitExecuteRecord',verbose_name='测试用例集记录',on_delete=models.CASCADE)




