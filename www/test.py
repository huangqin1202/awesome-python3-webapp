#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/1/30 17:33
# @Author : Huang Qin
# @Description :  一句话描述该类的功能
# @usage :
import asyncio
import orm
from models import Users


# 添加用户到数据库
async def insertUser(loop):
    await orm.create_pool(loop=loop, user='root', password='root', db='awesome')
    u = Users(name='Test01', email='test01@example.com', passwd='123456', image='about:blank')
    await u.save()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(insertUser(loop))
    loop.run_forever()
