# -*- coding: utf-8 -*-

from django import forms
from .MACRO import *
from .models import project

class styleCharField(forms.CharField):
    def __init__(self,**kwargs):
        super(styleCharField,self).__init__(widget=forms.TextInput(attrs={'class':'form-control'}),**kwargs)
class styleMulitipleCharField(forms.CharField):
    def __init__(self,**kwargs):
        super(styleMulitipleCharField,self).__init__(widget=forms.Textarea(attrs={'class':'form-control',
                                                                                  'rows':'5'}),**kwargs)
class styleChoiceFiled(forms.ChoiceField):
    def __init__(self,**kwargs):
        super(styleChoiceFiled,self).__init__(widget=forms.Select({'class':'form-control'}),**kwargs)

# Authentication
from django.contrib.auth.models import User
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class TestcaseForm(forms.Form):
    docfile = forms.FileField(label='Select a test case file (.xlsx) :')
    project_name = styleCharField(label='New project name :')

class TestcaseItemForm(forms.Form):

    LEVEL_CHOICES = (
        (SELECT_ITEM_NONE,'---------------------------------'),
        (CASE_LEVEL_P0, translate_case_level(CASE_LEVEL_P0)),
        (CASE_LEVEL_P1, translate_case_level(CASE_LEVEL_P1)),
        (CASE_LEVEL_P2, translate_case_level(CASE_LEVEL_P2)),
    )

    case_index = styleCharField()
    name = styleCharField()
    test_type = styleCharField()
    pre_condition = styleMulitipleCharField(required=False)
    step = styleMulitipleCharField()
    expectation = styleMulitipleCharField()
    level = styleChoiceFiled(label='System:', choices=LEVEL_CHOICES)


    def loadFromDBItem(self,item):
        self.fields['case_index'].initial = item.case_index
        self.fields['name'].initial = item.name
        self.fields['test_type'].initial = item.test_type
        self.fields['pre_condition'].initial = item.pre_condition
        self.fields['step'].initial = item.step
        self.fields['expectation'].initial = item.exception
        self.fields['level'].initial = item.level



class UpdateTestcaseForm(forms.Form):
    docfile = forms.FileField(label='Select a test case file (.xlsx) :')


from django.forms import ModelChoiceField
class TestCaseChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name

class TestingProjectForm(forms.Form):
    project_name = styleCharField(label='New testing version name :')
    #testcase_choice = TestCaseChoiceField(label='Please select relate TestCase project :',queryset=None,to_field_name="content")
    testcase_choice = TestCaseChoiceField(widget=forms.Select(attrs={'class':'form-control'}),
            label='Please select relate TestCase project :',queryset=None,to_field_name="id")

    def __init__(self, *args, **kwargs):
        testcase_choice_default,project_name_default=None,None
        if 'choice_testcase_id' in kwargs:
            testcase_choice_default=kwargs.pop('choice_testcase_id')
        if 'project_name_default' in kwargs:
            project_name_default=kwargs.pop('project_name_default')

        super(TestingProjectForm, self).__init__(*args, **kwargs)
        self.fields['testcase_choice'].queryset = project.objects.all()
        if testcase_choice_default:
            self.fields['testcase_choice'].initial = testcase_choice_default
        if project_name_default:
            self.fields['project_name'].initial = project_name_default

class BugInfoForm(forms.Form):
    STATUE_CHOICES = (
        (SELECT_ITEM_NONE,'---------------------------------'),
        (BUG_STATUS_OPENING, translate_bug_status(BUG_STATUS_OPENING)),
        (BUG_STATUS_CLOSED, translate_bug_status(BUG_STATUS_CLOSED)),
        (BUG_STATUS_PENDING, translate_bug_status(BUG_STATUS_PENDING)),
    )
    SYSTEM_CHOICES = (
        (SELECT_ITEM_NONE,'---------------------------------'),
        (SYSTEM_TYPE_IOS, translate_system_type(SYSTEM_TYPE_IOS)),
        (SYSTEM_TYPE_ANDROID, translate_system_type(SYSTEM_TYPE_ANDROID)),
    )

    jira_number = styleCharField(label='JIRA Number:')
    system = styleChoiceFiled(label='System:', choices=SYSTEM_CHOICES,required=False)
    status = styleChoiceFiled(label='Bug Status:', choices=STATUE_CHOICES,required=False)
    occurance_probability = styleCharField(label='Occurance Probability:',required=False)
    description = styleMulitipleCharField(label='Description:',required=False)

