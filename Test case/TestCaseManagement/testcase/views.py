from django.shortcuts import render
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse

from .MACRO import *
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from .Functions.Common import *

def Handler404(request, text=None):
    return render(request, 'testcase/404.html', {'Detail': text})

from .module.load import UpdateTestCasesFromFile

from . import permission
#from .tests import *

from .Functions import InstanceRelated

@login_required
def AllProjects(request):
    context = {}

    cur_user=User.objects.get(username=request.user.username)
    if permission.JudgeAdmin(cur_user)==1:
        context['admin'] = 1
        projectsInfo = [i for i in project.objects.all()]
        for item in projectsInfo:
            users = permission.GetProjectUser(item)
            item.principals = users[PERMISSION_PROJECT_PRINCIPAL]
            item.members = users[PERMISSION_PROJECT_MEMBER]
            item.enable_config = 1
    else:
        related_project = permission.GetRelatedProject(cur_user)
        projectsInfo = []
        for item in related_project:
            users = permission.GetProjectUser(item)
            item.principals = users[PERMISSION_PROJECT_PRINCIPAL]
            item.members = users[PERMISSION_PROJECT_MEMBER]
            if related_project[item]==PERMISSION_PROJECT_PRINCIPAL:
                item.enable_config = 1
            projectsInfo.append(item)
    context['project'] = projectsInfo


    return render(request, 'testcase/AllTestCases.html', context=context)


from .models import import_log
#from django.template.defaultfilters import slugify

@login_required
def ProjectModify(request,project_id=None):
    this_pro = None
    if project_id is not None:
        try:
            this_pro = project.objects.get(id=project_id)
        except:
            return render(request,'/testcase/404.html', {'Detail': 'Invalid Request!'})

    if request.method == 'POST':
        form = TestcaseForm(request.POST, request.FILES)

        if project_id is not None:
            this_pro.save()

        else:
            if form.is_valid():
                project_name = request.POST['project_name'].strip()
                this_pro = project(name=project_name)
                this_pro.save()
            else:
                return HttpResponse("Missing Data!")

        pro_id = this_pro.id

        if 'docfile' in request.FILES:
            new_item = import_log(relate_project_id=pro_id, doc_file=request.FILES['docfile'])
            chg_file_path = new_item.save(project_name=this_pro.name)
            UpdateTestCasesFromFile(chg_file_path, pro_id)

        if 'principals' in request.POST:
            principal_items = project_permission.objects.filter(project=this_pro,level=PERMISSION_PROJECT_PRINCIPAL)
            now_principals = set([int(item) for item in request.POST.getlist('principals')])
            for item in principal_items:
                if item.user_id in now_principals:
                    now_principals.remove(item.user_id)
                else:
                    item.delete()
            for item in now_principals:
                db_item = project_permission(project=this_pro,level=PERMISSION_PROJECT_PRINCIPAL)
                db_item.user = User.objects.get(id=item)
                db_item.save()

        if 'members' in request.POST:
            members_items = project_permission.objects.filter(project=this_pro,level=PERMISSION_PROJECT_MEMBER)
            now_members = set([int(item) for item in request.POST.getlist('members')])
            for item in members_items:
                if item.user_id in now_members:
                    now_members.remove(item.user_id)
                else:
                    item.delete()
            for item in now_members:
                db_item = project_permission(project=this_pro,level=PERMISSION_PROJECT_MEMBER)
                db_item.user = User.objects.get(id=item)
                db_item.save()

        return HttpResponseRedirect('/testcase/')
    else:
        cur_user=User.objects.get(username=request.user.username)
        form = TestcaseForm()
        content = {}
        if permission.JudgeAdmin(cur_user)==1:
            # 只有管理员拥有配置有如下权限
            #   项目负责人修改 、 项目名称修改
            content['showPrincipal']=1
            if this_pro is not None:
                content['principalUsers']=project_permission.objects.filter(project=this_pro,level=PERMISSION_PROJECT_PRINCIPAL)
            content['showName']=1
        else:
            if (project_id is None) or (not permission.ProjectPrincipalCheck(this_pro,cur_user)):
                return Handler404(request,'Oops, You do not have permission to manipulate this page!')

        if project_id is not None:
            content['projectName']=this_pro.name
            form.fields['project_name'].initial = this_pro.name
            form.fields['docfile'].required = False

        content['form'] = form
        content['AllUsers'] = User.objects.all()
        content['memberUsers'] = project_permission.objects.filter(project_id=project_id,level=PERMISSION_PROJECT_MEMBER)
        return render(request, 'testcase/ProjectModify.html',content )

