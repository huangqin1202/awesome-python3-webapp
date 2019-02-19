#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/1/31 9:26
# @Author : Huang Qin
# @Description :  定义数据库表对应的Model对象
# @usage :

"""
Models for user, blog, comment
"""

import time
import uuid
from orm import Model, StringField, BooleanField, FloatField, TextField

# 用于生成主键id
def next_id():
    return '%015d%s000' % (int(time.time() * 1000), uuid.uuid4().hex)


class Users(Model):
    __table__ = 'users'

    id = StringField(primary_key=True, default=next_id(), ddl='varchar(50)')
    email = StringField(ddl='varchar(50)')
    passwd = StringField(ddl='varchar(50)')
    admin = BooleanField()
    name = StringField(ddl='varchar(50)')
    image = StringField(ddl='varchar(500)')
    created_at = FloatField(default=time.time())  # 默认值为当前日期和时间，用float类型存储在数据库中


class Blog(Model):
    __table__ = 'blog'

    id = StringField(primary_key=True, default=next_id(), ddl='varchar(50)')
    user_id = StringField(ddl='varchar(50)')
    user_name = StringField(ddl='varchar(50)')
    user_image = StringField(ddl='varchar(500)')
    name = StringField(ddl='varchar(50)')
    summary = StringField(ddl='varchar(200)')
    content = TextField()
    created_at = FloatField(default=time.time())  # 默认值为当前日期和时间，用float类型存储在数据库中


class Comment(Model):
    __table__ = 'comment'

    id = StringField(primary_key=True, default=next_id(), ddl='varchar(50)')
    blog_id = StringField(ddl='varchar(50)')
    user_id = StringField(ddl='varchar(50)')
    user_name = StringField(ddl='varchar(50)')
    user_image = StringField(ddl='varchar(500)')
    content = TextField()
    created_at = FloatField(default=time.time())  # 默认值为当前日期和时间，用float类型存储在数据库中


