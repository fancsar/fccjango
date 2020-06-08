from rest_framework import serializers

from .models import Projects
from interfaces.models import Interfaces
from debugtalks.models import DebugTalks
from envs.models import Envs


def is_unique_project_name(value):
    project = Projects.objects.filter(name=value)
    if project:
        raise serializers.ValidationError(f'该{value}名已存在')


class ProjectsSerializer(serializers.Serializer):
    id = serializers.IntegerField(label='id主键', help_text='id主键', read_only=True)
    name = serializers.CharField(label='项目名称', help_text='项目名称', max_length=200, validators=[is_unique_project_name])
    leader = serializers.CharField(label='项目负责人', help_text='项目负责人', max_length=50)
    tester = serializers.CharField(label='测试人员', help_text='测试人员', max_length=50)
    programmer = serializers.CharField(label='开发人员', help_text='开发人员', max_length=50)
    publish_app = serializers.CharField(label='发布应用', help_text='发布应用', max_length=100)
    desc = serializers.CharField(label='简要描述', help_text='简要描述', max_length=200, default='', allow_blank=True,
                                 allow_null=True)

    # class Meta:
    #     db_table = 'tb_projects'
    # 对name单字段进行校验
    def validate_name(self, value):
        if not value.endswith("项目"):
            raise serializers.ValidationError('项目名称必须以“项目”结尾')
        return value

    # 多字段校验
    def validate(self, attrs):
        name = attrs['name']
        leader = attrs['leader']
        if '项目' not in name and 'fancc' not in leader:
            raise serializers.ValidationError(f'{name}中不包含"项目"，并且{leader}中要包含fancc')
        return attrs

    def create(self, validated_data):
        project = Projects.objects.create(**validated_data)
        return project

    def update(self, instance, validated_data):
        instance.name = validated_data['name']
        instance.leader = validated_data['leader']
        instance.tester = validated_data['tester']
        instance.programer = validated_data['programer']
        instance.publish_app = validated_data['publish_app']
        instance.desc = validated_data['desc']
        # 更新数据进行保存
        instance.save()
        return instance


# -----------------interfaces项目--------------
class InterfacesMSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interfaces
        # fields = '__all__'
        exclude = ('update_time',)


class ProjectsModelSerializer(serializers.ModelSerializer):
    # interfaces = serializers.StringRelatedField(many=True)
    # interfaces = InterfacesMSerializer(many=True, read_only=True)

    class Meta:
        model = Projects
        exclude = ('update_time',)
        # fields = ('id', 'name', 'leader', 'tester', 'programmer', 'publish_app', 'desc', 'interfaces')
        extra_kwargs = {
            'name': {
                # 'validators': [is_unique_project_name],
                'error_messages': {
                    'max_length': '不能超过200个字符'
                }
            },
            'leader': {
                'min_length': 2,
                'error_messages': {
                    'min_length': '就是一傻逼'
                }
            },
            'create_time': {
                'read_only': True
            }
        }

    # 对name单字段进行校验
    def validate_name(self, value):
        if not value.endswith("项目"):
            raise serializers.ValidationError('项目名称必须以“项目”结尾')
        return value

    # 多字段校验
    def validate(self, attrs):
        name = attrs['name']
        leader = attrs['leader']
        if '项目' not in name and 'fancc' not in leader:
            raise serializers.ValidationError(f'{name}中不包含"项目"，并且{leader}中要包含fancc')
        return attrs

    def create(self, validated_data):
        project = super().create(validated_data)
        DebugTalks.objects.create(project=project)
        return project


class ProjectsNameModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        # exclude = ('create_time', 'update_time')
        fields = ('id', 'name')


class ProjectsInsModelSerializer(serializers.ModelSerializer):
    interfaces = InterfacesMSerializer(many=True, read_only=True)

    class Meta:
        model = Projects
        # exclude = ('create_time', 'update_time')
        fields = ('interfaces',)


class ProjectsRunSerializer(serializers.ModelSerializer):
    env_id = serializers.IntegerField(label='环境id', help_text='环境id', write_only=True)

    class Meta:
        model = Projects
        fields = ('id', 'env_id')

    def validate_env_id(self, value):
        if not isinstance(value, int):
            raise serializers.ValidationError('所填参数有误')
        elif not Envs.objects.filter(id=value).exists():
            raise serializers.ValidationError('所选环境不存在')
        # 字段校验完后，必须返回值
        return value
