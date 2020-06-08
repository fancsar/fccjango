# -*- coding: utf-8 -*-
# @Time   :2020/5/24 11:25
# @Author :XDF_FCC
# @Email  :fanchengcheng3@xdf.cn
# @File   :utils.py
import os
from utils.time_famter import get_data
from fccjango.settings import REPORT_DIR


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


# 获取目录下所有的文件夹
def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        print('root_dir:', root)  # 当前目录路径
        print('sub_dirs:', dirs)  # 当前路径下所有子目录
        print('files:', files)  # 当前路径下所有非目录子文件
