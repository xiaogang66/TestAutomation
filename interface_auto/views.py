# -*- coding: UTF-8 -*-

from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.shortcuts import render,redirect
from sys_manager.models import ManagerUser,Module,SysParam
from interface_auto.models import InterfaceParam,InterfaceCase,InterfaceSuit,InterfaceSuitExecuteRecord,InterfaceSuitCaseExecuteRecord
from django.db.models import Q
from django.contrib import auth
from functools import wraps
from sys_manager.views import check_login
from TestAutomation.encrypt_utils import md5_encrypt,token_encrypt,token_decrypt
from TestAutomation.date_utils import LocalDateEncoder
import json



#########################参数管理##############################


@check_login
def param_list_page(request):
    return render(request,'interface/param_list.html',{})


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


def param_add_page(request):
    return render(request,'interface/param_add.html',{})


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
    except Exception:
        return JsonResponse({'code': 1})
    else:
        return JsonResponse({'code':0})


def param_edit_page(request):
    id = request.GET.get('id')
    param = InterfaceParam.objects.get(id=id)
    return render(request,'interface/param_edit.html',{'param':param})


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
    except Exception:
        return JsonResponse({'code': 1})
    else:
        return JsonResponse({'code':0})


def param_delete(request):
    try:
        id = request.POST.get('id')
        param = InterfaceParam.objects.filter(id=id)
        param.delete()
    except Exception:
        return JsonResponse({'code': 1})
    else:
        return JsonResponse({'code': 0})





@check_login
def case_list_page(request):
    return render(request,'interface/case_list.html',{})


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
        rows.append({'id': case.id, 'case_no': case.case_no, 'case_name': case.case_name,'case_description': case.case_description, 'run_flag':case.run_flag,'url':case.url,'request_method':case.request_method,'request_param':case.request_param,'builder':case.builder})
    return HttpResponse(json.dumps({'total': total, 'rows': rows},cls=LocalDateEncoder))


def case_add_page(request):
    moduleId  = request.GET.get('moduleId')
    user_name = request.COOKIES.get('user_name', '').encode('latin-1').decode('utf-8')
    return render(request,'interface/case_add.html',{'moduleId':moduleId,'user_name':user_name})


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
        request_header = request.POST.get('request_header')
        request_cookie = request.POST.get('request_cookie')
        request_param = request.POST.get('request_param')
        exp_result = request.POST.get('exp_result')
        asset_type = request.POST.get('asset_type')
        asset_partern = request.POST.get('asset_partern')
        builder = request.POST.get('builder')
        module = Module.objects.get(id=moduleId)
        case.case_no = case_no
        case.case_name = case_name
        case.case_description = case_description
        case.run_flag = run_flag
        case.url = url
        case.request_method = request_method
        case.request_header = request_header
        case.request_cookie = request_cookie
        case.request_param = request_param
        case.exp_result = exp_result
        case.asset_type = asset_type
        case.asset_partern = asset_partern
        case.builder = builder
        case.module = module
        case.save()
    except Exception:
        return JsonResponse({'code': 1})
    else:
        return JsonResponse({'code':0})


def case_delete(request):
    try:
        id = request.POST.get('id')
        case = InterfaceCase.objects.filter(id=id)
        case.delete()
    except Exception:
        return JsonResponse({'code': 1})
    else:
        return JsonResponse({'code': 0})


def case_edit_page(request):
    id = request.GET.get('id')
    interfaceCase = InterfaceCase.objects.get(id=id)
    interfaceCase.build_time = interfaceCase.build_time.strftime('%Y-%m-%d %H:%M:%S')
    interfaceCase.modify_time = interfaceCase.modify_time.strftime('%Y-%m-%d %H:%M:%S')
    return render(request,'interface/case_edit.html',{'interfaceCase':interfaceCase})


