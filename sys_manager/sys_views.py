# -*- coding: UTF-8 -*-

from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.shortcuts import render,redirect
from sys_manager.models import ManagerUser,Module,SysParam,Task
from interface_auto.models import InterfaceParam,InterfaceSuit
from web_auto.models import UiParam,UiSuit
from django.db.models import Q
from django.contrib import auth
from functools import wraps
from TestAutomation.encrypt_utils import md5_encrypt,token_encrypt,token_decrypt
from TestAutomation.date_utils import LocalDateEncoder
from TestAutomation.utils.redis_util import RedisOpt
from TestAutomation.utils.logger_util import Logger
from TestAutomation.utils.file_util import FileUtil
from django.db import transaction
import json


def init_parameters():
    """初始化配置参数至redis"""
    sys_parameters = SysParam.objects.all()
    ui_parameters = UiParam.objects.all()
    interface_parameters = InterfaceParam.objects.all()
    for sys_parameter in sys_parameters:
        RedisOpt.set('sys_param_'+sys_parameter.param_name,sys_parameter.param_value)
    for ui_parameter in ui_parameters:
        RedisOpt.set('ui_param_'+ui_parameter.param_name,ui_parameter.param_value)
    for interface_parameter in interface_parameters:
        RedisOpt.set('interface_param_'+interface_parameter.param_name,interface_parameter.param_value)


init_parameters()

# 日志对象定义和初始化
log_dir = RedisOpt.get_str('sys_param_LogDir')
log_console = RedisOpt.get_str('sys_param_LogConsole')
log_level = RedisOpt.get_str('sys_param_LogLevel')
logger = Logger('SysViews',log_dir,log_console,log_level).logger

#######################系统登录################################


def login(request):
    return render(request, 'login.html', {})


def login_check(request):
    account = request.POST.get('account')
    password = request.POST.get('password')
    password = md5_encrypt(password)
    user = ManagerUser.objects.filter(Q(account=account)&Q(password=password))
    if user:
        # 设置coookie信息，保存用户名和账号
        response = redirect("/index")
        username = user[0].user_name
        username = username.encode('utf-8').decode('latin-1')
        logger.info('账号%s登录成功，用户名：%s'% (account, username))
        login_expire_time = RedisOpt.get('sys_param_LoginExpireTime')
        if login_expire_time is None:
            login_expire_time = '600'
        response.set_cookie("user_name", username)
        response.set_cookie("account", account)
        # 设置session信息，保存登录的token
        token = token_encrypt(account)
        request.session.set_expiry(int(login_expire_time))     # 登录后设置session有效期
        request.session[account] = token
        return response
    else:
        logger.info('账号%s登录失败'% account)
        return render(request, 'login.html', {'msg':'账号或密码错误'})


def check_login(f):
    @wraps(f)       # 取消装饰器装饰完成之后，函数名称改变的问题
    def inner(request, *args, **kwargs):
        account = request.COOKIES.get('account', '').encode('latin-1').decode('utf-8')
        if account is None:
            return redirect("/login")
        elif request.session.get(account):
            login_expire_time = RedisOpt.get('sys_param_LoginExpireTime')   # 每次执行操作都经过登录检查，重新设置session有效时间
            request.session.set_expiry(int(login_expire_time))
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

@check_login
def logout(request):
    account = request.COOKIES.get('account', '').encode('latin-1').decode('utf-8')
    response = redirect("/login")
    response.delete_cookie('user_name')
    response.delete_cookie('account')
    if account:
        del request.session[account]
        logger.info('账号%s退出登录' % account)
    return response


@check_login
def index(request):
    user_name = request.COOKIES.get('user_name','').encode('latin-1').decode('utf-8')
    return render(request, 'index.html', {'user_name':user_name})


@check_login
def main(request):
    return render(request, 'main.html', {})


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
def user_account_is_exist(request):
    """判断用户账号是否可用"""
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
        user = ManagerUser.objects.get(id=id)
        user.delete()
        logger.info('删除用户%s' % user.user_name)
    except Exception:
        return JsonResponse({'code': 1})
    else:
        return JsonResponse({'code': 0})


@check_login
@transaction.atomic
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
@transaction.atomic
def module_delete(request):
    try:
        id = request.POST.get('id')
        module = Module.objects.get(id=id)
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
@transaction.atomic
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
        RedisOpt.set('sys_param_' + param_name, param_value)
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
@transaction.atomic
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
        RedisOpt.set('sys_param_' + param_name, param_value)
    except Exception:
        return JsonResponse({'code': 1})
    else:
        return JsonResponse({'code':0})


@check_login
@transaction.atomic
def sysParam_delete(request):
    try:
        id = request.POST.get('id')
        sysParam = SysParam.objects.get(id=id)
        sysParam.delete()
        RedisOpt.delete('sys_param_'+sysParam.param_name)
    except Exception:
        return JsonResponse({'code': 1})
    else:
        return JsonResponse({'code': 0})


#########################日志管理##############################


@check_login
def log_list_page(request):
    return render(request,'sys/log_list.html',{})


@check_login
def log_list(request):
    """查询日志目录下的所有文件"""
    log_dir = RedisOpt.get_str('sys_param_LogDir')
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
    log_dir = RedisOpt.get_str('sys_param_LogDir')
    log_size = RedisOpt.get_str('sys_param_LogFontSize')
    file_path = log_dir+'/'+log_name
    file_content = ""
    with open(file_path,'rb') as file:
        file_content = file.read()
        file_content = "<style>body{font-size:"+log_size+"px;}</style>"+file_content.decode(encoding='UTF-8').replace('\n','<br/>')
    return HttpResponse(file_content)


