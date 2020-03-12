# -*- coding: UTF-8 -*-

from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.shortcuts import render,redirect
from web_auto.models import UiParam,UiElement,UiCase,UiCaseStep,UiSuit,UiSuitExecuteRecord,UiSuitCaseExecuteRecord
from sys_manager.models import Module
from django.db.models import Q
from sys_manager.sys_views import check_login
from TestAutomation.date_utils import LocalDateEncoder
from django.utils import timezone
from TestAutomation.utils.logger_util import Logger
from TestAutomation.utils.redis_util import RedisOpt
from TestAutomation.utils.file_util import FileUtil
from web_auto.run_case import RunCase
from celery_tasks.tasks import execute_interface_case_suit
from selenium.webdriver.support.wait import WebDriverWait
import re,time
import json
from django.db.models import Sum,Count,Max,Min,Avg
from django.db import transaction

# 日志对象定义和初始化
log_dir = RedisOpt.get_str('ui_param_LogDir')
log_console = RedisOpt.get_str('ui_param_LogConsole')
log_level = RedisOpt.get_str('ui_param_LogLevel')
logger = Logger('WebViews',log_dir,log_console,log_level).logger

#########################参数管理##############################


@check_login
def param_list_page(request):
    return render(request,'web/param_list.html',{})


@check_login
def param_list(request):
    param_name = request.GET.get('param_name')
    belong_menu = request.GET.get('belong_menu')
    page = request.GET.get('page')
    size = request.GET.get('size')
    # 条件过滤查询，page为页码，size为页大小，right_boundary为分页右边界
    right_boundary = int(page) * int(size)
    params = UiParam.objects.all()
    if param_name:
        params = params.filter(Q(param_name__contains=param_name))
    if belong_menu:
        params = params.filter(Q(belong_menu__contains=belong_menu))
    # 记录总数
    total = params.count()
    params = params.order_by('id')[int(size) * (int(page) - 1):right_boundary]     #分页切片
    rows = []
    for param in params:
        rows.append({'id': param.id, 'param_name': param.param_name, 'param_value': param.param_value,'belong_menu': param.belong_menu, 'description':param.description,'build_time':param.build_time})
    return HttpResponse(json.dumps({'total': total, 'rows': rows},cls=LocalDateEncoder))


@check_login
def param_add_page(request):
    return render(request,'web/param_add.html',{})


@check_login
@transaction.atomic
def param_add(request):
    try:
        param = UiParam()
        param_name = request.POST.get('param_name')
        param_value = request.POST.get('param_value')
        belong_menu = request.POST.get('belong_menu')
        description = request.POST.get('description')
        param.param_name = param_name
        param.param_value = param_value
        param.belong_menu = belong_menu
        param.description = description
        param.save()
        RedisOpt.set('ui_param_'+param_name,param_value)
    except Exception:
        return JsonResponse({'code': 1})
    else:
        return JsonResponse({'code':0})


@check_login
def param_edit_page(request):
    id = request.GET.get('id')
    param = UiParam.objects.get(id=id)
    return render(request,'web/param_edit.html',{'param':param})


@check_login
@transaction.atomic
def param_edit(request):
    try:
        id = request.POST.get('id')
        param_name = request.POST.get('param_name')
        param_value = request.POST.get('param_value')
        description = request.POST.get('description')
        belong_menu = request.POST.get('belong_menu')
        param = UiParam.objects.get(id=id)
        param.param_name = param_name
        param.param_value = param_value
        if description is not None:
            param.description = description
        if belong_menu is not None:
            param.belong_menu = belong_menu
        param.save()
        RedisOpt.set('ui_param_'+param_name,param_value)
    except Exception:
        return JsonResponse({'code': 1})
    else:
        return JsonResponse({'code':0})


@check_login
@transaction.atomic
def param_delete(request):
    try:
        id = request.POST.get('id')
        param = UiParam.objects.get(id=id)
        param.delete()
        RedisOpt.delete('ui_param_'+param.param_name)
    except Exception:
        return JsonResponse({'code': 1})
    else:
        return JsonResponse({'code': 0})


