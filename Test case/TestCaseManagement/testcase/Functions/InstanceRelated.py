#-*- coding=utf-8 -*-
from ..models import project_path,AllCases

def createCaseTree(query):

    if query is None:
        return {}

    tree_map={}
    result_group_str=''
    for item in query:
        try:
            testcase = item.case
            path_item = testcase.path

            cur_case_item = ('case',testcase.name,item.id)

            if path_item.id not in tree_map:
                tree_map[path_item.id]=[cur_case_item]
            else:
                tree_map[path_item.id].append(cur_case_item)


            while True:
                if path_item.parent_id in tree_map:
                    if path_item.id not in [i[0] for i in tree_map[path_item.parent_id]]:
                        tree_map[path_item.parent_id].append((path_item.id,path_item.name))
                else:
                    tree_map[path_item.parent_id]=[(path_item.id,path_item.name)]

                if path_item.parent_id == 0:
                    break
                path_item=project_path.objects.get(id=path_item.parent_id)
        except:
            pass #Omit invalid data
        if item.result is not None:
            result_group_str += str(item.id)+','+str(item.result)+';'

    context_dict={}
    if len(tree_map)>0:
        context_dict['root_items']= tree_map[0]
        context_dict['map']= tree_map
        context_dict['testedItems'] = result_group_str

    return context_dict

def loadInstanceCases(itemStr,resStr):
    items = itemStr.split(',')
    if len(resStr)==0:
        executed_res={}
    else:
        executed_res ={ i.split(',')[0]:i.split(",")[1] for i in resStr.split(';') }
    res_cases = []


    for item in items:
        try:
            item_info = AllCases.objects.get(id=int(item))
            if item in executed_res:
                item_res = executed_res[item]
                if item_res=='1':
                    res_cases.append((item,item_info,item_res,))
                    continue
            else:
                item_res=-1
            res_cases.append((item,item_info,item_res))
        except:
            pass #Omit invalid data

    return res_cases