# -*- coding: utf-8 -*-
# @Time   :2020/5/19 16:29
# @Author :XDF_FCC
# @Email  :fanchengcheng3@xdf.cn
# @File   :urls.py

from rest_framework import routers
from .views import EnvsList

router = routers.SimpleRouter()
router.register(r'envs', EnvsList)
urlpatterns = []
urlpatterns += router.urls
