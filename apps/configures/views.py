import json
from jsonpath import jsonpath
from rest_framework import viewsets
from rest_framework.response import Response
from utils.time_famter import get_data
from interfaces.models import Interfaces
from .models import Configures
from .serializers import ConfiguresModelSerializer
from utils import handle_datas


class ConfiguresList(viewsets.ModelViewSet):
    queryset = Configures.objects.all()
    serializer_class = ConfiguresModelSerializer

    def retrieve(self, request, *args, **kwargs):
        config_obj = self.get_object()
        config_request = json.loads(config_obj.request)
        # 处理请求头数据
        config_headers = jsonpath(config_request, '$..headers')
        web_handers_list = handle_datas.handle_data4(config_headers[0])
        # 处理全局配置数据
        config_variables = config_request['config'].get('variables')
        web_variables_list = handle_datas.handle_data2(config_variables)
        # 获取配置名称
        web_name = config_request['config'].get('name')
        # 该配置的接口id值
        web_selected_interface_id = config_obj.interface_id
        # 该配置的项目id值
        web_selected_project_id = Interfaces.objects.get(id=web_selected_interface_id).project_id
        datas = {
            "author": config_obj.author,
            "configure_name": web_name,
            "selected_interface_id": web_selected_interface_id,
            "selected_project_id": web_selected_project_id,
            "header": web_handers_list,
            "globalVar": web_variables_list,
        }
        return Response(datas)
