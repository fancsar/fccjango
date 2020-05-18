# -*- coding: utf-8 -*-
# @Time   :2020/5/17 15:44
# @Author :XDF_FCC
# @Email  :fanchengcheng3@xdf.cn
# @File   :utils.py
from django.db.models import Count
from interfaces.models import Interfaces
from testcases.models import Testcases
from testsuits.models import Testsuits
from configures.models import Configures
from utils.time_famter import get_data


def get_projects_list_format(datas):
    for item in datas:
        item = get_data(item)
        # 获取项目id值
        project_id = item['id']
        interfances_testcases_obj = Interfaces.objects.values('id').annotate(testcases=Count('testcases')).filter(
            project_id=project_id)
        interfances_configures_obj = Interfaces.objects.values('id').annotate(configures=Count('configures')).filter(
            project_id=project_id)
        testsuits = Testsuits.objects.filter(project_id=project_id).count()
        item['interfaces'] = len(interfances_configures_obj)
        item['testcases'] = sum([i['testcases'] for i in interfances_testcases_obj])
        item['configures'] = sum([i['configures'] for i in interfances_configures_obj])
        item['testsuits'] = testsuits
    return datas


def get_project_interface_format(datas):
    for item in datas:
        get_data(item)
    return datas
