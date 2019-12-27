from django.conf.urls import include,url
from interface_auto import views

urlpatterns = [

    url(r'^paramListPage$', views.param_list_page),
    url(r'^paramList$', views.param_list),
    url(r'^paramAddPage$', views.param_add_page),
    url(r'^paramAdd$', views.param_add),
    url(r'^paramEditPage$', views.param_edit_page),
    url(r'^paramEdit$', views.param_edit),
    url(r'^paramDelete$', views.param_delete),

    url(r'^caseListPage$', views.case_list_page),
    url(r'^caseList$',views.case_list),
    url(r'^caseAddPage$', views.case_add_page),
    url(r'^caseNoIsExist$',views.case_no_is_exist),
    url(r'^caseAdd$', views.case_add),
    url(r'^caseEditPage$', views.case_edit_page),
    url(r'^caseEdit$', views.case_edit),
    url(r'^caseDelete$',views.case_delete),
    url(r'^caseBatchDelete$',views.case_batch_delete),
    url(r'^caseExecute$',views.case_execute),

    url(r'^suitListPage$', views.suit_list_page),
    url(r'^suitList$', views.suit_list),
    url(r'^suitAddPage$', views.suit_add_page),
    url(r'^suitAdd$', views.suit_add),
    url(r'^suitEditPage$', views.suit_edit_page),
    url(r'^suitEdit$', views.suit_edit),
    url(r'^suitDelete$', views.suit_delete),
    url(r'^suitCaseListPage$',views.suit_case_list_page),
    url(r'^suitCaseList$',views.suit_case_list),
    url(r'^suitCaseAddPage$',views.suit_case_add_page),
    url(r'^suitCaseAdd$', views.suit_case_add),
    url(r'^suitCaseDelete$', views.suit_case_delete),
]