#########################元素管理##############################


@check_login
def element_list_page(request):
    return render(request,'web/element_list.html',{})


@check_login
def element_list(request):
    moduleId = request.GET.get('choseModuleId')
    element_name = request.GET.get('element_name')
    locate_type = request.GET.get('locate_type')
    page = request.GET.get('page')
    size = request.GET.get('size')
    # 条件过滤查询，page为页码，size为页大小，right_boundary为分页右边界
    right_boundary = int(page) * int(size)
    elements = UiElement.objects.all()
    if moduleId:
        elements = elements.filter(module_id=moduleId)
    if element_name:
        elements = elements.filter(Q(element_name__contains=element_name))
    if locate_type:
        elements = elements.filter(Q(locate_type=locate_type))
    # 记录总数
    total = elements.count()
    elements = elements.order_by('id')[int(size) * (int(page) - 1):right_boundary]     #分页切片
    rows = []
    for element in elements:
        rows.append({'id': element.id, 'element_name': element.element_name, 'locate_type': element.locate_type,'locate_partern': element.locate_partern, 'description':element.description})
    return HttpResponse(json.dumps({'total': total, 'rows': rows},cls=LocalDateEncoder))


@check_login
def element_add_page(request):
    moduleId = request.GET.get('moduleId')
    return render(request,'web/element_add.html',{'moduleId':moduleId})


@check_login
def element_add(request):
    try:
        element = UiElement()
        moduleId = request.POST.get('moduleId')
        element_name = request.POST.get('element_name')
        description = request.POST.get('description')
        locate_type = request.POST.get('locate_type')
        locate_partern = request.POST.get('locate_partern')
        module = Module.objects.get(id=moduleId)
        element.module = module
        element.element_name = element_name
        element.description = description
        element.locate_type = locate_type
        element.locate_partern = locate_partern
        element.save()
    except Exception:
        return JsonResponse({'code': 1})
    else:
        return JsonResponse({'code':0})


@check_login
def element_edit_page(request):
    id = request.GET.get('id')
    element = UiElement.objects.get(id=id)
    return render(request,'web/element_edit.html',{'element':element})


@check_login
def element_edit(request):
    try:
        id = request.POST.get('id')
        element_name = request.POST.get('element_name')
        locate_type = request.POST.get('locate_type')
        locate_partern = request.POST.get('locate_partern')
        description = request.POST.get('description')
        element = UiElement.objects.get(id=id)
        element.element_name = element_name
        element.locate_type = locate_type
        element.locate_partern = locate_partern
        if description is not None:
            element.description = description
        element.save()
    except Exception:
        return JsonResponse({'code': 1})
    else:
        return JsonResponse({'code':0})


@check_login
def element_delete(request):
    try:
        id = request.POST.get('id')
        element = UiElement.objects.get(id=id)
        element.delete()
    except Exception:
        return JsonResponse({'code': 1})
    else:
        return JsonResponse({'code': 0})


#########################用例管理##############################


@check_login
def case_list_page(request):
    return render(request,'web/case_list.html',{})


@check_login
def case_list(request):
    size = request.GET.get('size')
    page = request.GET.get('page')
    moduleId = request.GET.get('moduleId')
    run_flag = request.GET.get('run_flag')
    builder = request.GET.get('builder')
    case_name = request.GET.get('case_name')
    case_no = request.GET.get('case_no')
    right_boundary = int(page) * int(size)
    cases = UiCase.objects.all()
    # 方式一
    if moduleId:
        cases = UiCase.objects.filter(module__id=moduleId)
    # 方式二
    # if moduleId:
    #     module = Module.objects.get(id=moduleId)
    #     cases = module.interfacecase_set.all()
    # 方式三
    # if moduleId:
    #     cases = cases.filter(Q(module_id=moduleId))
    if run_flag:
        cases = cases.filter(Q(run_flag=run_flag))
    if builder:
        cases = cases.filter(Q(builder__contains=builder))
    if case_name:
        cases = cases.filter(Q(case_name__contains=case_name))
    if case_no:
        cases = cases.filter(Q(case_no__contains=case_no))
    # 记录总数
    total = cases.count()
    cases = cases.order_by('id')[int(size) * (int(page) - 1):right_boundary]     #分页切片
    rows = []
    for case in cases:
        rows.append({'id': case.id, 'case_no': case.case_no, 'case_name': case.case_name,'case_description': case.case_description, 'run_flag':case.run_flag,'builder':case.builder,'build_time':case.build_time,'modify_time':case.modify_time})
    return HttpResponse(json.dumps({'total': total, 'rows': rows},cls=LocalDateEncoder))


