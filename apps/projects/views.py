# -*- coding: utf-8 -*-

import json
from django.http import HttpResponse, JsonResponse, Http404
from django.views import View
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets

from .models import Projects
from . import serializers


def haha(request):
    return HttpResponse('<h1>Success</h1>')


# 使用类视图
class ProjectList(viewsets.ModelViewSet):
    """
    create: 新增项目
    list: 查询项目所有信息
    retrieve: 获取某一个项目信息
    update: 更改某个项目信息(全部更新)
    partial_update: 更改某个项目信息(部分更新)
    destroy: 删除某个项目
    names: 获取所有的项目名称
    interface: 获取某个项目的所有接口信息
    """
    queryset = Projects.objects.all()
    serializer_class = serializers.ProjectsModelSerializer
    filterset_fields = ['id', 'name', 'leader', 'tester']
    ordering_fields = ['id', 'name']

    # 获取所有的项目名
    @action(detail=False)
    def names(self, request, *args, **kwargs):
        project = self.get_queryset()
        page = self.paginate_queryset(project)
        if page is not None:
            serializer = self.get_serializer(instance=page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(instance=project, many=True)
        return Response(serializer.data)

    # 获取某个项目名下的所有接口信息
    @action(detail=True)
    def interface(self, request, *args, **kwargs):
        pro_ins = self.get_object()
        serializer = self.get_serializer(instance=pro_ins)
        return Response(serializer.data["interfaces"])

    # 当遇到多个action用到多个serializer时，指定
    def get_serializer_class(self):
        if self.action == 'names':
            return serializers.ProjectsNameModelSerializer
        elif self.action == 'interface':
            return serializers.ProjectsInsModelSerializer
        else:
            return self.serializer_class
