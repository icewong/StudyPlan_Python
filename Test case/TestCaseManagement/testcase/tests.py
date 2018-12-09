from django.test import TestCase

# Create your tests here.

from .models import *
from .Functions import InstanceRelated
from .MACRO import *

def findNext(this_items,project,parent_id):
    for item in this_items:
        new_path=project_path(name=item.name,
                            project=project,
                            parent_id=parent_id,
                            content=item.content)
        new_path.save()
        for ss in AllCases.objects.filter(parent_id=item.id):
            ss.path=new_path
            ss.save()

        next_items=Testcase.objects.filter(parent_id=item.id)
        if next_items.count()>0:
            findNext(next_items,project,new_path.id)


def changeTestcaseDatebase():

    for x_item in Testcase.objects.all():
        if x_item.parent_id==0:
            new_project=project(name=x_item.name)
            new_project.save()

            for tmp_item in testInstance.objects.filter(relate_case_project_id=x_item.id):
                tmp_item.project=new_project
                tmp_item.save()

            this_items=Testcase.objects.filter(parent_id=x_item.id)
            findNext(this_items,new_project,0)

