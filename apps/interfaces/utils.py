# -*- coding: utf-8 -*-
# @Time   :2020/5/18 13:17
# @Author :XDF_FCC
# @Email  :fanchengcheng3@xdf.cn
# @File   :utils.py
from utils.time_famter import get_data
from testcases.models import Testcases
from configures.models import Configures


def get_interface_list_format(datas):
    for item in datas:
        item = get_data(item)
        interface_id = item['id']
        testcases = Testcases.objects.filter(interface_id=interface_id).count()
        configures = Configures.objects.filter(interface_id=interface_id).count()
        item['testcases'] = testcases
        item['configures'] = configures
    return datas
