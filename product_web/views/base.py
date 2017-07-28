#!/usr/bin/python
# -*- coding: UTF-8 -*-

def entry_id_data_args(func):
    """
    入口解析
    :param func:
    :return:
    """
    def __(torn_self):
        user_name = torn_self.get_secure_cookie('user_name')
        user_level = torn_self.get_secure_cookie('user_level')
        if not user_name or user_level==1:
            torn_self.redirect('/')
            return
        func(torn_self)
    return __