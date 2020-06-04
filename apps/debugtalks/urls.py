# -*- coding: utf-8 -*-
# @Time   :2020/5/20 20:20
# @Author :XDF_FCC
# @Email  :fanchengcheng3@xdf.cn
# @File   :urls.py

from rest_framework import routers
from .views import DebugTalksList

router = routers.SimpleRouter()
router.register(r'debugtalks', DebugTalksList)
urlpatterns = []
urlpatterns += router.urls