@login_required
def ProjectDelete(request, project_id):
    if request.method == 'GET':
        try:
            cur_user = permission.GetCurUser(request)
            if permission.JudgeAdmin(cur_user):
                content = {'project': project.objects.get(id=project_id)}
                return render(request, 'testcase/ProjectDelete.html',content )
        except:
            return HttpResponse('unsupport')
    else:
        return HttpResponse('Unsupport')

@login_required
def ManipulateSimplePost(request):
    if request.method == 'POST':
        try:
            idf_delete_project = "project-delete"
            if idf_delete_project in request.POST:
                project_id = request.POST[idf_delete_project]
                cur_user = permission.GetCurUser(request)
                if permission.JudgeAdmin(cur_user):
                    cur_pro = project.objects.get(id=project_id)
                    cur_pro.delete()
                return HttpResponseRedirect("/testcase/Project/")

            idf_delete_instance = "instance-delete"
            if idf_delete_instance in request.POST:
                ins_id = request.POST[idf_delete_instance]
                cur_user = permission.GetCurUser(request)
                if permission.JudgeAdmin(cur_user):
                    cur_ins = testInstance.objects.get(id=ins_id)
                    cur_ins.delete()
                return HttpResponseRedirect("/testcase/Instances/")
        except:
            return HttpResponse('Update invalid.')
    else:
        return Handler404(request, 'This page doest not exist.')




'''
I cannot remember the meaning of this function.!!!


@login_required
def UpdateTestcase(request, project_slug=None):
    try:
        project_item = Testcase.objects.filter(parent_id=0).get(content=project_slug)
    except:
        return HttpResponseRedirect('/testcase/404.html', {'Detail': 'Can not find ' + project_slug})

    if request.method == 'POST':
        form = UpdateTestcaseForm(request.POST, request.FILES)
        if form.is_valid():
            project_item.save()
            new_item = import_log(relate_project_id=project_item.id, doc_file=request.FILES['docfile'])
            chg_file_path = new_item.save(project_name=project_item.name)
            UpdateTestCasesFromFile(chg_file_path, project_item.id)

            return HttpResponseRedirect('/testcase/' + project_slug)
    else:
        form = UpdateTestcaseForm()
        return render(request, 'testcase/UpdateTestCase.html',
                      {'form': form,
                       'project_name': project_item.name,
                       'project_slug': project_slug})

'''


@login_required
def ProjectDeatil(request, project_id,case_id=None):
    try:
        cur_pro = project.objects.get(id=project_id)
    except ObjectDoesNotExist:
        return Handler404(request, "This project do not exist!")

    context_dict = {'all_root_elems': project_path.objects.filter(parent_id=0,project_id=cur_pro.id)}
    return render(request, 'testcase/ProjectDetail.html', context=context_dict)


@login_required
def ProjectCaseDetail(request, project_id ,case_id):
    cur_user = permission.GetCurUser(request)
    if request.method == 'POST' and permission.ProjectManageCheck(project_id=project_id, user=cur_user):
        try:
            if case_id is not None:
                cur_pro = project.objects.get(id=project_id)
                item = AllCases.objects.get(id=case_id)
                if 'case_index' in request.POST:
                    item.case_index = request.POST['case_index']
                if 'name' in request.POST:
                    item.name = request.POST['name']
                if 'test_type' in request.POST:
                    item.test_type = request.POST['test_type']
                if 'pre_condition' in request.POST:
                    item.pre_condition = request.POST['pre_condition']
                if 'step' in request.POST:
                    item.step = request.POST['step']
                if 'expectation' in request.POST:
                    item.exception = request.POST['expectation']
                if 'level' in request.POST:
                    item.level = request.POST['level']
                item.save()
                cur_pro.save()
                return HttpResponse('success')
        except:
            pass
        response = HttpResponse("Invalid Data!")
        response.status_code=400
        return response
    else:
        try:
            if permission.ProjectMemberCheck(project_id=project_id, user=cur_user):
                testcase = AllCases.objects.get(id=case_id)
                caseForm = TestcaseItemForm()
                caseForm.loadFromDBItem(testcase)
                path = testcase.path.content + '/' + testcase.path.name + '/'
                content = {'form': caseForm, 'path': path}
                if permission.ProjectManageCheck(project_id=project_id, user=cur_user):
                    content['Manage_permission'] = True
                return render(request, 'testcase/ProjectDetail_sub.html', context = content )
        except:
            return HttpResponse('<div>Invalid Test Case!</div>')

        return HttpResponse('<div>Invalid request!</div>')

