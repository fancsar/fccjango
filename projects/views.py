# -*- coding: utf-8 -*-

import json
from django.http import HttpResponse, JsonResponse, Http404
from django.views import View
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from .models import Projects
from .serializers import ProjectsModelSerializer


def haha(request):
    return HttpResponse('<h1>Success</h1>')


# 使用类视图
class ProjectList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  GenericAPIView):
    queryset = Projects.objects.all()
    serializer_class = ProjectsModelSerializer
    # 指定过滤引擎，排序引擎
    # filter_backends = [DjangoFilterBackend, OrderingFilter]
    # # 指定分页引擎
    # # pagination_class =
    # # 指定的过滤字段
    filterset_fields = ['id', 'name', 'leader', 'tester']
    # # 指定排序字段，默认为升序排列
    ordering_fields = ['id', 'name']

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class IndexView(mixins.RetrieveModelMixin,
                mixins.UpdateModelMixin,
                mixins.DestroyModelMixin,
                GenericAPIView):
    '''
    index: 主页类视图
    1.类视图需要继承View或者View子类
    2.实例方法get,post,put,delete（全部小写），与其响应的请求方法一一对应
    3.方法的第一个参数为，该视图对象本身，第二个为HttpRequest请求对象
    4. 
    '''
    queryset = Projects.objects.all()
    serializer_class = ProjectsModelSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
