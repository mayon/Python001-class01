# Pandas 学习笔记

## 1. 常用 Web 框架

Python Web 框架设计均遵循 MVC 设计模式 .

- web.py
- Django Web
- Flask
- Tornado
- AIOHTTP
- FastAPI

## 2. Django 框架学习

- MTV 设计模式：
    - 模型（Model）
    - 模板（Template）
    - 视图（Views）

- Django 特点：
    - 采用了 MTV 的框架
    - 强调跨苏开发和代码复用 DRY （Do Not Repeat Yourself）
    - 组件丰富：
        - ORM（对象关系映射）映射类来构建数据模型
        - URL 支持正则表达式
        - 模板可继承
        - 内置用户认证，提供用户认证和权限功能
        - admin 管理系统
        - 内置表达模型、Cache 缓存系统、国际化系统等

- Django 安装：
    - 最新版本 3.0，版本不够稳定，目前使用最多的是 2.2.13（LTS）
    ```
    pip install --upgrade django==2.2.13
    >>> import django
    >>> django.__version__
    ```

## 3. 模块和包

- 模块和包：
    - 模块：.py 结尾的 Python 程序
    - 包：存放多个模块的目录
    - __init__.py：包运行的初始化文件，可以是空文件

- 常见以下几种方式导入：
    - import                    # 默认从 python site-packages 寻找 module
    - from . import **          # 从当前包导入 module
    - from .Pkg2 import **      # 从指定包 Pkg2 导入 module
    - from ** import **         # 导入 module 内的 func
    - from ** import ** as **   # 导入 module 内的 func 并重命名

## 4. Django 项目实战

- 创建项目
```
django-admin startproject MyDjango    # create project
cd MyDjango
python manage.py help                 # get django help info
python manage.py startapp index       # create index module
python manage.py runserver            # Starting Server http://127.0.0:8000/
```

- 启动项目：测试完成后，把代码运行模式关闭，以避免上传到云端后产生漏洞泄露
```
python manage.py migrate              # for error tips
# You have 17 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions.
# Run 'python manage.py migrate' to apply them.
python manage.py runserver            # default port: 127.0.0.1:8080
python manage.py runserver 0.0.0.0:80 # config port
CONTROL+C                             # quit the server
```

- 创建模块（APP）URLconf 说明：
    根据项目需求，注册独立模块 APP，以 douban 为例：`python manage.py startapp Douban`
    - http://ip/xxx
    - http://ip/douban/xxx
    - http://ip/douban/yyy

- 项目配置（setting.py）：
    - INSTALLED_APPS: 添加自己的 APP
    - DATABASES: 根据需求修改数据库配置

- urls.py : 
    - URL 调度器 : 
setting.py[ROOT_URLCONF] -> urlpatterns[路径匹配, 子应用路径urls] -> 子应用urls[匹配视图]
    - 带变量的 URL：
    str，int，slug，uuid，path
    path('<int:year>', views.myyear)

```
# ./index/urls.py
from django.urls import path, re_path, register_converter
from . import views
from . import converters

register_converter(converters.IntConverter, 'myint')
register_converter(converters.FourDigitYearConverter, 'yyyy')

urlpatterns = [
    path('', views.index),
    # path('<int:year>', views.year),
    path('<int:year>/<str:name>', views.name),
    re_path('(?P<year>[0-9]{4}).html', views.myyear, name='urlyear'),
    # path('<myint:year>', views.year),
    path('<yyyy:year>', views.year),
]
```

```
class IntConverter:
    regex = '[0-9]+'

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return str(value)

class FourDigitYearConverter:
    regex = '[0-9]{4}'

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return '%04d' % value
```

- view 视图快捷方式

默认从当前 APP 目录下，Templates 中寻找 template

  - HttpResponse(str)   
  - shortcuts:
    - render(request, template.html, ...) # return HttpResponse obj
    - redirect(url) # return HttpResponseRedirect obj
    - get_object_or_404() # 在给定的模型管理器（model Manager）上调用 get() ， 但它会引发 Http404 而不是模型的 DoesNotExist 异常

- 使用 ORM 创建数据表

每个模型都是一个 Pyhton 类，这些类继承 Django.db.models.Model
模型类的每个属性都相当于一个数据库的字段
利用这些，Django 提供了一个自动生成访问数据库的 API

  1. 在 models.py 中创建 Table, 一个 Table 对应 一个 Class

