from django.db import models
from rest_framework import serializers


# Create your models here.


class Projects(models.Model):
    id = models.AutoField(verbose_name='id主键', help_text='id主键', primary_key=True)
    name = models.CharField(verbose_name='项目名称', help_text='项目名称', unique=True, max_length=200)
    leader = models.CharField(verbose_name='项目负责人', help_text='项目负责人', max_length=50)
    tester = models.CharField(verbose_name='测试人员', help_text='测试人员', max_length=50)
    programmer = models.CharField(verbose_name='开发人员', help_text='开发人员', max_length=50)
    publish_app = models.CharField(verbose_name='发布应用', help_text='发布应用', max_length=100)
    desc = models.CharField(verbose_name='简要描述', help_text='简要描述', max_length=200, default='', blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', help_text='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间', help_text='更新时间')

    class Meta:
        db_table = 'tb_projects'

    def __str__(self):
        return self.name


def is_unique_project_name(value):
    project = Projects.objects.filter(name=value)
    if project:
        raise serializers.ValidationError(f'该{value}名已存在')


class ProjectsSerializer(serializers.Serializer):
    id = serializers.IntegerField(label='id主键', help_text='id主键', write_only=True)
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
