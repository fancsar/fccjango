from django.db import models

from utils.base_models import BaseModel


class DebugTalks(BaseModel):
    id = models.AutoField(verbose_name='id主键', help_text='id主键', primary_key=True)
    name = models.CharField(verbose_name='debugtalk文件名称', help_text='debugtalk文件名称', default='debugtalk.py',
                            max_length=200)
    debugtalk = models.TextField(null=True, default='#debugtalk.py', help_text='debugtalk.py', max_length=50)
    # 项目表和debugtalk文件是一对一的关系
    project = models.OneToOneField(to='projects.Projects', on_delete=models.CASCADE, related_name='debugtalks',
                                   help_text='所属项目')

    class Meta:
        db_table = 'tb_debugtalks'
        verbose_name = 'debugtalk.py文件'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
