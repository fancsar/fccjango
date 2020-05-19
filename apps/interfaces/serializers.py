from rest_framework import serializers

from .models import Interfaces
from projects.models import Projects


class ProjectMSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = '__all__'


class InterfacesModelSerializer(serializers.ModelSerializer):
    # 模型序列化默认指定的外键id
    project_id = serializers.PrimaryKeyRelatedField(write_only=True, label='所属项目id', help_text='所属项目id',
                                                    queryset=Projects.objects.all())
    # 使用接口的name名输出,调用projects模型类model中的__str__方法
    project = serializers.StringRelatedField(label='所属项目名称', help_text='所属项目名称')

    # project = ProjectMSerializer(read_only=True)

    class Meta:
        model = Interfaces
        # exclude = ('update_time',)
        # fields = '__all__'
        fields = ('id', 'name', 'tester', 'desc', 'project', 'project_id', 'create_time')

    def create(self, validated_data):
        validated_data['project_id'] = validated_data['project_id'].id
        interface = super().create(validated_data)
        return interface

    def update(self, instance, validated_data):
        validated_data['project_id'] = validated_data['project_id'].id
        super().update(instance, validated_data)
        return instance