@login_required
def ProjectPathNode(request, path_id):
    try:
        cur_user = permission.GetCurUser(request)
        cur_path_node = project_path.objects.get(id=path_id)

        if request.method=='POST' and permission.ProjectManageCheck(project_id=cur_path_node.project.id, user=cur_user):
            idf_add_testcase = 'ADD_TEST_CASE'
            idf_add_node = 'ADD_PATH_NODE'
            idf_modify = 'MODIFY'
            idf_delete = 'DELETE'
            type = request.POST.get('method').strip()
            if type == idf_add_testcase:
                form = TestcaseItemForm(request.POST)
                if form.is_valid():
                    cur_case_index = request.POST['case_index'].strip()
                    if AllCases.objects.filter(path__project__id=cur_path_node.project.id,case_index=cur_case_index).count()>0:
                        return HttpResponse("<b>"+cur_case_index+"</b> already existed!",status=400)

                    new_testcase = AllCases(case_index=cur_case_index,
                                            name=request.POST['name'],
                                            test_type=request.POST['test_type'],
                                            step=request.POST['step'],
                                            exception=request.POST['expectation'],
                                            path=cur_path_node,
                                            level=request.POST['level'])
                    if 'pre_condition' in request.POST:
                        new_testcase.pre_condition=request.POST['pre_condition']
                    new_testcase.save()
                    text = '<li class="testcase" id="'+str(new_testcase.id)+'">'+new_testcase.name+'</li>'
                    return HttpResponse(text)
            elif type == idf_add_node:
                new_name = request.POST['new_node_name'].strip()
                if project_path.objects.filter(name=new_name,parent_id=cur_path_node.id).count()>0:
                    return HttpResponse("<b>"+new_name+"</b> is already added!", status=400)
                else:
                    new_node_path = project_path( name=new_name,
                                                  project=cur_path_node.project,
                                                  parent_id=cur_path_node.id,
                                                  content=cur_path_node.content+'/'+cur_path_node.name)
                    new_node_path.save()
                    text = '<li pathid="'+str(new_node_path.id)+'" class="path-node"><b>'+new_node_path.name+'</b></li>'
                    return HttpResponse(text)
            elif type == idf_modify:
                cur_path_node.name = request.POST['modify_name'].strip()
                cur_path_node.save()
                return HttpResponse(cur_path_node.name)
            elif type == idf_delete:
                cur_path_node.delete()
                return HttpResponse("Successfully delete")
        else:
            if permission.ProjectManageCheck(project_id=cur_path_node.project.id, user=cur_user):
                caseForm = TestcaseItemForm()
                content = {'form': caseForm, 'node': cur_path_node}
                if project_path.objects.filter(parent_id=cur_path_node.id).count()==0:
                    content['add_testcase'] = True
                    if AllCases.objects.filter(path_id=cur_path_node.id).count()>0:
                        content['hide_add_node'] =True
                return render(request, 'testcase/ProjectDetail_sub_path.html', context = content )
    #except:
        #return HttpResponse('Invalid request.', status=400)
    except Exception as ex:
            return HttpResponse('Add Failed: ' + str(ex), status=400)

    return HttpResponse("You don't have permission to do this.", status=400)

@login_required
def ProjectAddRootItem(request, project_id):
    try:
        cur_user = permission.GetCurUser(request)
        cur_project = project.objects.get(id=project_id)
        if request.method=='POST':
            new_name = request.POST['new_node_name'].strip()
            if project_path.objects.filter(name=new_name,parent_id=project_id).count()>0:
                return HttpResponse("<b>"+new_name+"</b> is already added!", status=400)
            else:
                new_node_path = project_path( name=new_name,
                                              project=cur_project,
                                              parent_id=0,
                                              content="")
                new_node_path.save()
                text = '<li pathid="'+str(new_node_path.id)+'" class="path-node"><b>'+new_node_path.name+'</b></li>'
                return HttpResponse(text)
        else:
            if permission.ProjectManageCheck(project_id=project_id, user=cur_user):
                return render(request, 'testcase/ProjectDetail_sub_addRoot.html', context = {})
    except:
        return HttpResponse('Invalid request.', status=400)

    return HttpResponse("You don't have permission to do this.", status=400)


