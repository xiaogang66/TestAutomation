# -*- coding: UTF-8 -*-

from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.shortcuts import render,redirect
from sys_manager.models import ManagerUser,Module,SysParam
from interface_auto.models import InterfaceParam,InterfaceCase,InterfaceSuit,InterfaceSuitExecuteRecord,InterfaceSuitCaseExecuteRecord
from django.db.models import Q
from sys_manager.sys_views import check_login
from TestAutomation.date_utils import LocalDateEncoder
from django.utils import timezone
from TestAutomation.utils.logger_util import Logger
from TestAutomation.utils.redis_util import RedisOpt
from TestAutomation.utils.file_util import FileUtil
from interface_auto.run_case import RunCase
from celery_tasks.tasks import execute_interface_case_suit
import re,time
import json
from django.db.models import Sum,Count,Max,Min,Avg
from django.db import transaction

# 日志对象定义和初始化
log_dir = RedisOpt.get_str('interface_param_LogDir')
log_console = RedisOpt.get_str('interface_param_LogConsole')
log_level = RedisOpt.get_str('interface_param_LogLevel')
logger = Logger('InterfaceViews',log_dir,log_console,log_level).logger
runCase = RunCase(logger)

#########################参数管理##############################


@check_login
def param_list_page(request):
    return render(request,'interface/param_list.html',{})


@check_login
def param_list(request):
    param_name = request.GET.get('param_name')
    belong_menu = request.GET.get('belong_menu')
    page = request.GET.get('page')
    size = request.GET.get('size')
    # 条件过滤查询，page为页码，size为页大小，right_boundary为分页右边界
    right_boundary = int(page) * int(size)
    params = InterfaceParam.objects.all()
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
    return render(request,'interface/param_add.html',{})


@check_login
@transaction.atomic
def param_add(request):
    try:
        param = InterfaceParam()
        param_name = request.POST.get('param_name')
        param_value = request.POST.get('param_value')
        belong_menu = request.POST.get('belong_menu')
        description = request.POST.get('description')
        param.param_name = param_name
        param.param_value = param_value
        param.belong_menu = belong_menu
        param.description = description
        param.save()
        RedisOpt.set('interface_param_' + param_name, param_value)
    except Exception:
        return JsonResponse({'code': 1})
    else:
        return JsonResponse({'code':0})


@check_login
def param_edit_page(request):
    id = request.GET.get('id')
    param = InterfaceParam.objects.get(id=id)
    return render(request,'interface/param_edit.html',{'param':param})


@check_login
@transaction.atomic
def param_edit(request):
    try:
        id = request.POST.get('id')
        param_name = request.POST.get('param_name')
        param_value = request.POST.get('param_value')
        description = request.POST.get('description')
        belong_menu = request.POST.get('belong_menu')
        param = InterfaceParam.objects.get(id=id)
        param.param_name = param_name
        param.param_value = param_value
        if description is not None:
            param.description = description
        if belong_menu is not None:
            param.belong_menu = belong_menu
        param.save()
        RedisOpt.set('interface_param_' + param_name, param_value)
    except Exception:
        return JsonResponse({'code': 1})
    else:
        return JsonResponse({'code':0})


@check_login
@transaction.atomic
def param_delete(request):
    try:
        id = request.POST.get('id')
        param = InterfaceParam.objects.get(id=id)
        param.delete()
        RedisOpt.delete('interface_param_'+param.param_name)
    except Exception:
        return JsonResponse({'code': 1})
    else:
        return JsonResponse({'code': 0})


#########################用例管理##############################


@check_login
def case_list_page(request):
    return render(request,'interface/case_list.html',{})


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
    cases = InterfaceCase.objects.all()
    # 方式一
    if moduleId:
        cases = InterfaceCase.objects.filter(module__id=moduleId)
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
        rows.append({'id': case.id, 'case_no': case.case_no, 'case_name': case.case_name,'case_description': case.case_description, 'run_flag':case.run_flag,'url':case.url,'content_type':case.content_type,'request_method':case.request_method,'request_param':case.request_param,'builder':case.builder})
    return HttpResponse(json.dumps({'total': total, 'rows': rows},cls=LocalDateEncoder))


