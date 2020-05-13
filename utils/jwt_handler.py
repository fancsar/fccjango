# -*- coding: utf-8 -*-
# @Time   :2020/5/12 18:51
# @Author :XDF_FCC
# @Email  :fanchengcheng3@xdf.cn
# @File   :jwt_handler.py


def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'user_id': user.id,
        'user_name': user.username
    }
