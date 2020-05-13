from django.db import models
from projects.models import Projects


# Create your models here.


class Interfaces(models.Model):
    '''
    接口模型类
    一个项目中有多个接口
    一个接口属于一个项目
    项目表和接口表的关系
    一对多、需要在多的那一层，创建外键
    '''
    id = models.AutoField(verbose_name='id主键', help_text='id主键', primary_key=True)
    name = models.CharField(verbose_name='接口名称', help_text='接口名称', unique=True, max_length=200)
    tester = models.CharField(verbose_name='测试人员', help_text='测试人员', max_length=50)
    desc = models.CharField(verbose_name='简要描述', help_text='简要描述', max_length=200, default='', blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', help_text='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间', help_text='更新时间')
    # 设置外键,使用ForeignKey,第一个参数为'父类的应用名.模型类'，或者模型类,
    # 第二个参数为on_delete,该属性为主表(父表)删除以后，从表的删除逻辑，
    # on_delete = models.SET_NULL 是主表删除以后，子表会自动设置为null
    # on_delete = models.CASCADE 为父表删除之后，子表也会删除
    # related_name 指定父表对子表引用名，如不指定，默认为子表模型类名小写_set 即 interfances_set
    # project = models.ForeignKey(to='Projects')
    project = models.ForeignKey(to='projects.Projects', on_delete=models.CASCADE, related_name='interfaces',
                                help_text='所属项目')

    class Meta:
        db_table = 'tb_interfaces'
        verbose_name = '接口'

    def __str__(self):
        return self.name
    