@check_login
def case_add_page(request):
    moduleId  = request.GET.get('moduleId')
    user_name = request.COOKIES.get('user_name', '').encode('latin-1').decode('utf-8')
    return render(request,'web/case_add.html',{'moduleId':moduleId,'user_name':user_name})


@check_login
def case_no_is_exist(request):
    case_no = request.POST.get('case_no')
    original_no = request.POST.get('original_no')
    if original_no is not None and case_no==original_no:
        return HttpResponse('true')
    else:
        case = UiCase.objects.filter(case_no=case_no)
        if case:
            return HttpResponse('false')
        else:
            return HttpResponse('true')


@check_login
def case_add(request):
    try:
        case = UiCase()
        moduleId = request.POST.get('moduleId')
        case_no = request.POST.get('case_no')
        case_name = request.POST.get('case_name')
        case_description = request.POST.get('case_description')
        run_flag = request.POST.get('run_flag')
        builder = request.POST.get('builder')
        module = Module.objects.get(id=moduleId)
        case.case_no = case_no
        case.case_name = case_name
        case.case_description = case_description
        case.run_flag = run_flag
        case.builder = builder
        case.module = module
        case.save()
    except Exception:
        return JsonResponse({'code': 1})
    else:
        return JsonResponse({'code':0})


@check_login
def case_delete(request):
    try:
        id = request.POST.get('id')
        case = UiCase.objects.get(id=id)
        case.delete()
    except Exception:
        return JsonResponse({'code': 1})
    else:
        return JsonResponse({'code': 0})


@check_login
def case_edit_page(request):
    id = request.GET.get('id')
    uiCase = UiCase.objects.get(id=id)
    uiCase.build_time = uiCase.build_time.strftime('%Y-%m-%d %H:%M:%S')
    uiCase.modify_time = uiCase.modify_time.strftime('%Y-%m-%d %H:%M:%S')
    return render(request,'web/case_edit.html',{'uiCase':uiCase})


@check_login
def case_edit(request):
    try:
        id = request.POST.get('id')
        case_no = request.POST.get('case_no')
        case_name = request.POST.get('case_name')
        case_description = request.POST.get('case_description')
        run_flag = request.POST.get('run_flag')
        uiCase = UiCase.objects.get(id=id)
        uiCase.case_no = case_no
        uiCase.case_name = case_name
        uiCase.run_flag = run_flag
        if case_description is not None:
            uiCase.case_description = case_description
            uiCase.save()
    except Exception as e:
        return JsonResponse({'code': 1})
    else:
        return JsonResponse({'code':0})

@check_login
def case_copy_page(request):
    id = request.GET.get('id')
    user_name = request.COOKIES.get('user_name', '').encode('latin-1').decode('utf-8')
    uiCase = UiCase.objects.get(id=id)
    uiCase.builder = user_name
    return render(request,'web/case_copy.html',{'uiCase':uiCase,'id':id})

@check_login
@transaction.atomic
def case_copy(request):
    """用例复制"""
    try:
        case = UiCase()
        caseId = request.POST.get('caseId')
        moduleId = request.POST.get('moduleId')
        case_no = request.POST.get('case_no')
        case_name = request.POST.get('case_name')
        case_description = request.POST.get('case_description')
        run_flag = request.POST.get('run_flag')
        builder = request.POST.get('builder')
        module = Module.objects.get(id=moduleId)
        case.case_no = case_no
        case.case_name = case_name
        case.case_description = case_description
        case.run_flag = run_flag
        case.builder = builder
        case.module = module
        case.save()
        ui_case_steps = UiCaseStep.objects.filter(case__id=caseId)
        for ui_case_step in ui_case_steps:
            step = UiCaseStep()
            step.step_no = ui_case_step.step_no
            step.step_name = ui_case_step.step_name
            step.content = ui_case_step.content
            step.case = case
            step.step_type = ui_case_step.step_type
            step.element = ui_case_step.element
            step.operate_type = ui_case_step.operate_type
            step.assert_type = ui_case_step.assert_type
            step.assert_partern = ui_case_step.assert_partern
            step.save()
    except Exception:
        return JsonResponse({'code': 1})
    else:
        return JsonResponse({'code':0})

