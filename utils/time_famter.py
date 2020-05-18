# -*- coding: utf-8 -*-
# @Time   :2020/5/17 15:13
# @Author :XDF_FCC
# @Email  :fanchengcheng3@xdf.cn
# @File   :time_famter.py
def get_data(item):
    create_time_list = item['create_time'].split('T')
    first_part = create_time_list[0]
    second_part = create_time_list[1].split('.')[0]
    item['create_time'] = first_part + ' ' + second_part
    return item
# def get_data(item):
#     def time_format(func):
#         def wrapper(*args, **kwargs):
#             create_time_list = item['create_time'].split('T')
#             first_part = create_time_list[0]
#             second_part = create_time_list[1].split('.')[0]
#             item['create_time'] = first_part + ' ' + second_part
#             func(*args, **kwargs)
#
#         return wrapper
#
#     return time_format

#
# def fun(n):
#     def wrapper(*args, **kwargs):
#         print('xinz1')
#         aa = n(*args, **kwargs)
#         print('xinz2')
#         return aa
#
#     return wrapper
#
#
# @fun
# def qiu(num):
#     s = 0
#     for i in range(num):
#         s += i
#     print(s)
#
#
# qiu(200)
