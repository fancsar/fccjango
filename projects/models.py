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