@check_login
@transaction.atomic
def case_batch_delete(request):
    try:
        ids = request.POST.getlist('ids')  # django接收数组
        cases = UiCase.objects.filter(id__in = ids)
        cases.delete()
    except Exception as e:
        return JsonResponse({'code': 1})
    else:
        return JsonResponse({'code': 0})

@check_login
def case_execute(request):
    """执行单个用例"""
    # try:
    id = request.POST.get('id')
    uicase = UiCase.objects.get(id=id)
    runcase = RunCase(logger)
    execute_retuls = None
    logger.info('执行单个UI用例：%s'%uicase.case_name)
    # 执行基础步骤的用例
    # base_case_id = RedisOpt.get_str('ui_param_BaseCaseId')
    # base_case = UiCase.objects.get(id=base_case_id)
    pre_case = RedisOpt.get_obj('ui_param_pre_case')
    for step in UiCaseStep.objects.filter(case=pre_case).order_by('step_no'):
        runcase.run_case_by_step(step)
    # 正式开始执行用例
    for step in UiCaseStep.objects.filter(case=uicase).order_by('step_no'):
        execute_retuls = runcase.run_case_by_step(step)
    real_result = execute_retuls[0]
    pass_flag = execute_retuls[1]
    exception_msg = execute_retuls[2]
    runcase.base_page.quit()
    if pass_flag == runcase.CASE_PASS:
        return JsonResponse({'msg':'用例执行通过'})
    elif pass_flag == runcase.CASE_NOT_PASS:
        return JsonResponse({'msg':'用例执行不通过，实际断言结果为：<xmp>%s</xmp>'% real_result})
    else:
        return JsonResponse({'msg':'用例执行异常，异常信息为：<xmp>%s</xmp>'% exception_msg})
    # except Exception as e:
    #     return JsonResponse({'msg':'用例执行异常，异常信息为：<xmp>%s</xmp>' % e})

#########################用例步骤管理##############################


@check_login
def step_list_page(request):
    caseId = request.GET.get('caseId')
    case_steps = []
    steps = UiCaseStep.objects.filter(Q(case__id=caseId)&Q(step_type=1)).order_by('-step_no')
    for step in steps:
        if step.element is not None:
            step.moduleText = step.element.module.module_number+"_"+step.element.module.module_name+" > "+step.element.element_name
        case_steps.append(step)
    case_assert = UiCaseStep.objects.filter(Q(case__id=caseId) & Q(step_type=2))
    if case_assert:
        case_assert = case_assert[0]
        case_assert.moduleText = case_assert.element.module.module_number+"_"+case_assert.element.module.module_name+" > "+case_assert.element.element_name
    return render(request,'web/step_list.html',{'caseId':caseId,'case_steps':case_steps,'case_assert':case_assert})


@check_login
def step_element_list_page(request):
    """用例步骤维护页面，展示元素列表"""
    return render(request,'web/step_element_list.html',{})


