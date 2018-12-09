#-*- coding=utf-8 -*-

TEXT_SPLIT_TAG = "@:@"

PERMISSION_PROJECT_PRINCIPAL = 1
PERMISSION_PROJECT_MEMBER = 2

SELECT_ITEM_NONE = 0

BUG_STATUS_OPENING = 1
BUG_STATUS_CLOSED = 2
BUG_STATUS_PENDING = 3
def translate_bug_status(number):
    if number == BUG_STATUS_OPENING:
        return "Opening"
    elif number == BUG_STATUS_CLOSED:
        return  "Closed"
    elif number == BUG_STATUS_PENDING:
        return  "Pending"
    else:
        return  "UNKNOWN"

SYSTEM_TYPE_IOS = 1
SYSTEM_TYPE_ANDROID = 2
def translate_system_type(number):
    if number == SYSTEM_TYPE_IOS:
        return "iOS"
    elif number == SYSTEM_TYPE_ANDROID:
        return  "Android"
    else:
        return  "UNKNOWN"


RESULT_SUCCESS = 0
RESULT_FAIL = 1
RESULT_NA = 2
def translate_result(number):
    if number == RESULT_SUCCESS:
        return "Success"
    elif number == RESULT_FAIL:
        return  "Fail"
    elif number == RESULT_NA:
        return  "NA"
    else:
        return  "UNKNOWN"

CASE_LEVEL_P0 = 1
CASE_LEVEL_P1 = 2
CASE_LEVEL_P2 = 3
def translate_case_level(number):
    if number == CASE_LEVEL_P0:
        return "P0"
    elif number == CASE_LEVEL_P1:
        return  "P1"
    elif number == CASE_LEVEL_P2:
        return  "P2"
    else:
        return  "UNKNOWN"