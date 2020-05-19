import json

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
