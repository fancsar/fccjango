# -*- coding: utf-8 -*-
# @Time   :2020/5/21 20:35
# @Author :XDF_FCC
# @Email  :fanchengcheng3@xdf.cn
# @File   :urls.py

from rest_framework import routers
from .views import TestsuitsList

router = routers.SimpleRouter()
router.register(r'testsuits', TestsuitsList)
urlpatterns = []
urlpatterns += router.urls