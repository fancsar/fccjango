# -*- coding: utf-8 -*-
# @Time   :2020/5/19 16:29
# @Author :XDF_FCC
# @Email  :fanchengcheng3@xdf.cn
# @File   :serializers.py
from rest_framework import serializers
from .models import Envs


class EnvsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Envs
        exclude = ('update_time',)
