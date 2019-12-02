from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.shortcuts import render,redirect
from sys_manager.models import ManagerUser

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

def example(request):
    return render(request,'sys/example.html',{})

def user_list_page(request):
    return render(request,'sys/user_list.html',{})

def user_add_page(request):
    return render(request,'sys/user_add.html',{})

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
        return JsonResponse({'res': 1})
    else:
        return JsonResponse({'res':0})

def user_edit_page(request):
    return render(request,'sys/user_edit.html',{})

def query_user(request):
    return_data = {'total': 30, 'rows':[{'id':11, 'name':'张三','sal':'1000','sex':'男'},{'id':11, 'name':'张三','sal':'1000','sex':'男'},{'id':11, 'name':'张三','sal':'1000','sex':'男'},{'id':11, 'name':'张三','sal':'1000','sex':'男'},{'id':11, 'name':'张三','sal':'1000','sex':'男'},{'id':11, 'name':'张三','sal':'1000','sex':'男'}]}
    return JsonResponse(return_data)
