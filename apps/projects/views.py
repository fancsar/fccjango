# -*- coding: utf-8 -*-

import json
import os
from datetime import datetime

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

from envs.models import Envs
from interfaces.models import Interfaces
from testcases.models import Testcases
from fccjango.settings import SUITES_DIR
from .models import Projects
from . import serializers
from . import utils
from utils.time_famter import get_data
from utils import common


def haha(request):
    return HttpResponse('<h1>Success</h1>')


# 使用类视图
class ProjectList(viewsets.ModelViewSet):
    queryset = Projects.objects.all()
    serializer_class = serializers.ProjectsModelSerializer
    filterset_fields = ['id', 'name', 'leader', 'tester']
    ordering_fields = ['id', 'name']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            data = utils.get_projects_list_format(serializer.data)
            return self.get_paginated_response(data)

        serializer = self.get_serializer(queryset, many=True)
        data = utils.get_projects_list_format(serializer.data)
        return Response(data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = get_data(serializer.data)
        return Response(data)

    # 获取所有的项目名
    @action(detail=False)
    def names(self, request, *args, **kwargs):
        project = self.get_queryset()
        # page = self.paginate_queryset(project)
        # if page is not None:
        #     serializer = self.get_serializer(instance=page, many=True)
        #     return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(instance=project, many=True)
        return Response(serializer.data)

    # 获取某个项目名下的所有接口信息
    @action(detail=True)
    def interfaces(self, request, *args, **kwargs):
        pro_ins = self.get_object()
        serializer = self.get_serializer(instance=pro_ins)
        data = utils.get_project_interface_format(serializer.data["interfaces"])
        return Response(data)

    @action(methods=['post'], detail=True)
    def run(self, request, *args, **kwargs):
        project = self.get_object()
        serializer = self.get_serializer(instance=project, data=request.data)
        serializer.is_valid(raise_exception=True)
        # 此时的data为校验后的数据
        datas = serializer.validated_data
        env_id = datas.get('env_id')
        # 将文件夹时间戳处理化
        testcase_dir_path = os.path.join(SUITES_DIR, datetime.strftime(datetime.now(), '%Y-%m-%d_%H.%M.%S_%f'))
        os.mkdir(testcase_dir_path)
        # 获取环境变量对象
        env_obj = Envs.objects.get(id=env_id)
        # 获取项目下所有接口
        interface_objs = Interfaces.objects.filter(project=project)

        if not interface_objs.exists():
            data = {
                'detail': '此项目下无接口，无法运行'
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        for interface_obj in interface_objs:
            testcase_objs = Testcases.objects.filter(interface=interface_obj)
            for case_obj in testcase_objs:
                common.generate_testcase_files(case_obj, env_obj, testcase_dir_path)
        # 运行用例
        return common.run_testcase(project, testcase_dir_path)

    # 当遇到多个action用到多个serializer时，指定
    def get_serializer_class(self):
        if self.action == 'names':
            return serializers.ProjectsNameModelSerializer
        elif self.action == 'interfaces':
            return serializers.ProjectsInsModelSerializer
        elif self.action == 'run':
            return serializers.ProjectsRunSerializer
        else:
            return self.serializer_class