@login_required
def ProjectDeleteCase(request, project_id):
    if request.method == 'POST':
        try:
            cur_user = permission.GetCurUser(request)
            if cur_user is not None:
                if permission.ProjectManageCheck(project_id,cur_user):
                    case_id = request.POST['caseID'].strip()
                    case_item = AllCases.objects.get(id=case_id)
                    path_item = case_item.path
                    case_item.delete()
                    '''
                        删除空的父节点
                    delete_path_id = ""
                    if AllCases.objects.filter(path_id=path_item.id).count()==0:
                        while path_item is not None:
                            parent_id = path_item.parent_id
                            delete_path_id = str(path_item.id)
                            path_item.delete()
                            if project_path.objects.filter(parent_id=parent_id).count()==0:
                                path_item = project_path.objects.get(id=parent_id)
                            else:
                                path_item = None
                        return HttpResponse('DeletedPath='+delete_path_id)
                    '''
                    return HttpResponse("Successfully delete.")
        except:
            return HttpResponse('Update invalid.')
    else:
        return Handler404(request, 'This page doest not exist.')



@login_required
def Instances(request):
    cur_user = permission.GetCurUser(request)

    result = testInstance.objects.all().order_by('update_time').reverse()
    for item in result:
        try:
            ins_case = instance_cases.objects.filter(instance_id=item.id).latest('update_time')
            item.latest_executor = ins_case.executor
            if ins_case.executor_id is not None:
                item.latest_execution_time = ins_case.update_time
        except ObjectDoesNotExist:
            pass
    context = {'project': result}
    if permission.JudgeAdmin(cur_user)==1:
        context['admin'] = 1

    return render(request, 'testcase/AllInstance.html', context=context)

@login_required
def InstancesModify(request, id=None):
    if request.method == 'POST':
        form = TestingProjectForm(request.POST)
        if form.is_valid():
            name = request.POST['project_name'].strip()
            test_case_project_id = request.POST['testcase_choice']
            test_case_project = project.objects.get(id=test_case_project_id)
            if id:
                try:
                    cur_instance = testInstance.objects.get(id=id)
                    if cur_instance.name != name:
                        if testInstance.objects.filter(name=name).count() == 0:
                            cur_instance.name = name
                        else:
                            return HttpResponse("Testing version name '"+name+"' is already exist. Please change another!", status=400)
                except ObjectDoesNotExist:
                    return HttpResponse("This instance does not exist.", status=400)
            else:
                cur_instance = testInstance()
                if testInstance.objects.filter(name=name).count() == 0:
                    cur_instance.name = name
                else:
                    return HttpResponse("Testing version name '"+name+"' is already exist. Please change another!", status=400)

            cur_instance.project = test_case_project
            cur_instance.save()

            vers_tag = 'versionInfo'
            if vers_tag in request.POST:
                versions={}
                for item in request.POST.getlist(vers_tag):
                    sub_list = item.split(TEXT_SPLIT_TAG)
                    if len(sub_list) == 2:
                        versions[sub_list[0].strip()]=sub_list[1].strip()
                if id is not None:
                    tmp_items = instance_version.objects.filter(instance_id=id)
                    for item in tmp_items:
                        cur_system = item.system
                        if cur_system in versions:
                            item.version = versions.pop(cur_system)
                            item.save()
                        else:
                            item.delete()
                for item in versions:
                    tmp_item=instance_version()
                    tmp_item.instance=cur_instance
                    tmp_item.system= item
                    tmp_item.version= versions[item]
                    tmp_item.save()

            cases = set([int(i) for i in request.POST['testcases'].split(',') if len(i)>0])
            if id is not None:
                old_cases = instance_cases.objects.filter(instance_id=id)
                for item in old_cases:
                    caseid = item.case_id
                    if caseid in cases:
                        cases.remove(caseid)
                    else:
                        item.delete()
            for item in cases:
                try:
                    case_item = AllCases.objects.get(id=item)
                    new_case = instance_cases(instance=cur_instance, case=case_item )
                    new_case.save()
                except:
                    pass
            return HttpResponse('Success')
    else:
        if id:
            try:
                cur_instance = testInstance.objects.get(id=id)
            except:
                return HttpResponseRedirect('/testcase/404.html',
                                            {'Detail': 'Can not find related testing version! ' + id})
            form = TestingProjectForm(project_name_default=cur_instance.name,
                                      choice_testcase_id=cur_instance.project.id)
            form.project_name = cur_instance.name
            context_dict = {
                'title': 'Modify Testing Version: ' + cur_instance.name,
                'form': form,
                'testcase': project.objects.all(),
                'selected_cases': ','.join([str(i.case_id) for i in instance_cases.objects.filter(instance_id=id)]),}
            versions = []
            for item in instance_version.objects.filter(instance_id=id):
                versions.append({'name':item.system,'version':item.version})
            context_dict['versions'] = versions
            return render(request, 'testcase/InstanceModify.html', context=context_dict)
        else:
            form = TestingProjectForm()
            context_dict = {
                'title': 'Add Testing Version',
                'form': form,
                'testcase': project.objects.all()}
            return render(request, 'testcase/InstanceModify.html', context=context_dict)