@check_login
@transaction.atomic
def step_save(request):
    """保存用例步骤"""
    # try:
    data = json.loads(request.body.decode(encoding='UTF-8'))
    caseId = data['caseId']
    case_steps = data['case_steps']
    case_assert = data['case_assert']
    case = UiCase.objects.get(id=caseId)
    # 先删除原有步骤
    UiCaseStep.objects.filter(case__id=caseId).delete()
    # 添加新步骤
    for case_step in case_steps:
        step = UiCaseStep()
        step.step_no = case_step['step_no']
        step.step_name = case_step['step_name']
        step.content = case_step['content']
        step.case = case
        step.step_type = 1
        step.operate_type = case_step['operate_type']
        if step.operate_type == '8':
            step.element = None
        else:
            step.element = UiElement.objects.get(id = case_step['element_id'])
        step.save()
    if case_assert['assert_type'] == '0':
        pass
    else:
        assert_step = UiCaseStep()
        assert_step.assert_type = case_assert['assert_type']
        assert_step.case = case
        assert_step.step_no = case_assert['assert_no']
        assert_step.step_name = case_assert['assert_name']
        assert_step.step_type = 2
        assert_step.element = UiElement.objects.get(id = case_assert['assert_element_id'])
        assert_step.assert_partern = case_assert['assert_partern']
        assert_step.save()
# except Exception:
#     return JsonResponse({'code': 1})
# else:
    return JsonResponse({'code':0})


#########################用例集管理##############################


@check_login
def suit_list_page(request):
    return render(request,'web/suit_list.html',{})


@check_login
def suit_list(request):
    suit_name = request.GET.get('suit_name')
    builder = request.GET.get('builder')
    start_time = request.GET.get('start_time')
    end_time = request.GET.get('end_time')
    page = request.GET.get('page')
    size = request.GET.get('size')
    # 条件过滤查询，page为页码，size为页大小，right_boundary为分页右边界
    right_boundary = int(page) * int(size)
    suits = UiSuit.objects.all()
    if suit_name:
        suits = suits.filter(Q(suit_name__contains=suit_name))
    if builder:
        suits = suits.filter(Q(builder__contains=builder))
    if start_time:
        suits = suits.filter(Q(build_time__gte=start_time))
    if end_time:
        suits = suits.filter(Q(build_time__lte=end_time))
    # 记录总数
    total = suits.count()
    suits = suits.order_by('id')[int(size) * (int(page) - 1):right_boundary]     #分页切片
    rows = []
    for suit in suits:
        rows.append({'id': suit.id, 'suit_no': suit.suit_no, 'suit_name': suit.suit_name,'suit_description': suit.suit_description, 'build_time':suit.build_time,'modify_time':suit.modify_time,'builder':suit.builder})
    return HttpResponse(json.dumps({'total': total, 'rows': rows},cls=LocalDateEncoder))


@check_login
def suit_add_page(request):
    user_name = request.COOKIES.get('user_name', '').encode('latin-1').decode('utf-8')
    return render(request,'web/suit_add.html',{'user_name':user_name})


@check_login
def suit_add(request):
    try:
        suit = UiSuit()
        suit_no = request.POST.get('suit_no')
        suit_name = request.POST.get('suit_name')
        suit_description = request.POST.get('suit_description')
        builder = request.POST.get('builder')
        suit.suit_no = suit_no
        suit.suit_name = suit_name
        suit.suit_description = suit_description
        suit.builder = builder
        suit.save()
    except Exception:
        return JsonResponse({'code': 1})
    else:
        return JsonResponse({'code':0})


@check_login
def suit_edit_page(request):
    id = request.GET.get('id')
    suit = UiSuit.objects.get(id=id)
    suit.build_time = suit.build_time.strftime('%Y-%m-%d %H:%M:%S')
    suit.modify_time = suit.modify_time.strftime('%Y-%m-%d %H:%M:%S')
    return render(request,'web/suit_edit.html',{'suit':suit})


@check_login
def suit_edit(request):
    try:
        id = request.POST.get('id')
        suit_no = request.POST.get('suit_no')
        suit_name = request.POST.get('suit_name')
        suit_description = request.POST.get('suit_description')
        suit = UiSuit.objects.get(id=id)
        suit.suit_no = suit_no
        suit.suit_name = suit_name
        if suit_description:
            suit.suit_description = suit_description
        suit.save()
    except Exception:
        return JsonResponse({'code': 1})
    else:
        return JsonResponse({'code':0})


@check_login
def suit_delete(request):
    try:
        id = request.POST.get('id')
        suit = UiSuit.objects.get(id=id)
        suit.delete()
    except Exception:
        return JsonResponse({'code': 1})
    else:
        return JsonResponse({'code': 0})


