# -*- coding: utf-8 -*-
# @Time   :2020/5/25 19:29
# @Author :XDF_FCC
# @Email  :fanchengcheng3@xdf.cn
# @File   :serializers.py
from rest_framework import serializers
from .models import Testcases
from projects.models import Projects
from interfaces.models import Interfaces
from envs.models import Envs


class InterfacesAnotherSerializer(serializers.ModelSerializer):
    project = serializers.StringRelatedField(label='所属项目名称', help_text='所属项目名称')
    pid = serializers.IntegerField(label='项目id', help_text='项目id', write_only=True)
    iid = serializers.IntegerField(label='接口id', help_text='接口id', write_only=True)

    class Meta:
        model = Interfaces
        fields = ('iid', 'name', 'project', 'pid')
        extra_kwargs = {
            'name': {
                'read_only': True
            }
        }

    def validate_pid(self, value):
        if not isinstance(value, int):
            raise serializers.ValidationError('所填参数有误')
        elif not Projects.objects.filter(id=value).exists():
            raise serializers.ValidationError('所选项目不存在')
        # 字段校验完后，必须返回值
        return value

    def validate_iid(self, value):
        if not isinstance(value, int):
            raise serializers.ValidationError('所填参数有误')
        elif not Interfaces.objects.filter(id=value).exists():
            raise serializers.ValidationError('所选项目不存在')
        # 字段校验完后，必须返回值
        return value


class TestcasesModelSerializer(serializers.ModelSerializer):
    interface = InterfacesAnotherSerializer(label='项目id和接口id', help_text='项目id和接口id')

    class Meta:
        model = Testcases
        fields = ('id', 'name', 'include', 'author', 'request', 'interface')

        extra_kwargs = {
            'include': {
                'write_only': True
            },
            'request': {
                'write_only': True
            },
        }

    def create(self, validated_data):
        interface = validated_data.pop('interface')
        validated_data['interface_id'] = interface['iid']
        return super().create(validated_data)

    def update(self, instance, validated_data):
        interface = validated_data.pop('interface')
        validated_data['interface_id'] = interface['iid']
        return super().update(instance, validated_data)


class TestcasesRunSerializer(serializers.ModelSerializer):
    env_id = serializers.IntegerField(label='环境id', help_text='环境id', write_only=True)

    class Meta:
        model = Testcases
        fields = ('id', 'env_id')

    def validate_env_id(self, value):
        if not isinstance(value, int):
            raise serializers.ValidationError('所填参数有误')
        elif not Envs.objects.filter(id=value).exists():
            raise serializers.ValidationError('所选环境不存在')
        # 字段校验完后，必须返回值
        return value
