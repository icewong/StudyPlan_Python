#-*- coding=utf-8 -*-

from django import template

register = template.Library()

from ..models import project_path,AllCases
@register.inclusion_tag('testcase/tree_view_template.html')
def create_tree_from_parent(node_item):
    node={}
    node['name'] = node_item.name
    node['id'] = node_item.id
    node['all_children']=project_path.objects.filter(parent_id=node_item.id)
    if len(node['all_children'])>0:
        node['end_path'] = False
    else:
        node['all_children']=AllCases.objects.filter(path_id=node_item.id)
        node['end_path'] = True

    return {'node': node}

@register.inclusion_tag('testcase/tree_view_from_map.html')
def generate_tree_from_map(cur_item,map):
    node={}
    node['name']=cur_item[1]
    if cur_item[0]=='case':
        node['id']=cur_item[2]
        node['test_case'] = True
    else:
        if cur_item[0] in map:
            node['test_case'] = False
            node['all_children']=map[cur_item[0]]
        else:
            return {}
    return {'node': node,'map':map}

from ..forms import BugInfoForm
@register.inclusion_tag('testcase/FailItemDlg.html')
def fail_dlg(result_id=None,data=None):
    context_dict={}
    if result_id:
        context_dict['dlgID']=result_id
    else:
        context_dict['dlgID']='NewFailDlg'
    if data:
        context_dict['form'] = BugInfoForm(initial={'jira_number':data.jira_number,
    'system':data.system_type,
    'status':data.bug_status,
    'occurance_probability':data.occurrence_probability,
    'description':data.content})
    else:
        context_dict['form'] = BugInfoForm()
    context_dict['title'] = 'Bug Detail'
    return context_dict

@register.inclusion_tag('testcase/sub_bugs_info_create.html')
def create_bugs_info_table(bugs_item):
    context = {'bugs': bugs_item}
    return context