@check_login
def suit_case_list_page(request):
    suitId = request.GET.get('suitId')
    return render(request,'web/suit_case_list.html',{'suitId':suitId})


@check_login
def suit_case_list(request):
    size = request.GET.get('size')
    page = request.GET.get('page')
    suitId = request.GET.get('suitId')
    case_no = request.GET.get('case_no')
    case_name = request.GET.get('case_name')
    right_boundary = int(page) * int(size)
    suit = UiSuit.objects.get(id=suitId)
    cases = suit.ui_case
    if case_no:
        cases = cases.filter(Q(case_no__contains=case_no))
    if case_name:
        cases = cases.filter(Q(case_name__contains=case_name))
    # 记录总数
    total = cases.count()
    cases = cases.order_by('id')[int(size) * (int(page) - 1):right_boundary]  # 分页切片
    rows = []
    for case in cases:
        rows.append({'id': case.id, 'case_no': case.case_no, 'case_name': case.case_name,'case_description': case.case_description, 'run_flag': case.run_flag ,'builder': case.builder ,'build_time':case.build_time , 'modify_time':case.modify_time ,'module_name':case.module.module_name})
    return HttpResponse(json.dumps({'total': total, 'rows': rows}, cls=LocalDateEncoder))


@check_login
def suit_case_add_page(request):
    suitId = request.GET.get('suitId')
    return render(request,'web/suit_case_add.html',{'suitId':suitId})


@check_login
@transaction.atomic
def suit_case_add(request):
    try:
        caseIds = request.POST.getlist('caseIds')
        suitId = request.POST.get('suitId')
        suit = UiSuit.objects.get(id=suitId)
        exists_cases = suit.ui_case.all()
        for case_id in caseIds:
            add_case = UiCase.objects.get(id=case_id)
            if add_case in exists_cases:
                continue
            else:
                suit.ui_case.add(add_case)
    except Exception:
        return JsonResponse({'code': 1})
    else:
        return JsonResponse({'code':0})


@check_login
@transaction.atomic
def suit_case_delete(request):
    try:
        caseIds = request.POST.getlist('caseIds')
        suitId = request.POST.get('suitId')
        suit = UiSuit.objects.get(id=suitId)
        suit.ui_case.remove(*caseIds)
    except Exception as e:
        return JsonResponse({'code': 1})
    else:
        return JsonResponse({'code': 0})


@check_login
@transaction.atomic
def suit_execute(request):
    """用例集执行"""
    try:
        suitId = request.POST.get('suitId')
        execute_person = request.COOKIES.get('user_name', '').encode('latin-1').decode('utf-8')
        # 开启异步任务，执行用例集
        ui_suit = UiSuit.objects.get(id=suitId)
        logger.info('执行UI用例集：%s开始' % ui_suit.suit_name)
        case_list = ui_suit.ui_case.all()
        ui_suit_execute_record = UiSuitExecuteRecord()
        ui_suit_execute_record.start_time = timezone.now()
        ui_suit_execute_record.execute_person = execute_person
        ui_suit_execute_record.ececute_status = 2  # 执行中状态
        ui_suit_execute_record.ui_suit = ui_suit
        ui_suit_execute_record.save()
        # 浏览器操作
        runcase = RunCase(logger)
        # 执行基础步骤的用例
        base_case_id= RedisOpt.get_str('ui_param_BaseCaseId')
        base_case = UiCase.objects.get(id=base_case_id)
        for step in UiCaseStep.objects.filter(case=base_case).order_by('step_no'):
            runcase.run_case_by_step(step)
        # 执行用例集的用例
        for case_data in case_list:
            # 执行用例，保存用例结果
            logger.info('执行UI用例集的用例：%s' % case_data.case_name)
            caseRecord = UiSuitCaseExecuteRecord()
            caseRecord.module_name = case_data.module.module_name
            caseRecord.case_no = case_data.case_no
            caseRecord.case_name =  case_data.case_name
            caseRecord.case_description =  case_data.case_description
            caseRecord.run_flag = case_data.run_flag
            caseRecord.builder = case_data.builder
            caseRecord.build_time = case_data.build_time
            caseRecord.modify_time = case_data.modify_time
            caseRecord.start_time = timezone.now()
            caseRecord.ui_suit_execute_record = ui_suit_execute_record
            assert_step = UiCaseStep.objects.filter(case=case_data).get(step_type=2)
            caseRecord.element_name = assert_step.element.element_name
            caseRecord.assert_type = assert_step.assert_type
            caseRecord.assert_partern = assert_step.assert_partern
            real_result = ' '
            pass_flag = runcase.CASE_EXCEPTION
            exception_msg = ' '
            for step in UiCaseStep.objects.filter(case=case_data).order_by('step_no'):
                execute_retuls = runcase.run_case_by_step(step)
                real_result = execute_retuls[0]
                pass_flag = execute_retuls[1]
                exception_msg = execute_retuls[2]
            caseRecord.end_time = timezone.now()
            caseRecord.real_result = real_result
            caseRecord.pass_flag = pass_flag
            caseRecord.exception_msg = exception_msg
            caseRecord.save()
        ui_suit_execute_record.end_time = timezone.now()
        ui_suit_execute_record.ececute_status=3     # 执行结束状态
        ui_suit_execute_record.save()
        runcase.base_page.quit()
        logger.info('执行UI用例集：%s结束' % ui_suit.suit_name)
        return JsonResponse({'code': 0})    # 返回执行成功
    except Exception as e:
        return JsonResponse({'code': 1})    # 返回执行失败


