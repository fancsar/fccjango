import json
import os

from django.http import StreamingHttpResponse
from django.shortcuts import render
from django.utils.encoding import escape_uri_path
from rest_framework.decorators import action

from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import mixins
from fccjango import settings
from utils.time_famter import get_data
from .models import Reports
from .serializers import ReportsModelSerializer
from .utils import get_reports_format, get_file_content


class ReportsList(mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    queryset = Reports.objects.all()
    serializer_class = ReportsModelSerializer

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data['results'] = get_reports_format(response.data['results'])
        return response

    @action(detail=True)
    def download(self, *args, **kwargs):
        report = self.get_object()
        report_html = report.html
        response = StreamingHttpResponse(iter(report_html))
        # 对文件名进行转义
        report_final_path = escape_uri_path(report.name + '.html')
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = f'attachment;filename={report_final_path}'
        return response

    def retrieve(self, request, *args, **kwargs):
        report = self.get_object()
        serializer = self.get_serializer(instance=report)
        datas = get_data(serializer.data)
        try:
            datas['summary'] = json.loads(datas['summary'], encoding='utf-8')
        except Exception as e:
            pass
        return Response(datas)
