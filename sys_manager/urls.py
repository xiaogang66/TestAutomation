from django.conf.urls import include,url
from sys_manager import views

urlpatterns = [
    url(r'^login_check$', views.login_check),
    url(r'^logout$', views.logout),
    url(r'^index$', views.index),
    url(r'^example$', views.example),
    url(r'^userListPage$', views.user_list_page),
    url(r'^queryUser$', views.query_user),
    url(r'^userAddPage$', views.user_add_page),
    url(r'^userAdd$', views.user_add),
    url(r'^userEditPage$', views.user_edit_page),
]