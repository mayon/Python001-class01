# 学习笔记

## 1. Django 源码分析

#### URLConf

path()
re_path()
include()

```
def partial(func, *args, **kwargs):
    def newfunc(*fargs, **fkwargs):
        newkeywords = kwargs.copy()
        newkeywords = kwargs.update(fkwargs)
        return func(*args, *kargs, **newkeywords)
    return newfunc
```

isinstance(arg, (list, tuple))

#### View 

- 请求过程

request.py
class HttpRequest: 

用来处理同名参数的特殊 dict
class QueryDict: 

?id=1&id=2&value=3


只要有用户发起请求，modWSGI 会自动把我们的 HttpRequest 进行封装处理成对象，我们直接在 view 中接收  request 即可。
```
from django.http import HttpRequest
from djongo.http import HttpResponse

def index(request):
    print(request.GET)
    return HttpResponse('hello django')
```
- 返回过程

view 视图的返回结果

response.py
class HttpResponse:

```
from django.http import HttpResponse
from django.http import JsonResponse
from django.http import HttpResponseNotFound

def test1(request):
    response1 = HttpResponse()
    response2 = HttpResponse('any text', content_type='text/plain')

    response3 = JsonResponse({ 'foo': 'bar' })
    response3['Age'] = 120

    response4 = HttpResponseNotFount('<h1>Page not fount</h1>)
    return response4
```

modwsgi 协议：

接收 Http 的请求，再把 Http 的请求转到 WSGI 的请求上。
Django 初始化时会初始化一个实例 WSGIHandler , 用来监听请求和响应的一个完成，请求来了，就会自动初始化一个 Request 的对象，

class WSGIHandler # manage.py 中

默认 Request 使用 Get 方式请求，如果是使用 Post 方式请求，不包含上传文件的数据，
Django 会把文件数据放在 _files 属性中，并且只有当 content_type = 'multipart/form-data' 的时候才会有数据。

返回是我们自己在 views.py 中手写的 Response。

#### Models

models.py

为什么自定义的 Model 要继承 models.Model

- 不需要显示定义主键
- 自动拥有查询管理器对象
- 可以使用 ORM API 对数据库、表实现 CRUD

```
class Model:
    pass

class T1(models.Model):
    #id 自动创建
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50)
    short = models.IntegerField()
    senttiment = models.FloatField()

    class Meta:
        managed = False 
        db+table = 't1'
```

查询管理器

```
def books_short(request):
    shorts = T1.objects.all()
```

- 如何让查询管理器的名称不叫做 objects
- 如何利用 Manager(objects) 实现对 Model 的 CRUD
- 为什么查询管理器返回 QuerySet 对象？

```
# site-packages/django/db/models/manager.py
class Manager(BaseManager.from_queryset(Queryset)):
    pass
```
Manager 继承自 BaseManagerFromQuerySet 类，拥有 QuerySet 的大部分方法，get，create，filter 等方法都来自 QuerySet

学习动态创建类

```
@classmethod
def from_queryset(cls, queryset_class, class_name=None):
    if class_name is None:
        class_name = '%sFrom%s' % (cls.__name__, queryset_class.__name__)
    return type(class_name, (cls,), {
        '_queryset_class': queryset_class,
        **cls._get_queryset_methods(queryset_class),
    })
```

#### 模板

/templates

模板引擎

- 模板引擎怎样通过 render() 加载 HTML 文件
- 模板引擎怎样对模板进行渲染

```
def books_short(request):
    return render(request, 'result.html', locals())
```