``
    from django.db import models

    # Create your models here.
    class Type(models.Model):
        # id = models.AutoField(primary_key=True)
        typename = models.CharField(max_length = 20)

    class Name(models.Model):
        name = models.CharField(max_length = 50)
        author = models.CharField(max_length = 50)
        stars = models.CharField(max_length = 5)
```

  2. 将 models.py 转化成数据表
    - python manage.py makemigrations   # 将 models.py 转成中间文件
    - python manage.py migrate          # 将中间文件转成 sql 文件

    ```
    $ > python manage.py makemigrations
    Migrations for 'index':
    index/migrations/0001_initial.py
        - Create model Name
        - Create model Type
    $ > python manage.py migrate
    Operations to perform:
    Apply all migrations: admin, auth, contenttypes, index, sessions
    Running migrations:
    Applying contenttypes.0001_initial... OK
    Applying auth.0001_initial... OK
    Applying admin.0001_initial... OK
    Applying admin.0002_logentry_remove_auto_add... OK
    Applying admin.0003_logentry_add_action_flag_choices... OK
    Applying contenttypes.0002_remove_content_type_name... OK
    Applying auth.0002_alter_permission_name_max_length... OK
    Applying auth.0003_alter_user_email_max_length... OK
    Applying auth.0004_alter_user_username_opts... OK
    Applying auth.0005_alter_user_last_login_null... OK
    Applying auth.0006_require_contenttypes_0002... OK
    Applying auth.0007_alter_validators_add_error_messages... OK
    Applying auth.0008_alter_user_username_max_length... OK
    Applying auth.0009_alter_user_last_name_max_length... OK
    Applying auth.0010_alter_group_name_max_length... OK
    Applying auth.0011_update_proxy_permissions... OK
    Applying index.0001_initial... OK
    Applying sessions.0001_initial... OK
```

  3. 错误汇总：
        1. `No module named MySQLDB`
        ```
        # add in ./MyDjango/__init__.py
        import pymysql
        pymysql.install_as_MySQLdb()
        ```

        2. `pymysql.err.InternalError: (1049, "Unknown database 'TestDjango'")`
        ```
        /usr/local/mysql/bin/mysql -u root -p
        mysql> create database TestDjango;
        ```

        3. `mysqlclient 1.3.13 or newer is required; you have 0.9.3.`
        ```
        # 方案1：/MyDjango/__init__.py
        import pymysql
        pymysql.version_info = (1, 4, 6, 'final', 0)  # change mysqlclient version
        pymysql.install_as_MySQLdb()
        ```
        ```
        # 方案2：
        点击 command 找到报错提示的文件，把相关的错误判断代码注释掉
        ```

        4. `AttributeError: 'str' object has no attribute 'decode'`
        这是 Python 早期版本产生的问题，在 Python3 里面不存在这个问题
        ```
        # /venvGeek/lib/python3.7/site-packages/django/db/backends/mysql/operations.py
        搜索 query 将 decode 修改成 encode
        ```
    
    4. ORM 常用 API
 
        - 进入 shell 环境： `python manage.py shell`

        - Create:
        ```
        >>> from index.models import *
        >>> n = Name() 
        >>> type(n)    # index.models.Name
        >>> n.name = 'hongloumeng' 
        >>> n.author='caoxueqin'
        >>> n.stars=9.6
        >>> n.save() 
        >>> Name.objects.create(name='hahahha',author='test author',stars=9.2) 
        ```
        - Read:
        ```
        >>> Name.objects.get(id=2).name
        ```
        - Update:
        ```
        >>> Name.objects.filter('name'='hongloumeng').update(name='stone')
        ```
        - Delete:
        ```
        >>> Name.objects.filter('name'='hongloumeng').delete()
        >>> Name.objects.all().delete()
        ```
        - Query:
        ```
        >>> Name.objects.values_list('name')
        >>> Name.objects.values_list('author').count()
        >>> Name.objects.values_list('name')[0]
        ```

    5. 反向创建 models
        - 如果数据库中数据表已经存在，可以通过命令反向创建 models.py 文件
        - 创建命令：
            - 默认输出到终端 `python manage.py inspectdb`
            - 输出重定向 `python manage.py inspectdb > models.py`

- Django 模板开发：

    1. 模板变量 {{ variables }}
    2. 从 URL 获取模板变量 {% url 'urlyear' 2020 %}
    3. 读取静态资源内容 {% static "css/header.css" %}
    4. for 遍历标签 {% for type in type_list %}{% endfor %}
    5. if 判断标签 {% if name.type == type.type %}{% endif %}