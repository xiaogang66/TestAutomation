from django.conf.urls import include,url
from interface_auto import interface_views

urlpatterns = [

    url(r'^paramListPage$', interface_views.param_list_page),
    url(r'^paramList$', interface_views.param_list),
    url(r'^paramAddPage$', interface_views.param_add_page),
    url(r'^paramAdd$', interface_views.param_add),
    url(r'^paramEditPage$', interface_views.param_edit_page),
    url(r'^paramEdit$', interface_views.param_edit),
    url(r'^paramDelete$', interface_views.param_delete),

    url(r'^caseListPage$', interface_views.case_list_page),
    url(r'^caseList$', interface_views.case_list),
    url(r'^caseAddPage$', interface_views.case_add_page),
    url(r'^caseNoIsExist$', interface_views.case_no_is_exist),
    url(r'^caseAdd$', interface_views.case_add),
    url(r'^caseEditPage$', interface_views.case_edit_page),
    url(r'^caseEdit$', interface_views.case_edit),
    url(r'^caseCopyPage$', interface_views.case_copy_page),
    url(r'^caseDelete$', interface_views.case_delete),
    url(r'^caseBatchDelete$', interface_views.case_batch_delete),
    url(r'^caseExecute$', interface_views.case_execute),

    url(r'^suitListPage$', interface_views.suit_list_page),
    url(r'^suitList$', interface_views.suit_list),
    url(r'^suitAddPage$', interface_views.suit_add_page),
    url(r'^suitAdd$', interface_views.suit_add),
    url(r'^suitEditPage$', interface_views.suit_edit_page),
    url(r'^suitEdit$', interface_views.suit_edit),
    url(r'^suitDelete$', interface_views.suit_delete),
    url(r'^suitCaseListPage$', interface_views.suit_case_list_page),
    url(r'^suitCaseList$', interface_views.suit_case_list),
    url(r'^suitCaseAddPage$', interface_views.suit_case_add_page),
    url(r'^suitCaseAdd$', interface_views.suit_case_add),
    url(r'^suitCaseDelete$', interface_views.suit_case_delete),
    url(r'^suitExecute$', interface_views.suit_execute),

    url(r'^logListPage$',interface_views.log_list_page),
    url(r'^logList$', interface_views.log_list),
    url(r'^logDetailPage$', interface_views.log_detail_page),

    url(r'^reportListPage$', interface_views.report_list_page),
    url(r'^reportList$', interface_views.report_list),
    url(r'^reportDetailPage$', interface_views.report_detail_page),
    url(r'^reportDetail$', interface_views.report_detail),

]