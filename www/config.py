#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/1/31 16:37
# @Author : Huang Qin
# @Description :  一句话描述该类的功能
# @usage :

import config_default


class Dict(dict):
    """
    Simple dict but support access as x.y style.
    """
    def __init__(self, names=(), values=(), **kw):
        super(Dict, self).__init__(**kw)
        for k, v in zip(names, values):
            self[k] = v

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value


def merge(defaults, override):
    """
    合并默认配置和覆盖配置
    :param defaults: 默认配置
    :param override: 覆盖配置
    :return: 合并后的配置
    """
    r = {}
    for k, v in defaults.items():
        if k in override:
            if isinstance(v, dict):
                r[k] = merge(v, override[k])
            else:
                r[k] = override[k]
        else:
            r[k] = v
    return r


def to_dict(d):
    """
    转换为Dict对象
    :param d:
    :return:
    """
    d_d = Dict()
    for k, v in d.items():
        d_d[k] = to_dict(v) if isinstance(v, dict) else v
    return d_d


configs = config_default.configs  # 默认配置
try:
    import config_override
    configs = merge(configs, config_override.configs)  # 覆盖后的配置
except ImportError:
    pass

configs = to_dict(configs)

