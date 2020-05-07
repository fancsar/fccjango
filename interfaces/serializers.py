from rest_framework import serializers

from .models import Interfaces
from projects.models import Projects


class ProjectMSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = '__all__'


class InterfacesModelSerializer(serializers.ModelSerializer):
    # 模型序列化默认指定的外键id
    # project = serializers.PrimaryKeyRelatedField(label='所属项目', help_text='所属项目', queryset=Projects.objects.all())
    # 使用接口的name名输出,调用projects模型类model中的__str__方法
    # project = serializers.StringRelatedField(label='所属项目名称', help_text='所属项目名称')
    # project = ProjectMSerializer(read_only=True)

    class Meta:
        model = Interfaces
        # fields = '__all__'
        fields = ('id', 'name', 'tester', 'desc', 'project')
