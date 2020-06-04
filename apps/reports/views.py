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
        # 1.手动创建报告
        reports = self.get_object()
        html = reports.html
        # 写入report文件中
        report_path = settings.REPORT_DIR
        report_full_path = os.path.join(report_path, reports.name) + '.html'
        with open(report_full_path, 'w', encoding='utf-8') as file:
            file.write(html)
        # 2. 读取创建的报告，返回给前端
        # 如果提供前端用户能够下载，则需要在响应头中修改Content-Type
        # Content-Disposition:attachment
        response = StreamingHttpResponse(get_file_content(report_full_path))
        # 对文件名进行转义
        report_final_path = escape_uri_path(reports.name + '.html')
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
