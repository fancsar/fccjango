# -*- coding: utf-8 -*-
# @Time   :2020/5/24 11:13
# @Author :XDF_FCC
# @Email  :fanchengcheng3@xdf.cn
# @File   :serializers.py
from rest_framework import serializers
from .models import Reports


class ReportsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reports
        # fields = ('id', 'name', 'project', 'project_id', 'create_time', 'update_time')
        exclude = ('update_time',)

        extra_kwargs = {
            'create_time': {
                'read_only': True
            }
        }