@check_login
def case_add_page(request):
    moduleId  = request.GET.get('moduleId')
    user_name = request.COOKIES.get('user_name', '').encode('latin-1').decode('utf-8')
    return render(request,'interface/case_add.html',{'moduleId':moduleId,'user_name':user_name})


@check_login
def case_no_is_exist(request):
    case_no = request.POST.get('case_no')
    original_no = request.POST.get('original_no')
    if original_no is not None and case_no==original_no:
        return HttpResponse('true')
    else:
        case = InterfaceCase.objects.filter(case_no=case_no)
        if case:
            return HttpResponse('false')
        else:
            return HttpResponse('true')


@check_login
def case_add(request):
    try:
        case = InterfaceCase()
        moduleId = request.POST.get('moduleId')
        case_no = request.POST.get('case_no')
        case_name = request.POST.get('case_name')
        case_description = request.POST.get('case_description')
        run_flag = request.POST.get('run_flag')
        url = request.POST.get('url')
        request_method = request.POST.get('request_method')
        content_type = request.POST.get('content_type')
        request_header = request.POST.get('request_header')
        request_cookie = request.POST.get('request_cookie')
        request_param = request.POST.get('request_param')
        assert_type = request.POST.get('assert_type')
        assert_partern = request.POST.get('assert_partern')
        builder = request.POST.get('builder')
        module = Module.objects.get(id=moduleId)
        case.case_no = case_no
        case.case_name = case_name
        case.case_description = case_description
        case.run_flag = run_flag
        case.url = url
        case.request_method = request_method
        case.content_type = content_type
        case.request_header = request_header
        case.request_cookie = request_cookie
        case.request_param = request_param
        case.assert_type = assert_type
        case.assert_partern = assert_partern
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
        case = InterfaceCase.objects.filter(id=id)
        case.delete()
    except Exception:
        return JsonResponse({'code': 1})
    else:
        return JsonResponse({'code': 0})


@check_login
def case_edit_page(request):
    id = request.GET.get('id')
    interfaceCase = InterfaceCase.objects.get(id=id)
    interfaceCase.build_time = interfaceCase.build_time.strftime('%Y-%m-%d %H:%M:%S')
    interfaceCase.modify_time = interfaceCase.modify_time.strftime('%Y-%m-%d %H:%M:%S')
    return render(request,'interface/case_edit.html',{'interfaceCase':interfaceCase})


@check_login
def case_edit(request):
    try:
        id = request.POST.get('id')
        case_no = request.POST.get('case_no')
        case_name = request.POST.get('case_name')
        case_description = request.POST.get('case_description')
        run_flag = request.POST.get('run_flag')
        url = request.POST.get('url')
        request_method = request.POST.get('request_method')
        content_type = request.POST.get('content_type')
        request_header = request.POST.get('request_header')
        request_cookie = request.POST.get('request_cookie')
        request_param = request.POST.get('request_param')
        assert_type = request.POST.get('assert_type')
        assert_partern = request.POST.get('assert_partern')
        case = InterfaceCase.objects.get(id=id)
        case.case_no = case_no
        case.case_name = case_name
        case.content_type = content_type
        case.run_flag = run_flag
        case.url = url
        case.request_method = request_method
        case.assert_type = assert_type
        if case_description is not None:
            case.case_description = case_description
        if request_header is not None:
            case.request_header = request_header
        if request_cookie is not None:
            case.request_cookie = request_cookie
        if request_param is not None:
            case.request_param = request_param
        if assert_partern is not None:
            case.assert_partern = assert_partern
            case.save()
    except Exception as e:
        logger.error(e)
        return JsonResponse({'code': 1})
    else:
        return JsonResponse({'code':0})