#########################日志管理##############################


@check_login
def log_list_page(request):
    return render(request,'web/log_list.html',{})


@check_login
def log_list(request):
    """查询日志目录下的所有文件"""
    log_dir = RedisOpt.get_str('ui_param_LogDir')
    all_files = FileUtil.list_all_files(log_dir)
    list_files = []
    log_name = request.GET.get('log_name')
    size = request.GET.get('size')
    page = request.GET.get('page')
    if log_name is not None:
        for file in all_files:
            if log_name in file:
                list_files.append(file)
            else:
                continue
    else:
        list_files = all_files
    list_files.sort(key=lambda x: str(x[3:10]))
    list_files.reverse()
    total = len(list_files)
    right_boundary = int(page) * int(size)
    list_files = list_files[int(size) * (int(page) - 1):right_boundary]
    rows = []
    for list_file in list_files:
        log_size = FileUtil.get_file_size(log_dir + '/' + list_file).__str__() + RedisOpt.get_str(
            'sys_param_FileSizeUnit')
        build_time = FileUtil.get_create_time(log_dir + '/' + list_file)
        modify_time = FileUtil.get_last_modify_time(log_dir + '/' + list_file)
        rows.append({'log_name': list_file, 'log_size': log_size, 'build_time': build_time, 'modify_time': modify_time})
    return HttpResponse(json.dumps({'total': total, 'rows': rows}, cls=LocalDateEncoder))


@check_login
def log_detail_page(request):
    log_name = request.GET.get('logName')
    log_dir = RedisOpt.get_str('ui_param_LogDir')
    log_size = RedisOpt.get_str('sys_param_LogFontSize')
    file_path = log_dir+'/'+log_name
    file_content = ""
    with open(file_path,'rb') as file:
        file_content = file.read()
        file_content = "<style>body{font-size:" + log_size + "px;}</style>" + file_content.decode(encoding='UTF-8').replace('\n', '<br/>')
    return HttpResponse(file_content)


#########################测试报告##############################


@check_login
def report_list_page(request):
    return render(request,'web/report_list.html',{})


