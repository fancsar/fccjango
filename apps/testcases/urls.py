# -*- coding: utf-8 -*-
# @Time   :2020/5/25 19:29
# @Author :XDF_FCC
# @Email  :fanchengcheng3@xdf.cn
# @File   :urls.py

from rest_framework import routers
from .views import TestcasesList

router = routers.SimpleRouter()
router.register(r'testcases', TestcasesList)
urlpatterns = []
urlpatterns += router.urls