django/template/**.py
- shortcuts.py # 模板解析
- loader.py # 模板导入
- engine.py # 模板引擎导入
- base.py  # 模板渲染类 Template

## 2. Django 管理页面

管理页面的设计哲学：

- 管理后台是一项缺乏创造性和乏味的工作，Django 全自动地根据模型创建后台界面。
- 管理界面不是为了网站的访问者，而是为管理者准备的。

操作步骤：

1. 增加管理后台模型：

```
# ./index/admin.py
from .models import Type, Name

admin.site.register(Type)
admin.site.register(Name)
```

2. 创建管理员账号：
python manage.py createsuperuser

3. 访问管理后台：
http://127.0.0.1:8000/admin

## 3. Django Web 表单

- 表单和 csrf 防护

默认对全站的 post 请求进行防护

```
# setting.py
'django.middleware.csrf.CsrfViewMiddleware',
```

- 只对指定的 views 进行 csrf 防护

```
# setting.py 
# 'django.middleware.csrf.CsrfViewMiddleware', 注释掉 setting 中的配置，只对加了装饰器的 view 进行 CSRF 防护
# views.py
from django.views.decorators.csrf import csrf_exempt, csrf_protect

@csrf_exempt
def result(request):
    return render(request, 'result.html')
```

只对 post 请求进行了防护

## 4. Django Web Auth 用户组件

1. 在 view 中进行验证

```
# views.py
def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            cd = login_form.cleaned_data
            user = authenticate(name=cd['username'], password=cd['password'])
            if user:
                login(request, user)             # loginout(request, user)
                return HttpResponse('登录成功')
            else:
                return HttpResponse('登录失败')
```

2. 注册 Auth 

```
$ python manage.py shell
# 创建用户
>>> from django.contrib.auth.models import User
>>> user = User.objects.create_user('jerry', 'jerry@jerry.com', 'jerrypassword')
>>> user.save()
# 验证用户
>>> from django.contrib.auth import authenticat
>>> authenticate(username='jerry',password='jerrypassword')
<<< <User: jerry>
```

## 5. Django Web 信号机制

信号：

- 发生事件，通知应用程序
- 支持若干信号发送者通知一组接受者
- 解耦
- 内建信号：docs.djangoproject.com/zh-hans/2.2/ref/signals/

创建信号：

```
# views.py
# Type1
def my_callback1(sender, **kwargs):
    print('Request started!')
from django.core.signals import request_started
request_started.connect(my_callback1)

# Type2
from django.core.signals import request_finished
from django.dispatch import receiver

@receiver(request_finished)
def my_callback2(sender, **kwargs):
    print('Request finished')
```

## 6. Django Web 中间件

Django Middleware 的作用：

- 全局改变输入或输出
- 轻量级的、低级的 “插件” 系统
- 对请求、响应处理的钩子框架

Middleware 编写流程：

1. 编写 Middleware，在 middleware.py 中
2. 注册 Middleware，在 setting.py 中

注意注册顺序，最上面的最先执行，要根据中间件的功能来进行排序

## 7. Django 生产环境部署

本地运行 Django 时，底层产生的 HTTPRequest 叫做 WSGIHandler，遵循 WSGI 协议。

用户请求用的是 http 协议，本地采取的是模拟 http 协议，但是，模拟功能在有大量用户发出请求时，会产生阻塞。

需要把模拟转成正式功能，我们需要使用转换器来进行转化。

- Apache（已淘汰）
- Nginx（用的最普遍）
- Gunicon（性能最好）:green unix con
- Tornado（既可以用作 Web 框架，也可以用作 HTTP 服务器）：收到用户请求后，通过 WSGI 协议转给 Django

Gunicon + Django:

```
# 安装 gunicorn
pip install gunicorn

# 在项目目录执行
gunicorn MyDjango.wsgi
```

Gunicon 常用配置选项:

```
gunicorn --h

# 生产环境中，需要将 8000 改为实际需要的端口，通常为 80
# 127.0.0.1 为本机才能访问，需要改成 0.0.0.0，所有用户都能访问
  -b ADDRESS, --bind ADDRESS
                        The socket to bind. [['127.0.0.1:8000']]
# 如果服务器性能很好，可以指定多进程的数量，可以跟 CPU 核数相等
  -w INT, --workers INT
                        The number of worker processes for handling requests.
# 日志参数
  --access-logfile FILE
                        The Access log file to write to. [None]
  --disable-redirect-access-to-syslog
                        Disable redirect access logs to syslog. [False]
  --access-logformat STRING
                        The access log format. [%(h)s %(l)s %(u)s %(t)s
                        "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"]
  --error-logfile FILE, --log-file FILE
                        The Error log file to write to. [-]
  --log-level LEVEL     The granularity of Error log outputs. [info]   # 从 info 改成 debug

```

## 8. Django 定时任务 Celery - 分布式消息队列

**Celery 使用方法：**

1. **安装 Redis 依赖（用于存储）**

    1. 下载安装包：https://redis.io/

    2. 解压安装包 redis-6.0.6.tar.gz

    3. 进入解压后安装包：包内有可编译文件 Makefile，使用下面命令进行编译
    ```
    >>> make install
    ```
    4. redis.conf 发布前必须修改配置项
    ```
    daemonize no       # 如果是正式环境，即非调试环境，需要改成 yes，让它变成守护进程
    bind 127.0.0.1     # 如果发布，需要改成 0.0.0.0 允许所有人访问
    requirepass 123456 # 发布前，需要设置访问密码
    ```
    5. 启动 Redis 服务：复制 redis.conf 到项目根目录，也可以放在其他目录，启动时加上 path 即可
    ```
    >>> redis-server redis.conf
    ```

2. **安装 Celery**

```
pip install celery
pip install redis==2.10.6    # python 版本 redis 驱动
pip install celery-with-redis
pip install django-celery    # 关联 Django 和 Celery
```

> 版本兼容问题
> python 3.7 之后，async 成为保留关键字，如果用包含该关键字的方法或模块就会报错。
> 很多其他的包也会有这个问题，遇到类似问题要么将 python 降级，要么就是手动修改这些依赖包。

上述 Celery 相关软件包下载完成后会有一个 kombu 包，里面包含 async 模块，该模块需要改名后才能正常引用。

3. **添加 APP**
```
django-admin startproject MyDjango
python manager.py startapp djcron

# setting.py
INSTALL_APPS=[
    'djcelery',
    'djcron'
]
```

4. **迁移生成表**
```
python manage.py migrate
```

5. **配置 Django 时区**
```
from celery.schedules import crontab
from celery.schedules import timedelta
import djcelery
djcelery.setup_loader()
BROKER_URL = 'redis://:123456@127.0.0.1:6379/'    # 代理人
CELERY_IMPORTS = ('djcron.tasks')   # app
CELERY_TIMEZONE = 'Asia/Shanghai'   # 时区
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'   # 定时任务调度器
```

6. **在 MyDjango 下建立 Celery.py**
```
import os
form celery import Celery, platforms
from django.conf import settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE','MyDjango.settings')
app = Celery('MyDjango')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
platforms.C_FORCE_ROOT = True
```

7. **在 __init__.py 增加**
```
# 使用绝对引入，后续使用 import 引入会忽略当前目录下的包
from __future__ import absolute_import
from .celery import app as celery_app
```

8. **添加的当时任务 Celery**
```
# task.py
from MyDjango.celery import app

@app.task()
def task1():
    return 'test1'
@app.task()
def task2():
    return 'test2'
```

9. **启动定时任务**
```
>>> celery -A MyDjango beat -l info
>>> celery -A MyDjango worker -l info
```

10. **也可以通过 admin 增加定时任务**

## 9. Flask 框架解析

可插拔框架，微型 Web 框架。

只包含两个核心功能：
1. WSGI 协议的实现：使用 Werkzeug 工具
2. Jinjia 模板解析引擎

需要什么功能，就去寻找 Flask 对应扩展插件即可：
1. ORM：Flask-Alchemy
2. RestfulAPI：Flask Rest API

两种运行方法：（运行后修改源文件无变化，不能热修复）
```
# 1
>>> python flask_request_ctx.py
# 2
>>> export FLASK_APP=flask_request_ctx.py
>>> flask run
```

上下文：request 上下文与 session 上下文
```
from flask import Flask, Request
from flask.globals import _request_ctx_stack

app = Flask(__name__)

@app.route('/')
def index():
    ctx = _request_ctx_stack.top
    print(ctx)
    print(ctx.request.method)
    return 'index'

if __name__ == '__main__':
    app.run()

# <RequestContext 'http://127.0.0.1:5000/' [GET] of flask_request_ctx>
# GET
```

信号： Flask 从 0，6 开始，通过 Blinker 提供了信号支持

```
from flask import Flask
from flask import signals

app = Flask(__name__)

def func1(*argv):
    print('func1')

signals.request_started.connect(func1)

@app.route('/')
def func():
    print('View Function')
    return 'ok'

if __name__ == '__main__':
    app.run()
```

## 10. 其他常用框架

- 底层框架：(熟悉以下其中一个底层框架的原理)
    - Tornado：Web 框架和 HTTP 服务器，支持异步，兼容性最好，队列分片操作，只有有一个操作出错就会挂掉
    - Twisted：并发框架，python 事件驱动框架，稳定性最好，Scrapy 测试框架
    - Gevent：代码易维护

- Web 框架：（需要熟练掌握的两个框架）
    - Django
    - Flask
