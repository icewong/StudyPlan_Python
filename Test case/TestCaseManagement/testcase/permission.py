#-*- coding=utf-8 -*-
from .MACRO import *
from django.core.exceptions import ObjectDoesNotExist

def GetCurUser(request):
    try:
        cur_user = User.objects.get(username=request.user.username)
        return cur_user
    except ObjectDoesNotExist:
        return None


def JudgeAdmin(cur_user):
    if cur_user is None:
        return False
    return cur_user.is_superuser

from .models import *

def ProjectPrincipalCheck(project,user):
    try:
        project_permission.objects.get(project=project,user_id=user,level=PERMISSION_PROJECT_PRINCIPAL)
    except  ObjectDoesNotExist:
        return False
    return True

#Principal & Admin
def ProjectManageCheck(project_id,user):
    try:
        if JudgeAdmin(user):
            return True
        project_permission.objects.get(project_id=project_id,user_id=user,level=PERMISSION_PROJECT_PRINCIPAL)
    except  ObjectDoesNotExist:
        return False
    return True

def ProjectMemberCheck(project_id,user):
    try:
        if JudgeAdmin(user):
            return True
        project_permission.objects.get(project_id=project_id,user_id=user,level__in=[PERMISSION_PROJECT_PRINCIPAL,PERMISSION_PROJECT_MEMBER])
    except  ObjectDoesNotExist:
        return False
    return True


def GetRelatedProject(user):
    result={}
    try:
        queryRes = project_permission.objects.filter(user=user)
        for item in queryRes:
            result[item.project] = item.level
    except  ObjectDoesNotExist:
        pass
    return result

def GetProjectUser(project):
    result={PERMISSION_PROJECT_PRINCIPAL:[],
            PERMISSION_PROJECT_MEMBER:[]}
    try:
        queryRes = project_permission.objects.filter(project=project)
        for item in queryRes:
            if item.level==PERMISSION_PROJECT_PRINCIPAL:
                result[PERMISSION_PROJECT_PRINCIPAL].append(item.user)
            elif item.level==PERMISSION_PROJECT_MEMBER:
                result[PERMISSION_PROJECT_MEMBER].append(item.user)
    except  ObjectDoesNotExist:
        pass
    return result