@login_required
def InstancesModify_sub(request, id):
    try:
        context_dict = {'all_root_elems': project_path.objects.filter(project_id=id,parent_id=0)}
        return render(request, 'testcase/InstanceModify_sub.html', context=context_dict)
    except ObjectDoesNotExist:
        return HttpResponse('<div>Invalid Data!</div>')

@login_required
def InstanceDelete(request, ins_id):
    if request.method == 'GET':
        try:
            cur_user = permission.GetCurUser(request)
            if permission.JudgeAdmin(cur_user):
                content = {'instance': testInstance.objects.get(id=ins_id)}
                return render(request, 'testcase/InstanceDelete.html',content )
        except:
            return HttpResponse('unsupport')
    else:
        return HttpResponse('Unsupport')

@login_required
def RunInstance(request, id):
    try:
        query = instance_cases.objects.filter(instance_id=id)
        context_dict = InstanceRelated.createCaseTree(query)
        return render(request, 'testcase/RunInstance.html', context=context_dict)
    except ObjectDoesNotExist:
        return HttpResponseRedirect('/testcase/404.html', {'Detail': 'Can not find related testing version! ' + id})


@login_required
def InstancesCaseDetail(request, ins_case_id):
    if request.method == 'POST':
        try:
            idf_result = 'testresult'
            idf_comment = 'comment'
            item = instance_cases.objects.get(id=ins_case_id)
            if idf_result in request.POST:
                test_result = int(request.POST[idf_result])
                item.result = test_result
                item.executor = User.objects.get(username=request.user.username)
            if idf_comment in request.POST:
                item.comment = request.POST[idf_comment]
            item.save()
            return HttpResponse('updated')
        except:
            pass
        return HttpResponse('unknown')
    else:
        try:
            context_dict = {}
            ins_case = instance_cases.objects.get(id=ins_case_id)
            cur_case = ins_case.case
            cur_case.level_text = translate_case_level(cur_case.level)
            context_dict['ins_case'] = ins_case
            context_dict['case_detail'] = cur_case
            bugs_info = [i.bug for i in bug_instanceCases.objects.filter(instance_case_id=ins_case.id)]
            if bugs_info:
                context_dict['bugs_info'] = bugs_info
            return render(request, 'testcase/RunInstance_sub.html', context_dict)
        except ObjectDoesNotExist:
            return HttpResponse('<div>You request invalid Data!</div>')

@login_required
def InstanceSearchCase(request, instance_id):
    if request.method == 'POST':
        try:
            #s_all = "search_all"
            s_condition = "search_condition"
            s_case_index = "search_case_index"
            s_case_name = "search_case_name"

            query = instance_cases.objects.filter(instance_id=instance_id)
            if s_condition in request.POST:
                con_list = request.POST.getlist(s_condition)
                s_pass = "search_by_pass"
                s_fail = "search_by_fail"
                s_na = "search_by_na"
                s_none = "search_by_none"
                search_list = []
                if s_pass in con_list:
                    search_list.append(RESULT_SUCCESS)
                if s_fail in con_list:
                    search_list.append(RESULT_FAIL)
                if s_na in con_list:
                    search_list.append(RESULT_NA)
                if s_none in con_list:
                    query = query.filter(Q(result=None) | Q(result__in=search_list))
                else:
                    query = query.filter(result__in=search_list)

            if s_case_index in request.POST:
                search_index = request.POST[s_case_index]
                if len(search_index)>0:
                    query = query.filter(case__case_index__icontains=search_index)

            if s_case_name in request.POST:
                search_name = request.POST[s_case_name]
                if len(search_name)>0:
                    query = query.filter(case__name__icontains=search_name)

            context_dict = InstanceRelated.createCaseTree(query)
            return render(request, 'testcase/InstanceCasesTree.html', context=context_dict)
        except:
            pass
        return HttpResponse('unknown')
    else:
        return Handler404(request,'Unsupport')



