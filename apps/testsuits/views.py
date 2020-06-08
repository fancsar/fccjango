import os
from datetime import datetime

from django.shortcuts import render

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from envs.models import Envs
from fccjango.settings import SUITES_DIR
from interfaces.models import Interfaces
from testcases.models import Testcases
from utils import common
from utils.time_famter import get_data
from .models import Testsuits
from .serializers import TestsuitsModelSerializer, TestsuitsRunSerializer
from .utils import get_testsuit_project_format


class TestsuitsList(viewsets.ModelViewSet):
    queryset = Testsuits.objects.all()
    serializer_class = TestsuitsModelSerializer

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data['results'] = get_testsuit_project_format(response.data['results'])
        return response

    def retrieve(self, request, *args, **kwargs):
        testsuit_obj = self.get_object()
        datas = {
            'name': testsuit_obj.name,
            'project_id': testsuit_obj.project_id,
            'include': testsuit_obj.include
        }
        return Response(datas)

    @action(methods=['post'], detail=True)
    def run(self, request, *args, **kwargs):
        testsuit = self.get_object()
        serializer = self.get_serializer(instance=testsuit, data=request.data)
        serializer.is_valid(raise_exception=True)
        # 此时的data为校验后的数据
        datas = serializer.validated_data
        env_id = datas.get('env_id')
        # 将文件夹时间戳处理化
        testcase_dir_path = os.path.join(SUITES_DIR, datetime.strftime(datetime.now(), '%Y-%m-%d_%H.%M.%S_%f'))
        os.mkdir(testcase_dir_path)
        # 获取环境变量对象
        env_obj = Envs.objects.get(id=env_id)
        # 从include中获取运行接口id
        include = eval(testsuit.include)
        if not include:
            data = {
                'detail': '此套件下无接口，无法运行'
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        # 获取套件下所有接口
        for interface_id in include:
            testcase_list = Testcases.objects.filter(interface_id=interface_id)
            for case_obj in testcase_list:
                common.generate_testcase_files(case_obj, env_obj, testcase_dir_path)
        return common.run_testcase(testsuit, testcase_dir_path)

    def get_serializer_class(self):
        return TestsuitsRunSerializer if self.action == 'run' else self.serializer_class
