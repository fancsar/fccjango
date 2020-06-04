# -*- coding: utf-8 -*-
# @Time   :2020/6/3 16:15
# @Author :XDF_FCC
# @Email  :fanchengcheng3@xdf.cn
# @File   :urls.py
from rest_framework import routers
from .views import ConfiguresList

router = routers.SimpleRouter()
router.register(r'configures', ConfiguresList)
urlpatterns = []
urlpatterns += router.urls