@login_required
def InstanceBugModify(request, instance_id, bug_id):
    cur_user = permission.GetCurUser(request)

    if request.method == 'POST':
        try:
            useData = BugInfoForm(request.POST)
            if useData.is_valid():
                res_item = bugInfo.objects.get(id=int(bug_id))
                modify_jira_number = request.POST['jira_number']
                if res_item.jira_number != modify_jira_number:
                    if bugInfo.objects.filter(jira_number=modify_jira_number).count()==0:
                        res_item.jira_number = request.POST['jira_number']
                    else:
                        return HttpResponse(modify_jira_number+" is already existed! You can not change "+res_item.jira_number+\
                            " to "+modify_jira_number,status=400)
                res_item.system_type = request.POST['system']
                res_item.bug_status = request.POST['status']
                res_item.occurrence_probability = request.POST['occurance_probability']
                res_item.content = request.POST['description']
                res_item.update_time = datetime.datetime.now()
                res_item.update_user = cur_user
                res_item.save()
                return HttpResponse('updated')
        except:
            pass
        return HttpResponse('<div>You request invalid Data!</div>')
    else:
        HttpResponseRedirect('/testcase/404.html', {'Detail': 'Nonsupport!'})


from django.template import loader


@login_required
def BugAdd(request, ins_case_id):
    cur_user = permission.GetCurUser(request)

    if request.method == 'POST':
        try:
            useData = BugInfoForm(request.POST)
            cur_ins_case = instance_cases.objects.get(id=ins_case_id)

            if useData.is_valid():
                jira_number = request.POST['jira_number'].strip()
                try:
                    res_item = bugInfo.objects.get(jira_number=jira_number)
                    if bug_instanceCases.objects.filter(bug_id=res_item.id,instance_case_id=ins_case_id).count()!=0:
                        return HttpResponse('You already added this bug to this test case!', status=400)
                    b_new_bug = False
                except ObjectDoesNotExist:
                    b_new_bug = True
                    res_item = bugInfo()
                    res_item.create_user = cur_user
                    res_item.related_project = cur_ins_case.instance.project
                    res_item.jira_number = jira_number

                idf_status = 'status'
                idf_probability = 'occurance_probability'
                idf_content = 'description'
                idf_system = 'system'

                miss_information = False
                if check_idf_select_in_post(idf_status,request):
                    res_item.bug_status = int(request.POST[idf_status])
                elif b_new_bug:
                    miss_information = True
                if check_idf_select_in_post(idf_system,request):
                    res_item.system_type = int(request.POST[idf_system])
                elif b_new_bug:
                    miss_information = True
                if check_idf_text_in_post(idf_probability,request):
                    res_item.occurrence_probability = request.POST[idf_probability]
                elif b_new_bug:
                    miss_information = True
                if check_idf_text_in_post(idf_content,request):
                    res_item.content = request.POST[idf_content]
                elif b_new_bug:
                    miss_information = True
                if miss_information:
                    return HttpResponse('You are add a new bug, please input all related information!', status=400)

                res_item.update_time = datetime.datetime.now()
                res_item.update_user = cur_user
                res_item.save()

                relationship = bug_instanceCases()
                relationship.bug = res_item
                relationship.instance_case = cur_ins_case
                relationship.save()

                tpl = loader.get_template('testcase/FailItemDlg.html')
                context = {'dlgID': res_item.id,
                           'title': 'Bug Detail',
                           'form': BugInfoForm(initial={
                               'jira_number': res_item.jira_number,
                               'system':res_item.system_type,
                               'status': res_item.bug_status,
                               'occurance_probability': res_item.occurrence_probability,
                               'description': res_item.content})
                           }
                return HttpResponse(tpl.render(context, request), status=200)
        except Exception as ex:
            return HttpResponse('Add Failed: ' + str(ex), status=400)
    else:
        return HttpResponseRedirect('/testcase/404.html', {'Detail': 'Nonsupport!'}, status=400)

@login_required
def InstanceBugDelete(request, ins_case_id):
    if request.method == 'POST':
        try:
            text = request.POST['deleteBug']
            bug_id = text.strip('fail_dlg_')
            bug_rel = bug_instanceCases.objects.get(bug_id=bug_id,instance_case_id=ins_case_id)
            bug_rel.delete()
            if bug_instanceCases.objects.filter(bug_id=bug_id).count()==0:
                bugInfo.objects.get(id=bug_id).delete()
            return HttpResponse("Success.", status=200)
        except ObjectDoesNotExist:
            return HttpResponse("NotExist", status=200)
        except Exception as ex:
            return HttpResponse('Delete Failed: ' + str(ex), status=400)
    else:
        return HttpResponseRedirect('/testcase/404.html', {'Detail': 'Nonsupport!'}, status=400)



