# -*- coding: UTF-8 -*-

from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.shortcuts import render,redirect
from sys_manager.models import ManagerUser,Module,SysParam
from django.db.models import Q
from django.contrib import auth
from functools import wraps
from TestAutomation.encrypt_utils import md5_encrypt,token_encrypt,token_decrypt
from TestAutomation.date_utils import LocalDateEncoder
import json


login_token_dict = {}

#######################系统登录################################

def login(request):
    return render(request, '../templates/login.html', {})


def login_check(request):
    account = request.POST.get('account')
    password = request.POST.get('password')
    password = md5_encrypt(password)
    user = ManagerUser.objects.filter(Q(account=account)&Q(password=password))
    if user:
        # 设置coookie信息，保存用户名
        response = redirect("/index")
        username = user[0].user_name
        username = username.encode('utf-8').decode('latin-1')
        response.set_cookie("user_name", username,30000)   # cookie有效期为300秒
        # 设置session信息，保存登录状态
        token = token_encrypt(account)
        request.session['login_token'] = token
        # token在缓存中存一份
        login_token_dict[account] = token
        return response
    else:
        request.session['msg'] = u'用户名或密码错误'
        return redirect('/login')


def check_login(f):
    @wraps(f)       # 取消装饰器装饰完成之后，函数名称改变的问题
    def inner(request, *args, **kwargs):
        if request.session.get("login_token") in login_token_dict.values():    # 如果session中（is_login）对应的value为1,就执行f()函数，否则，返回登录页面
            return f(request, *args, **kwargs)
        else:
            return redirect("/login")
    return inner


# django自带认证
def login_check_self(request):
    account = request.POST.get('account')
    password = request.POST.get('password')
    user = auth.authenticate(username=account,password=password)
    if user is not None and user.is_active:
        auth.login(request,user)
        request.session['user_name'] = user.user_name
        response = HttpResponseRedirect('/index')
        return response
    else:
        return redirect('/login')

def logout(request):
    response = redirect("/login")
    response.delete_cookie('user_name')
    del request.session['login_token']
    return response

@check_login
def index(request):
    user_name = request.COOKIES.get('user_name','').encode('latin-1').decode('utf-8')
    return render(request, '../templates/index.html', {'user_name':user_name})

@check_login
def main(request):
    return render(request, '../templates/main.html', {})

@check_login
def example(request):
    return render(request,'sys/example.html',{})


########################用户管理###############################


@check_login
def user_list_page(request):
    return render(request, 'sys/user_list.html', {})

@check_login
def user_list(request):
    user_name = request.GET.get('user_name')
    gender = request.GET.get('gender')
    account = request.GET.get('account')
    page = request.GET.get('page')
    size = request.GET.get('size')
    # 条件过滤查询，page为页码，size为页大小，right_boundary为分页右边界
    right_boundary = int(page) * int(size)
    page_user = ManagerUser.objects.all()
    if user_name:
        page_user = page_user.filter(Q(user_name__contains=user_name))
    if gender:
        page_user = page_user.filter(Q(gender=gender))
    if account:
        page_user = page_user.filter(Q(account__contains=account))
    # 记录总数
    total = page_user.count()
    page_user = page_user.order_by('id')[int(size) * (int(page) - 1):right_boundary]     #分页切片
    rows = []
    for user in page_user:
        rows.append({'id': user.id, 'user_name': user.user_name, 'gender': user.gender,'account': user.account, 'comment':user.comment,'build_time':user.build_time})
    return HttpResponse(json.dumps({'total': total, 'rows': rows},cls=LocalDateEncoder))        # LocalDateEncoder为日期格式转换类

@check_login
def user_add_page(request):
    return render(request,'sys/user_add.html',{})

@check_login
# 判断用户是否可用
def user_account_is_exist(request):
    account = request.POST.get('account')
    original_account = request.POST.get('original_account')
    if original_account is not None and account == original_account:
        return HttpResponse('true')
    else:
        user = ManagerUser.objects.filter(account=account)
        if user:
            return HttpResponse('false')
        else:
            return HttpResponse('true')

