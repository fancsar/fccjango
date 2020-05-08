# -*- coding: utf-8 -*-

import json
from django.http import HttpResponse, JsonResponse, Http404
from django.views import View
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from .models import Projects
from .serializers import ProjectsModelSerializer


def haha(request):
    return HttpResponse('<h1>Success</h1>')


# 使用类视图
class ProjectList(GenericAPIView):
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

    def get(self, request):
        projects = self.get_queryset()
        # 使用过滤后的查询级
        projects = self.filter_queryset(projects)
        page = self.paginate_queryset(projects)
        if page is not None:
            project_page_list = self.get_serializer(instance=page, many=True)
            return self.get_paginated_response(project_page_list.data)
        project_list = self.get_serializer(instance=projects, many=True)
        return Response(project_list.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class IndexView(GenericAPIView):
    '''
    index: 主页类视图
    1.类视图需要继承View或者View子类
    2.实例方法get,post,put,delete（全部小写），与其响应的请求方法一一对应
    3.方法的第一个参数为，该视图对象本身，第二个为HttpRequest请求对象
    4. 
    '''
    queryset = Projects.objects.all()
    serializer_class = ProjectsModelSerializer

    def get(self, request, pk):
        project = self.get_object()
        serializer = self.get_serializer(instance=project)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, pk):
        project = self.get_object()
        serializer = self.get_serializer(data=request.data, instance=project)
        try:
            serializer.is_valid(raise_exception=True)
        except:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        project = self.get_object()
        project.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
