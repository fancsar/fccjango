import json
import os
from datetime import datetime

from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import render

# Create your views here.
from django.views import View
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from envs.models import Envs
from fccjango.settings import SUITES_DIR
from utils import common
from .models import Interfaces
from . import serializers
from . import utils
from utils.time_famter import get_data
from testcases.models import Testcases
from configures.models import Configures


# class InterfanceList(GenericAPIView):
#     queryset = Interfaces.objects.all()
#     serializer_class = InterfacesModelSerializer
#     filterset_fields = ['name', 'tester']
#     ordering_fields = ['id', 'name']
#
#     def get(self, request):
#         interfaces = self.filter_queryset(self.get_queryset())
#         page = self.paginate_queryset(interfaces)
#         if page is not None:
#             interface_page_list = self.get_serializer(instance=page, many=True)
#             return self.get_paginated_response(interface_page_list.data)
#         serializer = self.get_serializer(instance=interfaces, many=True)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#     def post(self, request):
#         serializer = self.get_serializer(data=request.data)
#         try:
#             serializer.is_valid(raise_exception=True)
#         except:
#             Response(Http404, status=status.HTTP_400_BAD_REQUEST)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#
# class InterfacesDetail(GenericAPIView):
#     queryset = Interfaces.objects.all()
#     serializer_class = InterfacesModelSerializer
#
#     def get(self, request, pk):
#         interface = self.get_object()
#         serializer = self.get_serializer(instance=interface)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#     def post(self, request, pk):
#         interface = self.get_object()
#         serializer = self.get_serializer(data=request.data, instance=interface)
#         try:
#             serializer.is_valid(raise_exception=True)
#         except:
#             Response(Http404, status=status.HTTP_400_BAD_REQUEST)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#     def delete(self, request, pk):
#         interface = self.get_object()
#         interface.delete()
#         return Response(None, status=status.HTTP_204_NO_CONTENT)
class InterfanceList(viewsets.ModelViewSet):
    queryset = Interfaces.objects.all()
    serializer_class = serializers.InterfacesModelSerializer
    filterset_fields = ['id', 'name', 'tester']
    ordering_fields = ['id', 'name']

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data['results'] = utils.get_interface_list_format(response.data['results'])
        return response

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        response.data = get_data(response.data)
        return response

    @action(detail=True)
    def testcases(self, request, pk):
        testcases = Testcases.objects.filter(interface_id=pk)
        data = [{'id': obj.id, 'name': obj.name} for obj in testcases]
        return Response(data)

    @action(detail=True, url_path='configs')
    def configures(self, request, pk):
        configures = Configures.objects.filter(interface_id=pk)
        data = [{'id': obj.id, 'name': obj.name} for obj in configures]
        return Response(data)

    @action(methods=['post'], detail=True)
    def run(self, request, *args, **kwargs):
        interface = self.get_object()
        serializer = self.get_serializer(instance=interface, data=request.data)
        serializer.is_valid(raise_exception=True)
        # 此时的data为校验后的数据
        datas = serializer.validated_data
        env_id = datas.get('env_id')
        # 将文件夹时间戳处理化
        testcase_dir_path = os.path.join(SUITES_DIR, datetime.strftime(datetime.now(), '%Y-%m-%d_%H.%M.%S_%f'))
        os.mkdir(testcase_dir_path)
        # 获取环境变量对象
        env_obj = Envs.objects.get(id=env_id)
        # 获取接口下所有用例
        testcase_objs = Testcases.objects.filter(interface=interface)
        if not testcase_objs.exists():
            data = {
                'detail': '此接口下无用例，无法运行'
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        for case_obj in testcase_objs:
            common.generate_testcase_files(case_obj, env_obj, testcase_dir_path)
        # 运行用例
        return common.run_testcase(interface, testcase_dir_path)

    def get_serializer_class(self):
        return serializers.InterfacesRunSerializer if self.action == 'run' else self.serializer_class
