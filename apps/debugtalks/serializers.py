# -*- coding: utf-8 -*-
# @Time   :2020/5/20 20:20
# @Author :XDF_FCC
# @Email  :fanchengcheng3@xdf.cn
# @File   :serializers.py
from rest_framework import serializers
from .models import DebugTalks


class DebugTalksModelSerializer(serializers.ModelSerializer):
    project = serializers.StringRelatedField(label='所属项目名称', help_text='所属项目名称')

    class Meta:
        model = DebugTalks
        exclude = ('update_time', 'create_time')

        extra_kwargs = {
            'name': {
                'read_only': True
            },
            'debugtalk': {
                'write_only': True
            }
        }