@check_login
def user_add(request):
    try:
        module = ManagerUser()
        user_name = request.POST.get('user_name')
        gender = request.POST.get('gender')
        account = request.POST.get('account')
        password = request.POST.get('password')
        password = md5_encrypt(password)
        comment = request.POST.get('comment')
        module.user_name = user_name
        module.gender = gender
        module.account = account
        module.password = password
        module.comment = comment
        module.save()
    except Exception:
        return JsonResponse({'code': 1})
    else:
        return JsonResponse({'code':0})

@check_login
def user_edit_page(request):
    id = request.GET.get('id')
    user = ManagerUser.objects.get(id=id)
    return render(request,'sys/user_edit.html',{'user':user})

@check_login
def user_edit(request):
    try:
        id = request.POST.get('id')
        user_name = request.POST.get('user_name')
        gender = request.POST.get('gender')
        account = request.POST.get('account')
        password = request.POST.get('password')
        comment = request.POST.get('comment')
        user = ManagerUser.objects.get(id=id)
        user.user_name = user_name
        user.gender = gender
        user.account = account
        if password is not None and password != '':
            password = md5_encrypt(password)
            user.password = password
        user.comment = comment
        user.save()
    except Exception:
        return JsonResponse({'code': 1})
    else:
        return JsonResponse({'code':0})

@check_login
def user_delete(request):
    try:
        id = request.POST.get('id')
        user = ManagerUser.objects.filter(id=id)
        user.delete()
    except Exception:
        return JsonResponse({'code': 1})
    else:
        return JsonResponse({'code': 0})

@check_login
def user_batch_delete(request):
    try:
        ids = request.POST.getlist('ids')  # django接收数组
        users = ManagerUser.objects.filter(id__in = ids)
        users.delete()
    except Exception as e:
        return JsonResponse({'code': 1})
    else:
        return JsonResponse({'code': 0})


#########################模块管理##############################
@check_login
def module_list_page(request):
    return render(request, 'sys/module_list.html', {})

@check_login
def get_children_by_parentId(parentId):
    modules = None
    if parentId is None or parentId == '':
        modules = Module.objects.filter(parent_module_id=None)
    else:
        modules = Module.objects.filter(parent_module_id=parentId)
    result = []
    if modules:
        for module in modules:
            text = module.module_number+'_'+module.module_name
            result.append({'id':module.id,'text':text,'children':get_children_by_parentId(module.id)})
    return result

@check_login
def module_tree(request):
    """递归获取模块节点树"""
    result = get_children_by_parentId('')
    return HttpResponse(json.dumps(result))

@check_login
def get_module_by_id(request):
    try:
        id = request.POST.get('id')
        module = Module.objects.get(id=id)
        moduleDict = {'id':module.id,'module_number':module.module_number,'module_name':module.module_name,'module_type':module.module_type,'module_desc':module.module_desc,'manager':module.manager,'builder':module.builder,'build_time':module.build_time}
    except Exception as e:
        print(e)
        return HttpResponse(json.dumps({'code':1,'data': {}}, cls=LocalDateEncoder))
    else:
        return HttpResponse(json.dumps({'code':0,'data': moduleDict}, cls=LocalDateEncoder))

@check_login
def module_number_is_exist(request):
    module_number = request.POST.get('module_number')
    original_number = request.POST.get('original_number')
    if original_number is not None and module_number==original_number:
        return HttpResponse('true')
    else:
        module = Module.objects.filter(module_number=module_number)
        if module:
            return HttpResponse('false')
        else:
            return HttpResponse('true')

@check_login
def module_add_page(request):
    subId = request.GET.get('subId')
    if subId is None:
        subId = ''
    user_name = request.COOKIES.get('user_name', '').encode('latin-1').decode('utf-8')
    return render(request,'sys/module_add.html',{'subId':subId,'user_name':user_name})

@check_login
def module_add(request):
    try:
        module = Module()
        subId = request.POST.get('subId')
        print(subId)
        module_number = request.POST.get('module_number')
        module_name = request.POST.get('module_name')
        module_type = request.POST.get('module_type')
        manager = request.POST.get('manager')
        builder = request.POST.get('builder')
        module_desc = request.POST.get('module_desc')
        module.module_number = module_number
        module.module_name = module_name
        module.module_type = module_type
        module.manager = manager
        module.builder = builder
        module.module_desc = module_desc
        if subId is None or subId == '':
            pass
        else:
            id = int(subId)
            module.parent_module = Module.objects.get(id=id)
        module.save()
    except Exception as e:
        print(e)
        return JsonResponse({'code': 1})
    else:
        return JsonResponse({'code':0})

