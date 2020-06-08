from rest_framework import serializers

from .models import Interfaces
from projects.models import Projects
from envs.models import Envs


class ProjectMSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = '__all__'


class InterfacesModelSerializer(serializers.ModelSerializer):
    # 模型序列化默认指定的外键id
    project_id = serializers.PrimaryKeyRelatedField(label='所属项目id', help_text='所属项目id',
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


class InterfacesRunSerializer(serializers.ModelSerializer):
    env_id = serializers.IntegerField(label='环境id', help_text='环境id', write_only=True)

    class Meta:
        model = Interfaces
        fields = ('id', 'env_id')

    def validate_env_id(self, value):
        if not isinstance(value, int):
            raise serializers.ValidationError('所填参数有误')
        elif not Envs.objects.filter(id=value).exists():
            raise serializers.ValidationError('所选环境不存在')
        # 字段校验完后，必须返回值
        return value
