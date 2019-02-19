#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/1/31 11:35
# @Author : Huang Qin
# @Description :  定义URL处理函数
# @usage :

import re, time, json, logging, hashlib, base64, asyncio
from coroweb import get, post
from models import Users, Blog, next_id
from apis import Page, APIError, APIValueError, APIResourceNotFoundError, APIPermissionError
from aiohttp import web
from config import configs

COOKIE_NAME = 'awesession'
_COOKIE_KEY = configs.session.secret

# 获取所有用户
# @get('/')
# async def index(request):
#     users = await Users.findAll()
#     return {
#         '__template__': 'test.html',
#         'users': users
#     }


# 获取所有blog
@get('/')
def index(request):
    summary = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'
    blogs = [
        Blog(id='1', name='Test Blog', summary=summary, created_at=time.time() - 120),
        Blog(id='2', name='Something New', summary=summary, created_at=time.time() - 3600),
        Blog(id='3', name='Learn Swift', summary=summary, created_at=time.time() - 7200)
    ]
    return {
        '__template__': 'blogs.html',
        'blogs': blogs
    }


# # 获取所有用户，按创建时间倒叙
# @get('/api/users')
# async def api_get_users(request):
#     users = await Users.findAll(orderBy='created_at desc')
#     for u in users:
#         u.passwd = '******'  # 密码显示为*
#     return dict(users=users)

# email和sha1规则：使用正则
_RE_EMAIL = re.compile(r'^[a-z0-9\.\-\_]+\@[a-z0-9\-\_]+(\.[a-z0-9\-\_]+){1,4}$')
_RE_SHA1 = re.compile(r'^[0-9a-f]{40}$')


# 跳转到注册页面
@get('/register')
def register():
    return {
        '__template__': 'register.html'
    }


# 跳转到登录页面
@get('/signin')
def signin():
    return {
        '__template__': 'signin.html'
    }


# 注册用户
@post('/api/users')
async def aip_register_user(*, email, name, passwd):
    # 参数校验
    if not name or not name.strip():
        raise APIValueError('name')
    if not email or not _RE_EMAIL.match(email):
        raise APIValueError('email')
    if not passwd or not _RE_SHA1.match(passwd):
        raise APIValueError('passwd')
    # 验证数据库中是否已存在此email
    users = await Users.findAll('email=?', [email])
    if len(users) > 0:  # 数据库中已存在
        raise APIError('register:failed', 'email', 'Email is already in use.')
    uid = next_id()  # 自动生成user id
    # 用户口令：经过SHA1计算后的40位Hash字符串
    sha1_passwd = '%s:%s' % (uid, passwd)
    # 封装Users对象
    user = Users(id=uid, name=name.strip(), email=email,
                 passwd=hashlib.sha1(sha1_passwd.encode('utf-8')).hexdigest(),
                 image='http://www.gravatar.com/avatar/%s?d=mm&s=120' % hashlib.md5(email.encode('utf-8')).hexdigest())
    await user.save()  # 存入数据库（注册成功）
    # make session cookie:
    r = web.Response()
    r.set_cookie(COOKIE_NAME, user2cookie(user, 86400), max_age=86400, httponly=True)
    user.passwd = '******'
    r.content_type = 'application/json'
    r.body = json.dumps(user, ensure_ascii=False).encode('utf-8')
    return r


# 用户登录（认证）
@post('/api/authenticate')
async def authenticate(*, email, passwd):
    # 参数校验
    if not email:
        raise APIValueError('email', 'Invalid email.')
    if not passwd:
        raise APIValueError('passwd', 'Invalid password.')
    # 根据email查询user
    users = await Users.findAll('email=?', [email])
    if len(users) == 0:  # 数据库中不存在
        raise APIValueError('email', 'Email not exist.')
    user = users[0]  # 数据中存储的user
    # check passwd:（userid:passwd）
    sha1 = hashlib.sha1()
    sha1.update(user.id.encode('utf-8'))
    sha1.update(b':')
    sha1.update(passwd.encode('utf-8'))
    if user.passwd != sha1.hexdigest():  # 数据库存的passwd和sha1生成的passwd不同
        raise APIValueError('passwd', 'Invalid password.')
    # authenticate ok, set cookie:
    r = web.Response()
    r.set_cookie(COOKIE_NAME, user2cookie(user, 86400), max_age=86400, httponly=True)
    user.passwd = '******'
    r.content_type = 'application/json'
    r.body = json.dumps(user, ensure_ascii=False).encode('utf-8')
    return r


