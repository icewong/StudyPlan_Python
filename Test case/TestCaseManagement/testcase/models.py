from django.db import models

import time,os
from django.contrib.auth.models import User
import datetime

class import_log(models.Model):
    doc_file = models.FileField(upload_to='testcase/')
    relate_project_id = models.IntegerField()

    def save(self , *args, **kwargs):
        try:
            d , f= os.path.split(self.doc_file.name)
            ext = os.path.splitext(f)[1]
            fn = '%s_%s' %(kwargs['project_name'],time.strftime("%Y%m%d%H%M%S"))
            self.doc_file.name=os.path.join(d, fn + ext)
        except:
            #if doesn't give project_name ,Not change name
            pass

        super(import_log, self).save()
        return self.doc_file.path

class project(models.Model):
    name = models.CharField(max_length=64)
    update_time = models.DateTimeField(auto_now=True)

class project_path(models.Model):
    name = models.CharField(max_length=256)
    project = models.ForeignKey(project,on_delete=models.CASCADE)
    parent_id =  models.IntegerField()
    content = models.CharField(max_length=1024)
    upload_time = models.DateTimeField(auto_now=True)

class project_permission(models.Model):
    project = models.ForeignKey(project, on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    level = models.SmallIntegerField()

class AllCases(models.Model):
    case_index = models.CharField(max_length=64)
    name = models.CharField(max_length=256)
    test_type = models.CharField(max_length=64)
    pre_condition = models.CharField(null=True,max_length=2048)
    step = models.CharField(max_length=2048)
    exception = models.CharField(max_length=2048)
    path = models.ForeignKey(project_path,on_delete=models.CASCADE)
    level = models.IntegerField(default=0)

class testInstance(models.Model):
    name = models.CharField(max_length=256)
    update_time = models.DateTimeField(auto_now=True)
    project = models.ForeignKey(project,on_delete=models.CASCADE)

class instance_cases(models.Model):
    instance = models.ForeignKey(testInstance, on_delete=models.CASCADE)
    case = models.ForeignKey(AllCases, on_delete=models.CASCADE)
    result = models.SmallIntegerField(null=True)
    executor = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,)
    update_time = models.DateTimeField(auto_now=True)
    comment = models.CharField(max_length=256,null=True,)

class instance_version(models.Model):
    instance = models.ForeignKey(testInstance, on_delete=models.CASCADE)
    system =  models.CharField(max_length=32)
    version =  models.CharField(max_length=64)

class bugInfo(models.Model):
    jira_number = models.CharField(max_length=64)
    bug_status = models.IntegerField()
    occurrence_probability = models.CharField(max_length=64)
    content = models.TextField()
    system_type = models.IntegerField()
    related_project = models.ForeignKey(project,on_delete=models.CASCADE)
    create_user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name='create_user')
    create_time = models.DateTimeField(default=datetime.datetime.now,null=True)
    update_user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True,related_name='update_user')
    update_time = models.DateTimeField(auto_now=True)

class bug_instanceCases(models.Model):
    bug = models.ForeignKey(bugInfo,on_delete=models.CASCADE)
    instance_case = models.ForeignKey(instance_cases,on_delete=models.CASCADE)