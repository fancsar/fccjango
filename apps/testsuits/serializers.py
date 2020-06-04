# -*- coding: utf-8 -*-
# @Time   :2020/5/21 20:35
# @Author :XDF_FCC
# @Email  :fanchengcheng3@xdf.cn
# @File   :serializers.py
from rest_framework import serializers
from .models import Testsuits
from projects.models import Projects
from interfaces.models import Interfaces


class TestsuitsModelSerializer(serializers.ModelSerializer):
    project = serializers.StringRelatedField(label='所属项目名称', help_text='所属项目名称')
    project_id = serializers.PrimaryKeyRelatedField(write_only=True, label='所属项目id', help_text='所属项目id',
                                                    queryset=Projects.objects.all())

    class Meta:
        model = Testsuits
        fields = ('id', 'name', 'project', 'project_id', 'create_time', 'update_time')

        extra_kwargs = {
            'include': {
                'write_only': True
            },
            'create_time': {
                'read_only': True
            },
            'update_time': {
                'read_only': True
            },
        }

    def create(self, validated_data):
        validated_data['project_id'] = validated_data['project_id'].id
        testsuit = super().create(validated_data)
        return testsuit

    def update(self, instance, validated_data):
        validated_data['project_id'] = validated_data['project_id'].id
        super().update(instance, validated_data)
        return instance

    def validate(self, attrs):
        include = eval(attrs['include'])
        project_id = attrs['project_id'].id
        interface = Interfaces.objects.filter(project_id=project_id)
        interface_list = [inter.id for inter in interface]
        for item in include:
            if item not in interface_list:
                raise serializers.ValidationError(f'该接口id值({item})不是该项目{attrs["project_id"]}id值为({project_id})的接口')
        return attrs
