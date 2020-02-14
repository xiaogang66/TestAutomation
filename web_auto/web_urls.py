from django.conf.urls import include,url
from web_auto import web_views

urlpatterns = [

    url(r'^paramListPage$', web_views.param_list_page),
    url(r'^paramList$', web_views.param_list),
    url(r'^paramAddPage$', web_views.param_add_page),
    url(r'^paramAdd$', web_views.param_add),
    url(r'^paramEditPage$', web_views.param_edit_page),
    url(r'^paramEdit$', web_views.param_edit),
    url(r'^paramDelete$', web_views.param_delete),

    url(r'^elementListPage$', web_views.element_list_page),
    url(r'^elementList$', web_views.element_list),
    url(r'^elementAddPage$', web_views.element_add_page),
    url(r'^elementAdd$', web_views.element_add),
    url(r'^elementEditPage$', web_views.element_edit_page),
    url(r'^elementEdit$', web_views.element_edit),
    url(r'^elementDelete$', web_views.element_delete),

    url(r'^caseListPage$', web_views.case_list_page),
    url(r'^caseList$', web_views.case_list),
    url(r'^caseAddPage$', web_views.case_add_page),
    url(r'^caseNoIsExist$', web_views.case_no_is_exist),
    url(r'^caseAdd$', web_views.case_add),
    url(r'^caseEditPage$', web_views.case_edit_page),
    url(r'^caseEdit$', web_views.case_edit),
    url(r'^caseCopyPage$',web_views.case_copy_page),
    url(r'^caseCopy$', web_views.case_copy),
    url(r'^caseDelete$', web_views.case_delete),
    url(r'^caseBatchDelete$', web_views.case_batch_delete),
    url(r'^caseExecute$',web_views.case_execute),

    url(r'^stepListPage$', web_views.step_list_page),
    url(r'^stepElementListPage$', web_views.step_element_list_page),
    url(r'^stepSave$', web_views.step_save),

    url(r'^suitListPage$', web_views.suit_list_page),
    url(r'^suitList$', web_views.suit_list),
    url(r'^suitAddPage$', web_views.suit_add_page),
    url(r'^suitAdd$', web_views.suit_add),
    url(r'^suitEditPage$', web_views.suit_edit_page),
    url(r'^suitEdit$', web_views.suit_edit),
    url(r'^suitDelete$', web_views.suit_delete),
    url(r'^suitCaseListPage$', web_views.suit_case_list_page),
    url(r'^suitCaseList$', web_views.suit_case_list),
    url(r'^suitCaseAddPage$', web_views.suit_case_add_page),
    url(r'^suitCaseAdd$', web_views.suit_case_add),
    url(r'^suitCaseDelete$', web_views.suit_case_delete),
    url(r'^suitExecute$', web_views.suit_execute),
    #
    url(r'^logListPage$',web_views.log_list_page),
    url(r'^logList$', web_views.log_list),
    url(r'^logDetailPage$', web_views.log_detail_page),

    url(r'^reportListPage$', web_views.report_list_page),
    url(r'^reportList$', web_views.report_list),
    url(r'^reportDetailPage$', web_views.report_detail_page),
    url(r'^reportDetail$', web_views.report_detail),

]