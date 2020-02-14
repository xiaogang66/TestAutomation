from django.conf.urls import include,url
from sys_manager import sys_views

urlpatterns = [
    url(r'^login_check$', sys_views.login_check),
    url(r'^logout$', sys_views.logout),
    url(r'^index$', sys_views.index),
    url(r'^example$', sys_views.example),

    url(r'^userListPage$', sys_views.user_list_page),
    url(r'^userList$', sys_views.user_list),
    url(r'^userAddPage$', sys_views.user_add_page),
    url(r'^userAccountIsExist$', sys_views.user_account_is_exist),
    url(r'^userAdd$', sys_views.user_add),
    url(r'^userEditPage$', sys_views.user_edit_page),
    url(r'^userEdit$', sys_views.user_edit),
    url(r'^userDelete$', sys_views.user_delete),
    url(r'^userBatchDelete$', sys_views.user_batch_delete),

    url(r'^moduleListPage$', sys_views.module_list_page),
    url(r'^moduleTree$', sys_views.module_tree),
    url(r'^getModuleById$', sys_views.get_module_by_id),
    url(r'^moduleNumberIsExist$', sys_views.module_number_is_exist),
    url(r'^moduleAddPage$', sys_views.module_add_page),
    url(r'^moduleAdd$', sys_views.module_add),
    url(r'^moduleEditPage$', sys_views.module_edit_page),
    url(r'^moduleEdit$', sys_views.module_edit),
    url(r'^moduleDelete$', sys_views.module_delete),

    url(r'^sysParamListPage$', sys_views.sysParam_list_page),
    url(r'^sysParamList$', sys_views.sysParam_list),
    url(r'^sysParamAddPage$', sys_views.sysParam_add_page),
    url(r'^sysParamAdd$', sys_views.sysParam_add),
    url(r'^sysParamEditPage$', sys_views.sysParam_edit_page),
    url(r'^sysParamEdit$', sys_views.sysParam_edit),
    url(r'^sysParamDelete$', sys_views.sysParam_delete),

    url(r'^logListPage$', sys_views.log_list_page),
    url(r'^logList$', sys_views.log_list),
    url(r'^logDetailPage$', sys_views.log_detail_page),

    url(r'^taskListPage$',sys_views.task_list_page),
    url(r'^taskList$', sys_views.task_list),
    url(r'^taskSuitList$',sys_views.task_suit_list),
    url(r'^taskAddPage$', sys_views.task_add_page),
    url(r'^taskAdd$', sys_views.task_add),
    url(r'^taskEditPage$', sys_views.task_edit_page),
    url(r'^taskEdit$', sys_views.task_edit),
    url(r'^taskDelete$', sys_views.task_delete),
]