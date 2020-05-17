# -*- coding: utf-8 -*-
# @Time   :2020/5/17 10:59
# @Author :XDF_FCC
# @Email  :fanchengcheng3@xdf.cn
# @File   :base_models.py
from django.db import models


class BaseModel(models.Model):
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', help_text='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间', help_text='更新时间')

    class Meta:
        abstract = True
        verbose_name = '公共字段'
