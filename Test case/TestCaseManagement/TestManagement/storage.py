# -*-coding:utf-8 -*-
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.conf import settings
import os, time, random


import base64
class FileStorage(FileSystemStorage):
    def __init__(self, location=settings.MEDIA_ROOT, base_url=settings.MEDIA_URL):
        #初始化
        super(FileStorage, self).__init__(location, base_url)

    #重写 _save方法
    def _save(self, name, content):
        d , f= os.path.split(name)
        fn , ext = os.path.splitext(f)[1]
        fn = base64.b64encode(fn)
        name = os.path.join(d, fn + ext)
        return super(FileStorage, self)._save(name, content)