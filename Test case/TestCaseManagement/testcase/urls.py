#-*- coding=utf-8 -*-
from django.conf.urls import url

from . import views

from django.contrib.auth.decorators import login_required

urlpatterns = [
    #url(r'^register/$',views.register, name='register'),

    url(r'^Instances/$', views.Instances),
    url(r'^Instances/add/$', views.InstancesModify,name='AddInstance'),
    url(r'^Instances/add/(?P<id>[\d\-]+)/$', views.InstancesModify_sub),
    url(r'^Instances/delete/(?P<ins_id>[\d\-]+)/$', views.InstanceDelete),
    url(r'^Instances/case/(?P<ins_case_id>[\d\-]+)/$', views.InstancesCaseDetail),
    url(r'^Instances/new-bug/(?P<ins_case_id>[\d\-]+)/$', views.BugAdd),
    url(r'^Instances/del-bug/(?P<ins_case_id>[\d\-]+)/$', views.InstanceBugDelete),
    url(r'^Instances/(?P<instance_id>[\d\-]+)/bug/(?P<bug_id>[\d\-]+)$', views.InstanceBugModify),
    url(r'^Instances/(?P<id>[\d\-]+)/config$', views.InstancesModify),
    url(r'^Instances/(?P<instance_id>[\d\-]+)/search/$', views.InstanceSearchCase),
    url(r'^Instances/(?P<id>[\d\-]+)/export-result$', views.InstancesExport),
    url(r'^Instances/(?P<id>[\d\-]+)/export-testcase$', views.InstancesTestcaseExport),
    url(r'^Instances/(?P<id>[\d\-]+)/$', views.RunInstance),

    url(r'^Project/(?P<project_id>[\d\-]+)/config$', views.ProjectModify),
    url(r'^Project/(?P<project_id>[\d\-]+)/delete', views.ProjectDelete),
    url(r'^Project/(?P<project_id>[\d\-]+)/$',views.ProjectDeatil),
    url(r'^Project/(?P<project_id>[\d\-]+)/del-case/$',views.ProjectDeleteCase),
    url(r'^Project/(?P<project_id>[\d\-]+)/case/(?P<case_id>.+)/$',views.ProjectCaseDetail),
    url(r'^Project/path-node/(?P<path_id>.+)/$',views.ProjectPathNode),
    url(r'^Project/(?P<project_id>[\d\-]+)/add-root/$',views.ProjectAddRootItem),
    url(r'^ImportTestCase/$',views.ProjectModify),
    url(r'^CaseDetail/(?P<case_id>.+)/$', views.ProjectCaseDetail),
    url(r'^Project/$',views.AllProjects),

    url(r'^Bugs/$',views.Bugs),
    url(r'^Bugs/delete/$',views.BugDelete),
    url(r'^Bugs/(?P<bug_id>[\d\-]+)/$', views.BugModify),
    url(r'^Bugs/search/$', views.BugSearch),

    url(r'^manipulate/$',views.ManipulateSimplePost),

    #Old
    url(r'^$', views.Instances, name='index'),
    #Maybe useless I forgotten
    # url(r'^ImportTestCase/(?P<project_id>[\w\-] +)/$',views.UpdateTestcase,name='UpdateTestCase'),
    #url(r'^Project/(?P<project_id>[\w\-]+)/(?P<case_id>[\d]+)$',views.ProjectDeatil),
]
