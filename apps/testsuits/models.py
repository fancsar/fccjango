from django.db import models

from utils.base_models import BaseModel


class Testsuits(BaseModel):
    id = models.AutoField(verbose_name='id主键', help_text='id主键', primary_key=True)
    name = models.CharField(verbose_name='套件名称', help_text='套件名称', unique=True, max_length=100)
    include = models.TextField(verbose_name='包含的接口', help_text='包含的接口', null=False)
    project = models.ForeignKey(to='projects.Projects', on_delete=models.CASCADE, related_name='testsuits',
                                help_text='所属项目')

    class Meta:
        db_table = 'tb_testsuits'
        verbose_name = '套件信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
