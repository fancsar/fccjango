# -*- coding: utf-8 -*-
# @Time   :2019/12/12 17:29
# @Author :XDF_FCC
# @Email  :fanchengcheng3@xdf.cn
# @File   :urls.py
from django.urls import path
from .views import haha
from .views import IndexView, ProjectList

urlpatterns = [
    path('projects/', ProjectList.as_view()),
    path('project/<int:pk>/', IndexView.as_view())
]
