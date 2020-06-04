from django.shortcuts import render
import json
from rest_framework import viewsets
from rest_framework.response import Response
from utils.time_famter import get_data
from .models import Testcases
from interfaces.models import Interfaces
from .serializers import TestcasesModelSerializer
from utils import handle_datas


class TestcasesList(viewsets.ModelViewSet):
    queryset = Testcases.objects.all()
    serializer_class = TestcasesModelSerializer

    def retrieve(self, request, *args, **kwargs):
        testcase = self.get_object()
        testcase_include = json.loads(testcase.include, encoding='utf-8')
        testcase_request = json.loads(testcase.request, encoding='utf-8')
        testcase_request_datas = testcase_request.get('test').get('request')
        # validate
        testcase_validate = testcase_request.get('test').get('validate')
        # 处理params参数
        testcase_request_params = testcase_request_datas.get('params')
        testcase_request_params_list = handle_datas.handle_data4(testcase_request_params)

        # 处理用例的header列表
        testcases_headers = testcase_request_datas.get('headers')
        testcase_request_headers_list = handle_datas.handle_data4(testcases_headers)

        # 处理用例variables变量列表
        testcase_variables = testcase_request.get('test').get('variables')
        testcase_variables_list = handle_datas.handle_data2(testcase_variables)

        # 处理form表单数据
        testcase_form_datas = testcase_request_datas.get('data')
        testcase_form_datas_list = handle_datas.handle_data6(testcase_form_datas)

        # 处理json格式数据
        testcase_request_json = json.dumps(testcase_request_datas.get('json'), ensure_ascii=False)

        # 处理extract数据
        testcase_extract = testcase_request.get('test').get('extract')
        testcase_extract_list = handle_datas.handle_data3(testcase_extract)

        # 处理parameters数据(处理参数化数据)
        # 在平台使用时，运用嵌套列表的列表
        testcase_parameters = testcase_request.get('test').get('parameters')
        testcase_parameters_list = handle_datas.handle_data3(testcase_parameters)

        # 处理setupHooks数据
        testcase_setup_hooks = testcase_request.get('test').get('setup_hooks')
        testcase_setup_hooks_list = handle_datas.handle_data5(testcase_setup_hooks)

        # 处理teardownHooks数据
        testcase_teardown_hooks = testcase_request.get('test').get('teardown_hooks')
        testcase_teardown_hooks_list = handle_datas.handle_data5(testcase_teardown_hooks)

        web_selected_configure_id = testcase_include.get('config')
        web_selected_interface_id = testcase.interface_id
        web_selected_project_id = Interfaces.objects.get(id=web_selected_interface_id).project_id
        web_selected_testcase_id = testcase_include.get('testcases')

        datas = {
            "author": testcase.author,
            "testcase_name": testcase.name,
            "selected_interface_id": web_selected_interface_id,
            "selected_project_id": web_selected_project_id,
            "selected_configure_id": web_selected_configure_id,
            "selected_testcase_id": web_selected_testcase_id,

            "method": testcase_request_datas.get("method"),
            "url": testcase_request_datas.get("url"),
            "param": testcase_request_params_list,
            "header": testcase_request_headers_list,
            "variable": testcase_variables_list,
            "jsonVariable": testcase_request_json,

            "extract": testcase_extract_list,
            "validate": testcase_validate,
            "globalVar": testcase_variables_list,
            "parameterized": testcase_parameters_list,
            "setupHooks": testcase_setup_hooks_list,
            "teardownHooks": testcase_teardown_hooks_list,
        }
        return Response(datas)
