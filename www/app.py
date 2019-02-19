#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
import logging
import asyncio, os, json, time
from datetime import datetime
from aiohttp import web, web_runner
# aiohttp是一个web框架
from jinja2 import Environment, FileSystemLoader
import orm
from coroweb import add_routes, add_static
from handlers import cookie2user, COOKIE_NAME
logging.basicConfig(level=logging.INFO)


# def index(request):
#     return web.Response(body=b'Awesome', content_type='text/html')
#
#
# @asyncio.coroutine
# def init():
#     app = web.Application()
#     app = web_runner.AppRunner(app=app).app()
#     app.router.add_route('GET', '/', index)
#     srv = yield from loop.create_server(app._make_handler(), '127.0.0.1', 9000)
#     logging.info('server started at http://127.0.0.1:9000...')
#     return srv
#
#
# loop = asyncio.get_event_loop()
# loop.run_until_complete(init())
# loop.run_forever()


def init_jinja2(app, **kw):
    logging.info('init jinja2...')
    options = dict(
        autoescape=kw.get('autoescape', True),
        block_start_string=kw.get('block_start_string', '{%'),
        block_end_string=kw.get('block_end_string', '%}'),
        variable_start_string=kw.get('variable_start_string', '{{'),
        variable_end_string=kw.get('variable_end_string', '}}'),
        auto_reload=kw.get('auto_reload', True)
    )
    path = kw.get('path', None)
    if path is None:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
    logging.info('set jinja2 template path: %s' % path)
    env = Environment(loader=FileSystemLoader(path), ** options)
    filter = kw.get('filters', None)
    if filter is not None:
        for name, f in filter.items():
            env.filters[name] = f
    app['__templating__'] = env


async def logger_factory(app, handler):
    """
    记录URL日志（通用功能，放在拦截器中）
    :param app:
    :param handler:
    :return:
    """
    async def logger(request):
        # 记录日志
        logging.info('Request: %s %s' % (request.method, request.path))
        # await asyncio.sleep(0.3）
        # 继续处理请求
        return await handler(request)
    return logger


async def data_factory(app, handler):
    async def parse_data(request):
        if request.method == 'POST':
            if request.content_type.startwith('application/json'):
                request.__data_ = await request.json()
                logging.info('request json: %s' % str(request.__data__))
            elif request.content_type.startwith('application/x-www-form-urlencoded'):
                request.__data__= await request.post()
                logging.info('request form: %s' % str(request.__data__))
        return (await handler(request))
    return parse_data


async def response_factory(app, handler):
    """
    将返回值转换为web.Response对象再返回（通用功能，放在拦截器中）
    :param app:
    :param handler:
    :return:
    """
    async def response(request):
        logging.info('Response handle...')
        r = await handler(request)  # 结果
        if isinstance(r, web.StreamResponse):
            return r
        if isinstance(r, bytes):
            resp = web.Response(body=r)
            resp.content_type = 'application/octet-stream'
            return resp
        if isinstance(r, str):
            if r.startswith('redirect:'):
                return web.HTTPFound[9:]
            resp = web.Response(body=r.encode('utf-8'))
            resp.content_type = 'text/html;charset=utf-8'
            return resp
        if isinstance(r, dict):
            template = r.get('__template__')
            if template is None:
                resp = web.Response(body=json.dumps(r, ensure_ascii=False, default=lambda o: o.__dict__).encode('utf-8'))
                resp.content_type = 'application/json;charset=utf-8'
                return resp
            else:
                resp = web.Response(body=app['__templating__'].get_template(template).render(**r).encode('utf-8'))
                resp.content_type = 'text/html;charset=utf-8'
                return resp
        if isinstance(r, int) and r >=100 and r <600:
            return web.Response
        if isinstance(r, tuple) and len(r) == 2:
            t, m = r
            if isinstance(t, int) and t >=100 and t < 600:
                return web.Response(t, str(m))
        # default:
        resp = web.Response(body=str(r).encode('utf-8'))
        resp.content_type = 'text/plain;charset=utf-8'
        return resp
    return response


@asyncio.coroutine
def auth_factory(app, handler):
    """
    解析cookie，并绑定用户到request对象（通用功能，放在拦截器中）
    :param app:
    :param handler:
    :return:
    """
    @asyncio.coroutine
    def auth(request):
        logging.info('check user: %s %s' % (request.method, request.path))
        request.__user__ = None
        cookie_str = request.cookies.get(COOKIE_NAME)
        if cookie_str:
            user = yield from cookie2user(cookie_str)
            if user:
                logging.info('set current user: %s' % user.email)
                request.__user__ = user
        if request.path.startswith('/manage/') and (request.__user__ is None or not request.__user__.admin):
            return web.HTTPFound('/signin')
        return (yield from handler(request))
    return auth


def datetime_filter(t):
    delta = int(time.time() - t)
    if delta < 60:
        return u'1分钟前'
    if delta < 3600:
        return u'%s分钟前' % (delta // 60)
    if delta < 86400:
        return u'%s小时前' % (delta // 3600)
    if delta < 604800:
        return u'%s天前' % (delta // 86400)
    dt = datetime.fromtimestamp(t)
    return u'%s年%s月%s日' % (dt.year, dt.month, dt.day)


async def init(loop):
    await orm.create_pool(loop=loop, host='127.0.0.1', port=3306, user='root', password='root', db='awesome')
    app = web.Application(loop=loop, middlewares=[logger_factory, auth_factory, response_factory])  # middlewares是一种拦截器
    init_jinja2(app, filters=dict(datetime=datetime_filter))
    add_routes(app, 'handlers')
    add_static(app)
    srv = await loop.create_server(app.make_handler(), '0.0.0.0', 9001)
    logging.info('server started at http://127.0.0.1:9000...')
    return srv

loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()
