def case_edit(request):
    try:
        id = request.POST.get('id')
        case_no = request.POST.get('case_no')
        case_name = request.POST.get('case_name')
        case_description = request.POST.get('case_description')
        run_flag = request.POST.get('run_flag')
        url = request.POST.get('url')
        request_method = request.POST.get('request_method')
        request_header = request.POST.get('request_header')
        request_cookie = request.POST.get('request_cookie')
        request_param = request.POST.get('request_param')
        exp_result = request.POST.get('exp_result')
        asset_type = request.POST.get('asset_type')
        asset_partern = request.POST.get('asset_partern')
        case = InterfaceCase.objects.get(id=id)
        case.case_no = case_no
        case.case_name = case_name
        case.run_flag = run_flag
        case.url = url
        case.request_method = request_method
        case.exp_result = exp_result
        case.asset_type = asset_type
        if case_description is not None:
            case.case_description = case_description
        if request_header is not None:
            case.request_header = request_header
        if request_cookie is not None:
            case.request_cookie = request_cookie
        if request_param is not None:
            case.request_param = request_param
        if asset_partern is not None:
            case.asset_partern = asset_partern
            case.save()
    except Exception as e:
        print(e)
        return JsonResponse({'code': 1})
    else:
        return JsonResponse({'code':0})


def case_batch_delete(request):
    try:
        ids = request.POST.getlist('ids')  # django接收数组
        cases = InterfaceCase.objects.filter(id__in = ids)
        cases.delete()
    except Exception as e:
        return JsonResponse({'code': 1})
    else:
        return JsonResponse({'code': 0})


def case_execute(request):
    try:
        id = request.POST.get('id')
        case = InterfaceCase.objects.get(id=id)
        #TODO 执行用例
        flag = False
        msg = 'aaa'
    except Exception as e:
        return JsonResponse({'code': -1,'msg':str(e)})
    else:
        if flag:
            return JsonResponse({'code': 0})
        else:
            return JsonResponse({'code': 1,'msg':msg})


#########################用例集管理##############################


@check_login
def suit_list_page(request):
    return render(request,'interface/suit_list.html',{})


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


def suit_add_page(request):
    user_name = request.COOKIES.get('user_name', '').encode('latin-1').decode('utf-8')
    return render(request,'interface/suit_add.html',{'user_name':user_name})


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


def suit_edit_page(request):
    id = request.GET.get('id')
    suit = InterfaceSuit.objects.get(id=id)
    suit.build_time = suit.build_time.strftime('%Y-%m-%d %H:%M:%S')
    suit.modify_time = suit.modify_time.strftime('%Y-%m-%d %H:%M:%S')
    return render(request,'interface/suit_edit.html',{'suit':suit})


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


def suit_delete(request):
    try:
        id = request.POST.get('id')
        suit = InterfaceSuit.objects.filter(id=id)
        suit.delete()
    except Exception:
        return JsonResponse({'code': 1})
    else:
        return JsonResponse({'code': 0})


def suit_case_list_page(request):
    suitId = request.GET.get('suitId')
    return render(request,'interface/suit_case_list.html',{'suitId':suitId})


def suit_case_list(request):
    size = request.GET.get('size')
    page = request.GET.get('page')
    suitId = request.GET.get('suitId')
    case_no = request.GET.get('case_no')
    case_name = request.GET.get('case_name')
    right_boundary = int(page) * int(size)
    suit = InterfaceSuit.objects.get(id=suitId)
    cases = suit.interfaceCase
    if case_no:
        cases = cases.filter(Q(case_no__contains=case_no))
    if case_name:
        cases = cases.filter(Q(case_name__contains=case_name))
    # 记录总数
    total = cases.count()
    cases = cases.order_by('id')[int(size) * (int(page) - 1):right_boundary]  # 分页切片
    rows = []
    for case in cases:
        rows.append({'id': case.id, 'case_no': case.case_no, 'case_name': case.case_name,
                     'case_description': case.case_description, 'run_flag': case.run_flag, 'url': case.url,
                     'request_method': case.request_method, 'request_param': case.request_param,
                     'builder': case.builder})
    return HttpResponse(json.dumps({'total': total, 'rows': rows}, cls=LocalDateEncoder))


def suit_case_add_page(request):
    suitId = request.GET.get('suitId')
    return render(request,'interface/suit_case_add.html',{'suitId':suitId})


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


def suit_case_delete(request):
    try:
        caseIds = request.POST.getlist('caseIds')  # django接收数组
        suitId = request.POST.get('suitId')
        suit = InterfaceSuit.objects.get(id=suitId)
        suit.interfaceCase.remove(*caseIds)
    except Exception as e:
        return JsonResponse({'code': 1})
    else:
        return JsonResponse({'code': 0})

