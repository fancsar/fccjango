# -*- coding: utf-8 -*-
# @Time   :2020/5/26 21:17
# @Author :XDF_FCC
# @Email  :fanchengcheng3@xdf.cn
# @File   :utils.py

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


# 将[{check':'status code','expected':200,'comparator':‘equals')]
# 转化为[{key:'status code',value:200,comparator:'equals',param type:'string'}]

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


def handle_data4(datas):
    # result_list = []
    # if datas is not None:
    #     for key, value in datas.items():
    #         result_list.append({
    #             "key": key,
    #             "value": value
    #         })
    result_list = [{"key": key, "value": value} for key, value in datas.items() if datas is not None]

    return result_list


bb = {'a': 1, 'b': 2}
aa = handle_data4(bb)
print(aa)
print(list(bb))