@check_login
def case_copy_page(request):
    case_id = request.GET.get('caseId')
    user_name = request.COOKIES.get('user_name', '').encode('latin-1').decode('utf-8')
    interfaceCase = InterfaceCase.objects.get(id=case_id)
    interfaceCase.builder = user_name
    return render(request,'interface/case_copy.html',{'interfaceCase':interfaceCase})

@check_login
def case_batch_delete(request):
    try:
        ids = request.POST.getlist('ids')  # django接收数组
        cases = InterfaceCase.objects.filter(id__in = ids)
        cases.delete()
    except Exception as e:
        return JsonResponse({'code': 1})
    else:
        return JsonResponse({'code': 0})


@check_login
def case_execute(request):
    """单个测试用例执行"""
    id = request.POST.get('id')
    case = InterfaceCase.objects.get(id=id)
    logger.info('执行单个接口用例：%s'% (case.case_name))
    result = runCase.run_case_by_data(case,None)
    return JsonResponse(result)


#########################用例集管理##############################


@check_login
def suit_list_page(request):
    return render(request,'interface/suit_list.html',{})


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
    suits = InterfaceSuit.objects.all()
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
    return render(request,'interface/suit_add.html',{'user_name':user_name})


@check_login
def suit_add(request):
    try:
        suit = InterfaceSuit()
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
    suit = InterfaceSuit.objects.get(id=id)
    suit.build_time = suit.build_time.strftime('%Y-%m-%d %H:%M:%S')
    suit.modify_time = suit.modify_time.strftime('%Y-%m-%d %H:%M:%S')
    return render(request,'interface/suit_edit.html',{'suit':suit})


@check_login
def suit_edit(request):
    try:
        id = request.POST.get('id')
        suit_no = request.POST.get('suit_no')
        suit_name = request.POST.get('suit_name')
        suit_description = request.POST.get('suit_description')
        suit = InterfaceSuit.objects.get(id=id)
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
        suit = InterfaceSuit.objects.filter(id=id)
        suit.delete()
    except Exception:
        return JsonResponse({'code': 1})
    else:
        return JsonResponse({'code': 0})


@check_login
def suit_case_list_page(request):
    suitId = request.GET.get('suitId')
    return render(request,'interface/suit_case_list.html',{'suitId':suitId})


@check_login
def suit_case_list(request):
    size = request.GET.get('size')
    page = request.GET.get('page')
    suitId = request.GET.get('suitId')
    case_no = request.GET.get('case_no')
    case_name = request.GET.get('case_name')
    right_boundary = int(page) * int(size)
    suit = InterfaceSuit.objects.get(id=suitId)
    cases = suit.interface_case
    if case_no:
        cases = cases.filter(Q(case_no__contains=case_no))
    if case_name:
        cases = cases.filter(Q(case_name__contains=case_name))
    # 记录总数
    total = cases.count()
    cases = cases.order_by('id')[int(size) * (int(page) - 1):right_boundary]  # 分页切片
    rows = []
    for case in cases:
        rows.append({'id': case.id, 'case_no': case.case_no, 'case_name': case.case_name,'case_description': case.case_description, 'run_flag': case.run_flag, 'url': case.url,'request_method': case.request_method, 'content_type': case.content_type,'request_param': case.request_param,'builder': case.builder})
    return HttpResponse(json.dumps({'total': total, 'rows': rows}, cls=LocalDateEncoder))


@check_login
def suit_case_add_page(request):
    suitId = request.GET.get('suitId')
    return render(request,'interface/suit_case_add.html',{'suitId':suitId})


@check_login
@transaction.atomic
def suit_case_add(request):
    try:
        caseIds = request.POST.getlist('caseIds')
        suitId = request.POST.get('suitId')
        suit = InterfaceSuit.objects.get(id=suitId)
        suit.interfaceCase.add(*caseIds)
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
        suit = InterfaceSuit.objects.get(id=suitId)
        suit.interfaceCase.remove(*caseIds)
    except Exception as e:
        return JsonResponse({'code': 1})
    else:
        return JsonResponse({'code': 0})


