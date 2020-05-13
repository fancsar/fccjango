# -*- coding: utf-8 -*-
# @Time   :2019/12/12 17:29
# @Author :XDF_FCC
# @Email  :fanchengcheng3@xdf.cn
# @File   :urls.py
from django.urls import path
from .views import haha
from .views import ProjectList
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'project', ProjectList)
urlpatterns = []
urlpatterns += router.urls
# urlpatterns = [
#     path('projects/', ProjectList.as_view({
#         "get": "list",
#         "post": "create"
#     })),
#     path('projects/names/', ProjectList.as_view({
#         "get": "names"
#     })),
#     path('projects/names/<int:pk>/', ProjectList.as_view({
#         "get": "interface"
#     })),
#     path('projects/<int:pk>/', ProjectList.as_view({
#         "get": "retrieve",
#         "post": "update",
#         "delete": "destroy"
#     }))
# ]
