"""TestAutomation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include,url
from sys_manager import sys_views

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', sys_views.login),
    url(r'^login', sys_views.login),
    url(r'^logout', sys_views.logout),
    url(r'^index', sys_views.index),
    url(r'^main', sys_views.main),
    url(r'^sys/', include('sys_manager.sys_urls')),
    url(r'^interface/', include('interface_auto.interface_urls')),
    url(r'^web/', include('web_auto.web_urls')),
]
