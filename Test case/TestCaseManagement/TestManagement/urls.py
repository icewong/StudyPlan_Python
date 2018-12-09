"""TestManagement URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))

"""
from django.conf.urls import url, include
from django.contrib import admin

from .views import *
from testcase import views as tcView
urlpatterns = [
    url(r'^$', tcView.Instances, name='index'),
    #url(r'^polls/',include('polls.urls')),
    url(r'^testcase/', include('testcase.urls') ),
    url(r'^admin/', admin.site.urls),
    url(r'^usersetting/$', user_setting, name='usersetting'),
    url(r'^accounts/login/$', user_login,name="login"),
    url(r'^loginWithNewPwd/$',user_login_newpwd),
    url(r'^logout/$', user_logout, name='logout'),
]
