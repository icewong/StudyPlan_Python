#-*- coding=utf-8 -*-

def check_idf_text_in_post(idf,request):
    if idf in request.POST:
        if len(request.POST[idf])>0:
            return True
    return False

from ..MACRO import SELECT_ITEM_NONE
def check_idf_select_in_post(idf,request):
    if idf in request.POST:
        if len(request.POST[idf])>0 and int(request.POST[idf])!=SELECT_ITEM_NONE:
            return True
    return False