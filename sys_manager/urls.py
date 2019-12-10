from django.conf.urls import include,url
from sys_manager import views

urlpatterns = [
    url(r'^login_check$', views.login_check),
    url(r'^logout$', views.logout),
    url(r'^index$', views.index),
    url(r'^example$', views.example),
    url(r'^userListPage$', views.user_list_page),
    url(r'^userList$', views.user_list),
    url(r'^userAddPage$', views.user_add_page),
    url(r'^userAccountIsExit$', views.user_account_is_exit),
    url(r'^userAdd$', views.user_add),
    url(r'^userEditPage$', views.user_edit_page),
    url(r'^userEdit$', views.user_edit),
    url(r'^userDelete$', views.user_delete),
    url(r'^userBatchDelete$', views.user_batch_delete),
    url(r'^roleListPage$', views.role_list_page),
]