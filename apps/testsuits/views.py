from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.response import Response
from utils.time_famter import get_data
from .models import Testsuits
from .serializers import TestsuitsModelSerializer
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
