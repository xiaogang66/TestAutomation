from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.shortcuts import render,redirect
from sys_manager.models import ManagerUser
from django.db.models import Q
import json

def login(request):
    return render(request, '../templates/login.html', {})

def login_check(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    request.COOKIES['username']=username
    if username == 'admin' and password == 'admin':
        # 设置coookie信息，保存用户名
        response = redirect("/index")
        response.set_cookie("is_login", True, 300)  # cookie有效期为300秒
        response.set_cookie("username", username)

        # 设置session信息，保存登录状态
        # request.session['islogin'] = True
        return response
    else:
        return redirect('/login')

def logout(request):
    response = redirect("/login")
    response.delete_cookie('username')
    # del request.session['username']
    return response

def index(request):
    username = request.COOKIES.get('username','')
    return render(request, '../templates/index.html', {'username':username})

def main(request):
    return render(request, '../templates/main.html', {})

def example(request):
    return render(request,'sys/example.html',{})

def user_list_page(request):
    return render(request, 'sys/user_list.html', {})

def user_add_page(request):
    return render(request,'sys/user_add.html',{})

# 判断用户是否可用
def user_account_is_exit(request):
    account = request.POST.get('account')
    user = ManagerUser.objects.filter(account=account)
    if user:
        return HttpResponse('false')
    else:
        return HttpResponse('true')

def user_add(request):
    try:
        managerUser = ManagerUser()
        user_name = request.POST.get('user_name')
        gender = request.POST.get('gender')
        account = request.POST.get('account')
        password = request.POST.get('password')
        comment = request.POST.get('comment')
        managerUser.user_name = user_name
        managerUser.gender = gender
        managerUser.account = account
        managerUser.password = password
        managerUser.comment = comment
        managerUser.save()
    except Exception:
        return JsonResponse({'code': 1})
    else:
        return JsonResponse({'code':0})

def user_edit_page(request):
    id = request.GET.get('id')
    user = ManagerUser.objects.get(id=id)
    return render(request,'sys/user_add.html',{'user':user})

def user_list(request):
    user_name = request.GET.get('user_name')
    gender = request.GET.get('gender')
    account = request.GET.get('account')
    page = request.GET.get('page')
    num = request.GET.get('rows')
    # 条件过滤查询
    right_boundary = int(page) * int(num)
    page_user = ManagerUser.objects.all()
    if user_name:
        page_user = page_user.filter(Q(user_name__contains=user_name))
    if gender:
        page_user = page_user.filter(Q(gender=gender))
    if account:
        page_user = page_user.filter(Q(account__contains=account))
    # 记录总数
    total = page_user.count()
    page_user = page_user.order_by('id')[int(num) * (int(page) - 1):right_boundary]
    rows = []
    for user in page_user:
        rows.append({'id': user.id, 'user_name': user.user_name, 'gender': user.gender,'account': user.account, 'password': user.password , 'comment':user.comment})
    return HttpResponse(json.dumps({'total': total, 'rows': rows}))

def user_delete(request):
    try:
        id = request.POST.get('id')
        user = ManagerUser.objects.filter(id=id)
        user.delete()
    except Exception:
        return JsonResponse({'code': 1})
    else:
        return JsonResponse({'code': 0})

def role_list_page(request):
    return render(request,'sys/role_list.html',{})

