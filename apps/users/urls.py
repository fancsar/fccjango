# -*- coding: utf-8 -*-
# @Time   :2020/5/12 13:48
# @Author :XDF_FCC
# @Email  :fanchengcheng3@xdf.cn
# @File   :urls.py

from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path("login/", obtain_jwt_token),
]