@check_login
def module_edit_page(request):
    id = request.GET.get('id')
    module = Module.objects.get(id=id)
    return render(request,'sys/module_edit.html',{'module':module})

@check_login
def module_edit(request):
    try:
        id = request.POST.get('id')
        module_number = request.POST.get('module_number')
        module_name = request.POST.get('module_name')
        module_type = request.POST.get('module_type')
        manager = request.POST.get('manager')
        builder = request.POST.get('builder')
        module_desc = request.POST.get('module_desc')
        module = Module.objects.get(id=id)
        module.module_number = module_number
        module.module_name = module_name
        module.module_type = module_type
        if manager is not None:
            module.manager = manager
        if builder is not None:
            module.builder = builder
        if module_desc is not None:
            module.module_desc = module_desc
        module.save()
    except Exception:
        return JsonResponse({'code': 1})
    else:
        return JsonResponse({'code':0})

@check_login
def module_delete(request):
    try:
        id = request.POST.get('id')
        module = Module.objects.filter(id=id)
        module.delete()
    except Exception:
        return JsonResponse({'code': 1})
    else:
        return JsonResponse({'code': 0})


#########################系统参数##############################
@check_login
def sysParam_list_page(request):
    return render(request,'sys/sysParam_list.html',{})

@check_login
def sysParam_list(request):
    param_name = request.GET.get('param_name')
    belong_menu = request.GET.get('belong_menu')
    page = request.GET.get('page')
    size = request.GET.get('size')
    # 条件过滤查询，page为页码，size为页大小，right_boundary为分页右边界
    right_boundary = int(page) * int(size)
    sysParams = SysParam.objects.all()
    if param_name:
        sysParams = sysParams.filter(Q(param_name__contains=param_name))
    if belong_menu:
        sysParams = sysParams.filter(Q(belong_menu__contains=belong_menu))
    # 记录总数
    total = sysParams.count()
    sysParams = sysParams.order_by('id')[int(size) * (int(page) - 1):right_boundary]     #分页切片
    rows = []
    for sysParam in sysParams:
        rows.append({'id': sysParam.id, 'param_name': sysParam.param_name, 'param_value': sysParam.param_value,'belong_menu': sysParam.belong_menu, 'description':sysParam.description,'build_time':sysParam.build_time})
    return HttpResponse(json.dumps({'total': total, 'rows': rows},cls=LocalDateEncoder))

@check_login
def sysParam_add_page(request):
    return render(request,'sys/sysParam_add.html',{})

@check_login
def sysParam_add(request):
    try:
        sysParam = SysParam()
        param_name = request.POST.get('param_name')
        param_value = request.POST.get('param_value')
        belong_menu = request.POST.get('belong_menu')
        description = request.POST.get('description')
        sysParam.param_name = param_name
        sysParam.param_value = param_value
        sysParam.belong_menu = belong_menu
        sysParam.description = description
        sysParam.save()
    except Exception:
        return JsonResponse({'code': 1})
    else:
        return JsonResponse({'code':0})

@check_login
def sysParam_edit_page(request):
    id = request.GET.get('id')
    sysParam = SysParam.objects.get(id=id)
    return render(request,'sys/sysParam_edit.html',{'sysParam':sysParam})

@check_login
def sysParam_edit(request):
    try:
        id = request.POST.get('id')
        param_name = request.POST.get('param_name')
        param_value = request.POST.get('param_value')
        description = request.POST.get('description')
        belong_menu = request.POST.get('belong_menu')
        sysParam = SysParam.objects.get(id=id)
        sysParam.param_name = param_name
        sysParam.param_value = param_value
        if description is not None:
            sysParam.description = description
        if belong_menu is not None:
            sysParam.belong_menu = belong_menu
        sysParam.save()
    except Exception:
        return JsonResponse({'code': 1})
    else:
        return JsonResponse({'code':0})

@check_login
def sysParam_delete(request):
    try:
        id = request.POST.get('id')
        sysParam = SysParam.objects.filter(id=id)
        sysParam.delete()
    except Exception:
        return JsonResponse({'code': 1})
    else:
        return JsonResponse({'code': 0})