@check_login
def report_list(request):
    suit_name = request.GET.get('suit_name')
    execute_person = request.GET.get('execute_person')
    start_time = request.GET.get('start_time')
    end_time = request.GET.get('end_time')
    page = request.GET.get('page')
    size = request.GET.get('size')
    # 条件过滤查询，page为页码，size为页大小，right_boundary为分页右边界
    right_boundary = int(page) * int(size)
    suit_execute_records = UiSuitExecuteRecord.objects.all()
    if suit_name:
        ui_suits = UiSuit.objects.filter(suit_name__contains=suit_name)
        suit_execute_records = suit_execute_records.filter(ui_suit__in=ui_suits)
    if execute_person:
        suit_execute_records = suit_execute_records.filter(Q(execute_person__contains=execute_person))
    if start_time:
        suit_execute_records = suit_execute_records.filter(Q(start_time__gte=start_time))
    if end_time:
        suit_execute_records = suit_execute_records.filter(Q(start_time__lte=end_time))
    # 记录总数
    total = suit_execute_records.count()
    suit_execute_records = suit_execute_records.order_by('-id')[int(size) * (int(page) - 1):right_boundary]     #分页切片
    rows = []
    for suit_record in suit_execute_records:
        rows.append({'id': suit_record.id, 'ececute_status': suit_record.ececute_status, 'execute_person': suit_record.execute_person,'start_time': suit_record.start_time, 'end_time':suit_record.end_time,'suit_no':suit_record.ui_suit.suit_no,'suit_name':suit_record.ui_suit.suit_name})
    return HttpResponse(json.dumps({'total': total, 'rows': rows},cls=LocalDateEncoder))


@check_login
def report_detail_page(request):
    suit_record_id = request.GET.get("id")
    moduleResultSet = UiSuitCaseExecuteRecord.objects.filter(ui_suit_execute_record__id=suit_record_id).values('module_name').annotate(count=Count(1))
    module_legend_data = []
    module_series_data = []
    for result in moduleResultSet:
        module_legend_data.append(result['module_name'])
        module_series_data.append({"value": result['count'], "name":result['module_name']})
    module_chart_option={"text":"模块用例数统计","legend_data":module_legend_data,"series_name":"模块名称","series_data":module_series_data}

    statusResultSet = UiSuitCaseExecuteRecord.objects.filter(ui_suit_execute_record__id=suit_record_id).values('pass_flag').annotate(count=Count(1))
    status_legend_data = []
    status_series_data = []
    for result in statusResultSet:
        if result['pass_flag'] == 1:
            status_legend_data.append("通过")
            status_series_data.append({"value": result['count'], "name": "通过"})
        elif result['pass_flag'] == 2:
            status_legend_data.append("未通过")
            status_series_data.append({"value": result['count'], "name": "未通过"})
        elif result['pass_flag'] == 3:
            status_legend_data.append("异常")
            status_series_data.append({"value": result['count'], "name": "异常"})
        else:
            status_legend_data.append("未知")
            status_series_data.append({"value": result['count'], "name":"未知"})
    status_chart_option={"text":"用例执行状态统计","legend_data":status_legend_data,"series_name":"执行状态","series_data":status_series_data}
    return render(request,'web/report_detail.html',{"suit_record_id":suit_record_id,"moduleChartOption":module_chart_option,"statusChartOption":status_chart_option})


@check_login
def report_detail(request):
    suit_record_id = request.GET.get('suit_record_id')
    page = request.GET.get('page')
    size = request.GET.get('size')
    # 条件过滤查询，page为页码，size为页大小，right_boundary为分页右边界
    right_boundary = int(page) * int(size)
    case_records = UiSuitCaseExecuteRecord.objects.filter(ui_suit_execute_record_id=suit_record_id)
    # 记录总数
    total = case_records.count()
    case_records = case_records.order_by('id')[int(size) * (int(page) - 1):right_boundary]     #分页切片
    rows = []
    for case_record in case_records:
        rows.append({'module_name': case_record.module_name, 'case_no': case_record.case_no, 'case_name': case_record.case_name,'case_description': case_record.case_description, 'builder':case_record.builder,'element_name':case_record.element_name,'assert_type':case_record.assert_type,'assert_partern':case_record.assert_partern,'real_result':'<xmp>%s</xmp>'%(case_record.real_result),'start_time':case_record.start_time,'end_time':case_record.end_time,'pass_flag':case_record.pass_flag,'exception_msg':case_record.exception_msg})
    return HttpResponse(json.dumps({'total': total, 'rows': rows},cls=LocalDateEncoder))

