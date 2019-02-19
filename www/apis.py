#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/1/31 11:49
# @Author : Huang Qin
# @Description :
# @usage :

"""
JSON API definition.
"""

import json, logging, inspect, functools


# 存储分页信息
class Page(object):
    """
    Page object for display pages.
    """

    def __init__(self, item_count, page_index=1, page_size=10):
        """
        Init Pagination by item_count, page_index and page_size.
        :param item_count: 总条数
        :param page_index: 第几页
        :param page_size: 每页条数
        """
        self.item_count = item_count  # 总条数
        self.page_size = page_size   # 每页条数
        self.page_count = item_count // page_size + (1 if item_count % page_size > 0 else 0)  # 总页数
        if (item_count == 0) or (page_index > self.page_count):
            self.offset = 0  # 从第1条数据开始
            self.limit = 0  # 每页条数为0
            self.page_index = 1  # 第1页
        else:
            self.page_index = page_index  # 第几页
            self.offset = self.page_size * (page_index - 1)  # 第几条数据开始
            self.limit = self.page_size  # 每页条数
        self.has_next = self.page_index < self.page_count  # 是否有下一页
        self.has_previous = self.page_index > 1  # 是否有上一页

    def __str__(self):
        return 'item_count: %s, page_count: %s, page_index: %s, page_size:%s, offset: %s, limit: %s' % (self.item_count,
                                                                                                        self.page_count,
                                                                                                        self.page_index,
                                                                                                        self.page_size,
                                                                                                        self.offset,
                                                                                                        self.limit)

    __repr__ = __str__


class APIError(Exception):
    """
    the base APIError which contains error(required), data(optional) and message(optional).
    """
    def __init__(self, error, data='', message=''):
        super(APIError, self).__init__(message)
        self.error = error
        self.data = data
        self.message = message


class APIValueError(APIError):
    """
    Indicate the input value has error or invalid. The data specifies the error field of input form.
    """
    def __init__(self, field, message=''):
        super(APIValueError, self).__init__('value:invalid', field, message)


class APIResourceNotFoundError(APIError):
    """
    Indicate the resource was not found. The data specifies the resource name.
    """
    def __init__(self, field, message=''):
        super(APIResourceNotFoundError, self).__init__('value:not found', field, message)


class APIPermissionError(APIError):
    """
    Indicate the api has no permission.
    """
    def __init__(self, message=''):
        super(APIPermissionError, self).__init__('permission:forbidden', 'permission', message)