@login_required
def InstancesExport(request, id):
    try:
        context_dict = {}
        Instance = testInstance.objects.get(id=int(id))
        # Version information
        query_version = instance_version.objects.filter(instance_id=id)
        versions = []
        for item in query_version:
            versions.append({'name':item.system,'version':item.version})
        context_dict['versions'] = versions

        # Instance
        context_dict['instance'] = Instance
        query_instance_cases = instance_cases.objects.filter(instance_id=id)
        cases_res = [i.result for i in query_instance_cases]
        context_dict['caseResTotal'] = len(cases_res)
        context_dict['caseResSuccess'] = cases_res.count(RESULT_SUCCESS)
        context_dict['caseResFail'] = cases_res.count(RESULT_FAIL)
        context_dict['caseResNg'] = cases_res.count(RESULT_NA)
        context_dict['caseResUnexectuted'] = cases_res.count(None)

        # bug
        query_bug_relationship = bug_instanceCases.objects.filter(instance_case__in=query_instance_cases)
        bugs={}
        for item in query_bug_relationship:
            if item.bug in bugs:
                bugs[item.bug].append(item.instance_case)
            else:
                bugs[item.bug]=[item.instance_case]
        bugs_res = [i.bug_status for i in bugs]
        context_dict['bugTotal'] = len(bugs_res)
        context_dict['bugOpening'] = bugs_res.count(BUG_STATUS_OPENING)
        context_dict['bugClosed'] = bugs_res.count(BUG_STATUS_CLOSED)
        context_dict['bugPending'] = bugs_res.count(BUG_STATUS_PENDING)

        # FailedCases
        query_fail_ins_case = [i for i in query_instance_cases if i.result == RESULT_FAIL]
        failed_items=[]
        for item in query_fail_ins_case:
            tmp_item = item.case
            tmp_item.bugs = [i.bug for i in bug_instanceCases.objects.filter(instance_case_id=item.id)]
            tmp_item.comment = item.comment
            tmp_item.level_text = translate_case_level(tmp_item.level)
            failed_items.append(tmp_item)
        context_dict['FailedCases'] = failed_items

        #NACases
        query_na_ins_case = [i for i in query_instance_cases if i.result == RESULT_NA]
        na_items=[]
        for item in query_na_ins_case:
            tmp_item = item.case
            tmp_item.bugs = [i.bug for i in bug_instanceCases.objects.filter(instance_case_id=item.id)]
            tmp_item.comment = item.comment
            tmp_item.level_text = translate_case_level(tmp_item.level)
            na_items.append(tmp_item)
        context_dict['NACases'] = na_items

        # BugDetail
        context_dict['AllBugs'] = set([i.bug for i in query_bug_relationship])
        for item in bugs:
            item.bug_status_text = translate_bug_status(item.bug_status)
        return render(request, 'testcase/InstanceExport.html', context_dict)

    except ObjectDoesNotExist:
        return HttpResponseRedirect('/testcase/404.html', {'Detail': 'Can not find related testing version! ' + id})

from .module import load
from django.utils.encoding import smart_str
@login_required
def InstancesTestcaseExport(request, id):
    try:
        cur_ins = testInstance.objects.get(id=id)
        export_data = load.ExportTestcase(id)
        response = HttpResponse(content_type='application/force-download') # mimetype is replaced by content_type for django 1.7
        response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(cur_ins.name+"_test_cases.xlsx")
        response.write(export_data)
        return response
    except:
        return Handler404(request,"Instances does not exist!")


@login_required
def Bugs(request):
    cur_user = permission.GetCurUser(request)

    all_bugs = bugInfo.objects.all()
    bugs_permission = {}
    for item in all_bugs:
        pro_id = item.related_project_id
        if pro_id not in bugs_permission:
            bugs_permission[pro_id]=permission.ProjectManageCheck(pro_id,cur_user)
        item.enable_delete = bugs_permission[pro_id]

    content = {'bugs':all_bugs}

    return render(request,'testcase/AllBugs.html', context=content)

