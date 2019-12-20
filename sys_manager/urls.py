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

    url(r'^moduleListPage$', views.module_list_page),
    url(r'^moduleTree$', views.module_tree),
    url(r'^listWithPage$', views.list_with_page),
    url(r'^moduleNumberIsExit$',views.module_number_is_exit),
    url(r'^moduleList$', views.module_list),
    url(r'^moduleAddPage$', views.module_add_page),
    url(r'^moduleAdd$', views.module_add),
    url(r'^moduleEditPage$', views.module_edit_page),
    url(r'^moduleEdit$', views.module_edit),
    url(r'^moduleDelete$', views.module_delete),
    url(r'^moduleBatchDelete$', views.module_batch_delete),

    url(r'^sysParamListPage$', views.sysParam_list_page),
    url(r'^sysParamList$', views.sysParam_list),
    url(r'^sysParamAddPage$', views.sysParam_add_page),
    url(r'^sysParamAdd$', views.sysParam_add),
    url(r'^sysParamEditPage$', views.sysParam_edit_page),
    url(r'^sysParamEdit$', views.sysParam_edit),
    url(r'^sysParamDelete$', views.sysParam_delete),

    url(r'^counter$', views.counter_page),
]