# 利用redis+celery实现后台异步请求
# @check_login
# def suit_execute(request):
#     # try:
#         suitId = request.POST.get('suitId')
#         execute_person = request.COOKIES.get('user_name', '').encode('latin-1').decode('utf-8')
#         # 开启异步任务，执行用例集
#         execute_interface_case_suit.delay(suitId,execute_person)
#         # 返回执行成功
#         return JsonResponse({'code': 0})
#     # except Exception as e:
#     #     return JsonResponse({'code': 1})


@check_login
def suit_execute(request):
    try:
        suitId = request.POST.get('suitId')
        execute_person = request.COOKIES.get('user_name', '').encode('latin-1').decode('utf-8')
        # 开启异步任务，执行用例集
        case_suit = InterfaceSuit.objects.get(id=suitId)
        logger.info('执行接口用例集：%s开始' % (case_suit.suit_name))
        case_list = case_suit.interface_case.all()
        # 获取所有cookie列数据，判断是否存在用例依赖
        cookies = []
        for case in case_list:
            cookies.append(case.request_cookie)
        # 如果匹配${test_01}成功，则表示存在依赖
        pattern = '^\$\{(.[^\.]+)\}$'
        cookie_list = []
        match_result = None
        for cookie_depend in cookies:
            if cookie_depend is not None:
                match_result = re.match(pattern, cookie_depend)
            if match_result:
                cookie_list.append(match_result.group(1))
        runCase.cookie_dict = dict.fromkeys(cookie_list, '')
        interfacesuitexecuterecord = InterfaceSuitExecuteRecord()
        interfacesuitexecuterecord.start_time = timezone.now()
        interfacesuitexecuterecord.execute_person = execute_person
        interfacesuitexecuterecord.ececute_status = 2  # 执行中状态
        interfacesuitexecuterecord.interface_suit = case_suit
        interfacesuitexecuterecord.save()
        for case_data in case_list:
            runCase.run_case_by_data(case_data, interfacesuitexecuterecord)
        interfacesuitexecuterecord.end_time = timezone.now()
        interfacesuitexecuterecord.ececute_status=3     # 执行结束状态
        interfacesuitexecuterecord.save()
        logger.info('执行接口用例集：%s结束' % (case_suit.suit_name))
        # 返回执行成功
        return JsonResponse({'code': 0})
    except Exception as e:
        return JsonResponse({'code': 1})


#########################日志管理##############################


@check_login
def log_list_page(request):
    return render(request,'interface/log_list.html',{})


@check_login
def log_list(request):
    """查询日志目录下的所有文件"""
    log_dir = RedisOpt.get_str('interface_param_LogDir')
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
        log_size = FileUtil.get_file_size(log_dir+'/'+list_file).__str__()+RedisOpt.get_str('sys_param_FileSizeUnit')
        build_time = FileUtil.get_create_time(log_dir+'/'+list_file)
        modify_time = FileUtil.get_last_modify_time(log_dir+'/'+list_file)
        rows.append({'log_name':list_file,'log_size':log_size,'build_time':build_time,'modify_time':modify_time})
    return HttpResponse(json.dumps({'total': total, 'rows': rows}, cls=LocalDateEncoder))


@check_login
def log_detail_page(request):
    log_name = request.GET.get('logName')
    log_dir = RedisOpt.get_str('interface_param_LogDir')
    log_size = RedisOpt.get_str('sys_param_LogFontSize')
    file_path = log_dir+'/'+log_name
    file_content = ""
    with open(file_path,'rb') as file:
        file_content = file.read()
        file_content = "<style>body{font-size:"+log_size+"px;}</style>"+file_content.decode(encoding='UTF-8').replace('\n','<br/>')
    return HttpResponse(file_content)


