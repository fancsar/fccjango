from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Envs
from .serializers import EnvsModelSerializer
from .utils import get_envs_list_format
from utils.time_famter import get_data


class EnvsList(viewsets.ModelViewSet):
    queryset = Envs.objects.all()
    serializer_class = EnvsModelSerializer

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data['results'] = get_envs_list_format(response.data['results'])
        return response

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        response.data = get_data(response.data)
        return response

    # 获取所有环境变量的名称
    @action(detail=False)
    def names(self, request, *args, **kwargs):
        envs = self.filter_queryset(self.get_queryset())
        data = [{'id': obj.id, 'name': obj.name} for obj in envs]
        return Response(data)