# 登出（退出）
@get('/signout')
def signout(request):
    referer = request.headers.get('Referer')
    r = web.HTTPFound(referer or '/')
    r.set_cookie(COOKIE_NAME, '-deleted-', max_age=0, httponly=True)
    logging.info('user signed out.')
    return r


# 计算加密cookie
def user2cookie(user, max_age):
    """
    Generate cookie str by user.
    :param user:
    :param max_age:
    :return:
    """
    # build cookie string by: id-expires-sha1
    expires = str(int(time.time()) + max_age)
    # cookie: "用户id" - "过期时间" - SHA1
    s = '%s-%s-%s-%s' % (user.id, user.passwd, expires, _COOKIE_KEY)  # "用户id" - "用户口令" - "过期时间" - "SecretKey"
    L = [user.id, expires, hashlib.sha1(s.encode('utf-8')).hexdigest()]
    return '-'.join(L)


# 解密cookie
@asyncio.coroutine
def cookie2user(cookie_str):
    """
    Parse cookie and load user if cookie is valid.
    :param cookie_str:
    :return:
    """
    if not cookie_str:
        return None
    try:
        L = cookie_str.split('-')  # 正确的格式："用户id" - "过期时间" - SHA1
        if len(L) != 3:
            return None
        uid, expires, sha1 = L
        if int(expires) < time.time():  # 已过期
            return None
        user = yield from Users.find(uid)
        if user is None:  # 数据库中不存在此用户
            return None
        s = '%s-%s-%s-%s' % (uid, user.passwd, expires, _COOKIE_KEY)
        if sha1 != hashlib.sha1(s.encode('utf-8')).hexdigest():  # 密码不一致
            logging.info('invalid sha1')
            return None
        user.passwd = '******'
        return user
    except Exception as e:
        logging.exception(e)
        return None


# 验证权限
def check_admin(request):
    if request.__user__ is None or not request.__user__.admin:
        raise APIPermissionError()


# 跳转到创建Blog页面
@get('/manage/blogs/create')
def manage_create_blog():
    return {
        '__template__': 'manage_blog_edit.html',
        'id': '',
        'action': '/api/blogs'
    }


# 分页显示blogs
@get('/api/blogs')
async def api_blogs(*, page='1'):
    page_index = get_page_index(page)  # 第几页
    num = await Blog.findNumber('count(id)')  # blog总条数
    p = Page(num, page_index)  # 获取Page对象
    if num == 0:
        return dict(page=p, blogs=())
    blogs = await Blog.findAll(orderBy='created_at desc', limit=(p.offset, p.limit))
    return dict(page=p, blogs=blogs)


# 管理页面
@get('/manage/blogs')
def manage_blogs(*, page='1'):
    return {
        '__template__': 'manage_blogs.html',
        'page_index': get_page_index(page)
    }


# 创建Blog
@post('/api/blogs')
async def api_create_blog(request, *, name, summary, content):
    check_admin(request)  # 验证权限
    # 参数校验
    if not name or not name.strip():
        raise APIValueError('name', 'name cannot be empty.')
    if not summary or not summary.strip():
        raise APIValueError('summary', 'summary cannot be empty.')
    if not content or not content.strip():
        raise APIValueError()
    # 封装Blog对象
    blog = Blog(user_id=request.__user__.id, user_name=request.__user__.name, user_image=request.__user__.image,
                name=name.strip(), summary=summary.strip(), content=content.strip())
    # 保存到数据库
    await blog.save()
    return blog


# 根据id获取Blog
@get('/api/blogs/{id}')
async def api_get_blog(*, id):
    blog = await Blog.find(id)
    return blog


def get_page_index(page_str):
    p = 1
    try:
        p = int(page_str)
    except ValueError as e:
        pass
    if p < 1:
        p = 1
    return p
