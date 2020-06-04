# -*- coding: utf-8 -*-
# @Time   :2020/6/3 17:30
# @Author :XDF_FCC
# @Email  :fanchengcheng3@xdf.cn
# @File   :handle_datas.py


def handle_param_type(value):
    if isinstance(value, int):
        param_type = "int"
    elif isinstance(value, float):
        param_type = "float"
    elif isinstance(value, bool):
        param_type = "boolean"
    else:
        param_type = "string"
    return param_type


def handle_data1(datas):
    result_list = []
    if datas is not None:
        for dict in datas:
            key = dict.get('check')
            value = dict.get("expected")
            comparator = dict.get("comparator")
            result_list.append({
                "key": key,
                "value": value,
                "comparator": comparator,
                "param_type": handle_param_type(value)
            })
    return result_list


def handle_data2(datas):
    """
    [{"var1":"val1"},{"var2":100}],

    @param datas: 嵌套列表的字典
    @return:
    """
    result_list = []
    if datas is not None:
        for dict in datas:
            key = list(dict)[0]
            value = dict.get(key)
            result_list.append({
                "key": key,
                "value": value,
                "param_type": handle_param_type(value)
            })
    return result_list


def handle_data3(datas):
    """
    处理格式，将 [{'token':'content.token'}]
    转换为 [{'key':'token','value':'content.token'}]

    """
    result_list = []
    if datas is not None:
        for dict in datas:
            key = list(dict)[0]
            value = dict.get(key)
            # value = list(datas.values())[0]
            result_list.append({
                "key": key,
                "value": value,
            })
    return result_list


def handle_data4(datas):
    """
    datas: dict 字典类型
    """
    result_list = []
    if datas is not None:
        for key, value in datas.items():
            result_list.append({
                "key": key,
                "value": value
            })
    # result_list = [{"key": key, "value": value} for key, value in datas.items() if datas is not None]

    return result_list


def handle_data5(datas):
    result_list = []
    if datas is not None:
        for item in datas:
            result_list.append({
                "key": item,
            })
    return result_list


def handle_data6(datas):
    result_list = []
    if datas is not None:
        for key, value in datas.items():
            result_list.append({
                "key": key,
                "value": value,
                "param_type": handle_param_type(value)
            })
    return result_list
