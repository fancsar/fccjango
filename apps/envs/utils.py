# -*- coding: utf-8 -*-
# @Time   :2020/5/19 17:28
# @Author :XDF_FCC
# @Email  :fanchengcheng3@xdf.cn
# @File   :utils.py
from utils.time_famter import get_data


def get_envs_list_format(datas):
    for item in datas:
        get_data(item)
    return datas
