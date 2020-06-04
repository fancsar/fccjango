# -*- coding: utf-8 -*-
# @Time   :2020/5/24 11:13
# @Author :XDF_FCC
# @Email  :fanchengcheng3@xdf.cn
# @File   :urls.py
from .views import ReportsList
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'reports', ReportsList)
urlpatterns = []
urlpatterns += router.urls
