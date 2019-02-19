#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/1/31 16:30
# @Author : Huang Qin
# @Description :  默认的配置文件（可作为开发环境的标准配置）
# @usage :

"""
Default configurations.
"""
configs = {
    'debug': True,
    'db': {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'root',
        'password': 'root',
        'db': 'awesome'
    },
    'session': {
        'secret': 'Awesome'
    }
}