#########################测试报告##############################


@check_login
def report_list_page(request):
    return render(request,'interface/report_list.html',{})


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
    suit_execute_records = InterfaceSuitExecuteRecord.objects.all()
    if suit_name:
        interface_suits = InterfaceSuit.objects.filter(suit_name__contains=suit_name)
        suit_execute_records = suit_execute_records.filter(interface_suit__in=interface_suits)
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
        rows.append({'id': suit_record.id, 'ececute_status': suit_record.ececute_status, 'execute_person': suit_record.execute_person,'start_time': suit_record.start_time, 'end_time':suit_record.end_time,'suit_no':suit_record.interface_suit.suit_no,'suit_name':suit_record.interface_suit.suit_name})
    return HttpResponse(json.dumps({'total': total, 'rows': rows},cls=LocalDateEncoder))


@check_login
def report_detail_page(request):
    suit_record_id = request.GET.get("id")
    moduleResultSet = InterfaceSuitCaseExecuteRecord.objects.filter(interface_suit_execute_record__id=suit_record_id).values('module_name').annotate(count=Count(1))
    module_legend_data = []
    module_series_data = []
    for result in moduleResultSet:
        module_legend_data.append(result['module_name'])
        module_series_data.append({"value": result['count'], "name":result['module_name']})
    module_chart_option={"text":"模块用例数统计","legend_data":module_legend_data,"series_name":"模块名称","series_data":module_series_data}

    statusResultSet = InterfaceSuitCaseExecuteRecord.objects.filter(interface_suit_execute_record__id=suit_record_id).values('pass_flag').annotate(count=Count(1))
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
    return render(request,'interface/report_detail.html',{"suit_record_id":suit_record_id,"moduleChartOption":module_chart_option,"statusChartOption":status_chart_option})


@check_login
def report_detail(request):
    suit_record_id = request.GET.get('suit_record_id')
    page = request.GET.get('page')
    size = request.GET.get('size')
    # 条件过滤查询，page为页码，size为页大小，right_boundary为分页右边界
    right_boundary = int(page) * int(size)
    case_records = InterfaceSuitCaseExecuteRecord.objects.filter(interface_suit_execute_record_id=suit_record_id)
    # 记录总数
    total = case_records.count()
    case_records = case_records.order_by('id')[int(size) * (int(page) - 1):right_boundary]     #分页切片
    rows = []
    for case_record in case_records:
        if case_record.end_time is not None:
            rows.append({'module_name': case_record.module_name, 'case_no': case_record.case_no,
                         'case_name': case_record.case_name, 'case_description': case_record.case_description,
                         'builder': case_record.builder, 'url': case_record.url,
                         'request_method': case_record.request_method, 'request_param': case_record.request_param,
                         'assert_type': case_record.assert_type, 'status_code': case_record.status_code,
                         'real_result': case_record.real_result, 'start_time': case_record.start_time,
                         'end_time': case_record.end_time,
                         'period': (case_record.end_time - case_record.start_time).microseconds / 1000,
                         'pass_flag': case_record.pass_flag, 'exception_msg': case_record.exception_msg})
        else:
            rows.append({'module_name': case_record.module_name, 'case_no': case_record.case_no,
                         'case_name': case_record.case_name, 'case_description': case_record.case_description,
                         'builder': case_record.builder, 'url': case_record.url,
                         'request_method': case_record.request_method, 'request_param': case_record.request_param,
                         'assert_type': case_record.assert_type, 'status_code': case_record.status_code,
                         'real_result': case_record.real_result, 'start_time': case_record.start_time,
                         'end_time': '',
                         'period': '',
                         'pass_flag': case_record.pass_flag, 'exception_msg': case_record.exception_msg})
    return HttpResponse(json.dumps({'total': total, 'rows': rows},cls=LocalDateEncoder))

