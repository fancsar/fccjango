# -*- coding: utf-8 -*-
# @Time   :2020/5/21 21:04
# @Author :XDF_FCC
# @Email  :fanchengcheng3@xdf.cn
# @File   :utils.py
from utils.time_famter import get_data


def get_testsuit_project_format(datas):
    for item in datas:
        get_data(item)
        create_time_list = item['update_time'].split('T')
        first_part = create_time_list[0]
        second_part = create_time_list[1].split('.')[0]
        item['update_time'] = first_part + ' ' + second_part
    return datas
