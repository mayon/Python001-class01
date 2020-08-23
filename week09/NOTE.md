# 学习笔记

## 1. Django 源码分析

#### URLConf

path()
re_path()
include()

def partial(func, *args, **kwargs):
    def newfunc(*fargs, **fkwargs):
        newkeywords = kwargs.copy()
        newkeywords = kwargs.update(fkwargs)
        return func(*args, *kargs, **newkeywords)
    return newfunc

isinstance(arg, (list, tuple))

#### View 

- 请求过程

request.py
class HttpRequest: 

用来处理同名参数的特殊 dict
class QueryDict: 

?id=1&id=2&value=3
```


只要有用户发起请求，modWSGI 会自动把我们的 HttpRequest 进行封装处理成对象，我们直接在 view 中接收  request 即可。

from django.http import HttpRequest
from djongo.http import HttpResponse

def index(request):
    print(request.GET)
    return HttpResponse('hello django')

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

查询管理器

def books_short(request):
    shorts = T1.objects.all()

- 如何让查询管理器的名称不叫做 objects
- 如何利用 Manager(objects) 实现对 Model 的 CRUD
- 为什么查询管理器返回 QuerySet 对象？

# site-packages/django/db/models/manager.py
class Manager(BaseManager.from_queryset(Queryset)):
    pass

Manager 继承自 BaseManagerFromQuerySet 类，拥有 QuerySet 的大部分方法，get，create，filter 等方法都来自 QuerySet

学习动态创建类

@classmethod
def from_queryset(cls, queryset_class, class_name=None):
    if class_name is None:
        class_name = '%sFrom%s' % (cls.__name__, queryset_class.__name__)
    return type(class_name, (cls,), {
        '_queryset_class': queryset_class,
        **cls._get_queryset_methods(queryset_class),
    })

#### 模板

/templates

模板引擎

- 模板引擎怎样通过 render() 加载 HTML 文件
- 模板引擎怎样对模板进行渲染

def books_short(request):
    return render(request, 'result.html', locals())

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

## 3. Django Web 常用组件

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

#### Auth 验证组件

- 在 view 中进行验证

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

- 注册 Auth 

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