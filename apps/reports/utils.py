# -*- coding: utf-8 -*-
# @Time   :2020/5/24 11:25
# @Author :XDF_FCC
# @Email  :fanchengcheng3@xdf.cn
# @File   :utils.py
from utils.time_famter import get_data


def get_reports_format(datas):
    for item in datas:
        get_data(item)
    return datas


def get_file_content(filename):
    """
    读取文件，返回一个生成器对象
    @param filename:
    @return:
    """
    with open(filename, encoding='utf-8') as file:
        while True:  # 不确定什么时候读取完
            line = file.read(1024)
            if line:
                yield line
            else:  # 如果line为None,那么说明已经读取到了文件末尾
                break