#########################定时任务管理##############################


@check_login
def task_list_page(request):
    return render(request,'sys/task_list.html',{})

@check_login
def task_list(request):
    run_flag = request.GET.get('run_flag')
    task_type = request.GET.get('task_type')
    task_name = request.GET.get('task_name')
    task_no = request.GET.get('task_no')
    page = request.GET.get('page')
    size = request.GET.get('size')
    # 条件过滤查询，page为页码，size为页大小，right_boundary为分页右边界
    right_boundary = int(page) * int(size)
    tasks = Task.objects.all()
    if run_flag:
        tasks = tasks.filter(run_flag=run_flag)
    if task_type:
        tasks = tasks.filter(task_type=task_type)
    if task_name:
        tasks = tasks.filter(task_name__contains=task_name)
    if task_no:
        tasks = tasks.filter(task_no__contains=task_no)
    # 记录总数
    total = tasks.count()
    tasks = tasks.order_by('id')[int(size) * (int(page) - 1):right_boundary]     #分页切片
    rows = []
    for task in tasks:
        suit_name = ''
        if task.task_type == 1:
            suit_name = InterfaceSuit.objects.get(id=task.suit_id).suit_name
        elif task.task_type == 2:
            suit_name = UiSuit.objects.get(id=task.suit_id).suit_name
        else:
            pass
        logger.info('任务%s对应的用例集为：%s'% (task.task_name,suit_name))
        rows.append({'id':task.id,'task_no': task.task_no, 'task_name': task.task_name, 'task_type': task.task_type,'task_desc': task.task_desc, 'task_partern':task.task_partern,'run_flag':task.run_flag,'manager':task.manager,'builder':task.builder,'build_time':task.build_time,'modify_time':task.modify_time,'suit_name':suit_name,'suit_id':task.suit_id})
    return HttpResponse(json.dumps({'total': total, 'rows': rows},cls=LocalDateEncoder))

@check_login
def task_suit_list(request):
    suit_type = request.POST.get('suit_type')
    suit_list = []
    if suit_type == '1':
        suits = InterfaceSuit.objects.all()
    elif suit_type == '2':
        suits = UiSuit.objects.all()
    for suit in suits:
        suit_list.append({'id':suit.id,'suit_name':suit.suit_name})
    return JsonResponse({'suits':suit_list})

@check_login
def task_add_page(request):
    user_name = request.COOKIES.get('user_name', '').encode('latin-1').decode('utf-8')
    suits = InterfaceSuit.objects.all()
    return render(request,'sys/task_add.html',{'user_name':user_name,'suits':suits})

@check_login
def task_add(request):
    try:
        task = Task()
        task_no = request.POST.get('task_no')
        task_name = request.POST.get('task_name')
        task_type = request.POST.get('task_type')
        task_desc = request.POST.get('task_desc')
        task_partern = request.POST.get('task_partern')
        suit_id = request.POST.get('suit_id')
        run_flag = request.POST.get('run_flag')
        manager = request.POST.get('manager')
        builder = request.POST.get('builder')
        task.task_no = task_no
        task.task_name = task_name
        task.task_type = task_type
        task.task_partern = task_partern
        task.run_flag = run_flag
        task.suit_id = suit_id
        if task_desc:
            task.task_desc = task_desc
        if manager:
            task.manager = manager
        if builder:
            task.builder = builder
        task.save()
    except Exception:
        return JsonResponse({'code': 1})
    else:
        return JsonResponse({'code':0})

@check_login
def task_edit_page(request):
    id = request.GET.get('id')
    task = Task.objects.get(id=id)
    suit = None
    if task.task_type == 1:
        suit = InterfaceSuit.objects.get(id=task.suit_id)
        suits = InterfaceSuit.objects.all()
    elif task.task_type == 2:
        suit = UiSuit.objects.get(id=task.suit_id)
        suits = UiSuit.objects.all()
    return render(request,'sys/task_edit.html',{'task':task,'suit':suit,'suits':suits})

@check_login
def task_edit(request):
    try:
        id = request.POST.get('id')
        task = Task.objects.get(id=id)
        task_no = request.POST.get('task_no')
        task_name = request.POST.get('task_name')
        task_type = request.POST.get('task_type')
        task_desc = request.POST.get('task_desc')
        task_partern = request.POST.get('task_partern')
        suit_id = request.POST.get('suit_id')
        run_flag = request.POST.get('run_flag')
        manager = request.POST.get('manager')
        builder = request.POST.get('builder')
        task.task_no = task_no
        task.task_name = task_name
        task.task_type = task_type
        task.task_partern = task_partern
        task.run_flag = run_flag
        task.suit_id = suit_id
        if task_desc:
            task.task_desc = task_desc
        if manager:
            task.manager = manager
        if builder:
            task.builder = builder
        task.save()
    except Exception:
        return JsonResponse({'code': 1})
    else:
        return JsonResponse({'code':0})

@check_login
def task_delete(request):
    try:
        id = request.POST.get('id')
        task = Task.objects.get(id=id)
        task.delete()
    except Exception:
        return JsonResponse({'code': 1})
    else:
        return JsonResponse({'code': 0})