@login_required
def BugModify(request, bug_id):
    cur_user = permission.GetCurUser(request)
    if request.method == 'POST':
        try:
            useData = BugInfoForm(request.POST)
            if useData.is_valid():
                res_item = bugInfo.objects.get(id=int(bug_id))
                if permission.ProjectMemberCheck(res_item.related_project_id,cur_user):
                    modify_jira_number = request.POST['jira_number']
                    if res_item.jira_number != modify_jira_number:
                        if bugInfo.objects.filter(jira_number=modify_jira_number).count()==0:
                            res_item.jira_number = request.POST['jira_number']
                        else:
                            return HttpResponse(modify_jira_number+" is already existed! You can not change "+res_item.jira_number+\
                                " to "+modify_jira_number,status=400)
                    res_item.system_type = request.POST['system']
                    res_item.bug_status = request.POST['status']
                    res_item.occurrence_probability = request.POST['occurance_probability']
                    res_item.content = request.POST['description']
                    res_item.update_time = datetime.datetime.now()
                    res_item.update_user = cur_user
                    res_item.save()
                    return HttpResponse('updated')
                else:
                    return HttpResponse('You do not have permission.',status=400)
        except:
            pass
        return HttpResponse('<div>You request invalid Data!</div>')
    else:
        HttpResponseRedirect('/testcase/404.html', {'Detail': 'Not support!'})


@login_required
def BugDelete(request):
    cur_user = permission.GetCurUser(request)
    if request.method == 'POST':
        try:
            bug_id = request.POST['deleteBug']
            cur_bug = bugInfo.objects.get(id=bug_id)
            if permission.ProjectManageCheck(cur_bug.related_project_id,cur_user):
                cur_bug.delete()
            else:
                return HttpResponse('You do not have permission.',status=400)
            return HttpResponse("Success.", status=200)
        except ObjectDoesNotExist:
            return HttpResponse("Not Existed", status=200)
        except Exception as ex:
            return HttpResponse('Delete Failed: ' + str(ex), status=400)
    else:
        return HttpResponseRedirect('/testcase/404.html', {'Detail': 'Nonsupport!'}, status=400)

@login_required
def BugSearch(request):
    cur_user = permission.GetCurUser(request)
    if request.method == 'POST':
        try:
            s_system = "search_by_system"
            s_status = "search_by_status"
            s_no = "search_jira_no"
            s_dis = "search_discription"

            query = bugInfo.objects.all()

            if s_system in request.POST:
                con_list = request.POST.getlist(s_system)
                s_ios = "search_by_ios"
                s_and = "search_by_android"
                search_list = []
                if s_ios in con_list:
                    search_list.append(SYSTEM_TYPE_IOS)
                if s_and in con_list:
                    search_list.append(SYSTEM_TYPE_ANDROID)
                query = query.filter(system_type__in=search_list)

            if s_status in request.POST:
                con_list = request.POST.getlist(s_status)
                s_open = "search_by_open"
                s_close = "search_by_close"
                s_pend = "search_by_pend"
                search_list = []
                if s_open in con_list:
                    search_list.append(BUG_STATUS_OPENING)
                if s_close in con_list:
                    search_list.append(BUG_STATUS_CLOSED)
                if s_pend in con_list:
                    search_list.append(BUG_STATUS_PENDING)
                query = query.filter(bug_status__in=search_list)

            if s_no in request.POST:
                search_no = request.POST[s_no]
                if len(search_no)>0:
                    query = query.filter(jira_number__icontains=search_no)

            if s_dis in request.POST:
                search_dis = request.POST[s_dis]
                if len(search_dis)>0:
                    query = query.filter(content__icontains=search_dis)

            context = {}
            if query.count()>0:
                bugs_permission = {}
                for item in query:
                    pro_id = item.related_project_id
                    if pro_id not in bugs_permission:
                        bugs_permission[pro_id]=permission.ProjectManageCheck(pro_id,cur_user)
                    item.enable_delete = bugs_permission[pro_id]
                context['bugs'] = query
            return render(request, 'testcase/sub_bugs_info_create.html', context=context)
        except:
            pass
        return HttpResponse('unknown')
    else:
        return Handler404(request,'Unsupport')




@login_required
def register(request):


    # A boolean value for telling the template
    # whether the registration was successful.
    # Set to False initially. Code changes value to
    # True when registration succeeds.
    registered = False
    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        # If the two forms are valid...
        if user_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()
            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()
            registered = True
        else:
            # Invalid form or forms - mistakes or something else?
            # Print problems to the terminal.
            print(user_form.errors)

    else:
        # Not a HTTP POST, so we render our form using two ModelForm instances.
        # These forms will be blank, ready for user input.
        user_form = UserForm()

    # Render the template depending on the context.
    return render(request, 'testcase/Register.html',
                  {'user_form': user_form, 'registered': registered})
