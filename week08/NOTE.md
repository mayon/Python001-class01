# 学习笔记

## 1. 数据类型

##### 可变数据类型

list、dict、collections.deque

##### 不可变数据类型
int、float、string、tuple

改变不可变数据类型，id() 值会发生变化；改变可变数据类型中的值，id() 值不会发生变化

## 2. 序列

##### 容器序列

list、tuple、collections.deque, dict 等，能存放不同类型的数据.

```
import copy
copy.copy(object)       # 深拷贝：把所有的值都拷贝出来，并且重新申请了一块内存
copy.deepcopy(object)   # 浅拷贝：只是复制了引用地址，指向的还是原有的内存空间
```

说明：非容器类型没有拷贝问题

##### 扁平序列

str、bytes、bytearray、memoryview（内存视图）、array.array 等，存放的是相同类型的数据，即只能容纳一种类型

## 3. 字典与扩展内置数据类型

对集合 {a,b,c,d,e,f} 进行散列的图形化表示，其中关系 R 被称为散列函数 hash 。

字典的 key 必须是非空的不可变数据类型。

```
a - b         # a.__sub__(b), 操作符重载
a == b        # a.__eq__(b)
```

## 4. 变量作用域（命名空间）

##### 高级语言对变量的使用：

- 变量声明
- 定义类型（分配内存空间大小）
- 初始化（赋值、填充内存）
- 引用（通过对象名称调用对象内存数据）

Python 只有在模块、类、函数中定义，才有作用域的概念，这一点跟 Javascript 类似。

`Type Hint` 用于类型提示，但不会进行类型检查，只是一种书写上的约定。

##### Python 作用域遵循 LEGB 规则

- L-Local（function）：函数内的名字空间
- E-Enclosing function locals：外部嵌套函数的名字空间（例如 closure）
- G-Global(module)：函数定义所在模块（文件）的名字空间
- B-Builtin(Python)；Python 内置模块的名字空间

`dir(__builtins__)`  用于查看全局变量或函数

##### 作用域提升标识符

内部函数默认可以访问外部函数定义的变量，但如果对该变量进行修改，将自动转变成内部的局部变量；

如果要将修改作用到外部变量中，可以使用作用域提升标识符，提高内部变量的作用域。

`nonlocal:` 访问外部函数的局部变量
```
def counter(start = 0):
    def incr():
        nonlocal start
        start += 1
        return start
    return incr
c = counter(100)
c()
```

`global:` 访问全局变量

```
a = 100
def func():
    global a
    a += 100
```

## 5. 可变长参数函数

默认按顺序传递参数，如果要给函数指定某个参数，需要按照 key=value 形式赋值。

可变参数要放到参数列表的最后，位置参数放到参数列表的前面，位置可变参数需要放在关键字可变参数之前。

kwargs会截获所有的关键字参数，就算在调用函数时的形参中有类似x = 5形式的传参，形参x也不能得到该值.

def func(*args, **kargs):
    print(f'args: {args}')       # 获取常规序列参数
    print(f'kargs: {kargs}')     # 获取所有 key=value 形式参数

参数列表中的参数的一般顺序是：普通参数、缺省参数、可变位置参数、keyword-only参数（可带缺省值）、可变关键字参数。如下：

```
def fn(x, y, z=3, *arg, m=4, n, **kwargs):
    print(x,y,z,m,n)
    print(args)
    print(kwargs)
```

#### keyword-only参数

keyword-only参数是在 Python3 中加入的。如果在一个星号参数后，或者一个位置可变参数后，出现普通参数，那么这个参数就为 keyword-only 参数。

```
def fn(*args, x):
    print(x)
    print(args)
fn(3,5)
fn(3,5,7)
fn(3,5,x=7)
```

keyword-only参数另一种形式：*号之后跟普通形参，示例如下：

```
def fn(*, x,y):
    print(x,y)
fn(x=5,y=6)

```

#### 函数参数解构

参数解构时，非字典类型的实参使用*解构成位置参数；

字典类型使用**解构成关键字参数。

注意：提取出来的元素数目要和参数的要求匹配，也要和参数的类型匹配。


#### 偏函数

functools.partial: 返回一个可调用的 partial 对象
可以指定部分默认参数，不用每次都传全部参数

使用方法：partial(func, *args, **kw)

注意：
func 是必须参数
至少需要一个 args 或 kw 参数

#### Lambda 表达式

Lambda 只是表达式，不是所有的函数逻辑都能封装进去

k = lambda x:x+1
print(k(1))

Lambda 表达式后面只能有一个表达式

- 实现简单函数的时候可以使用 Lambda 表达式替代
- 使用高阶函数的时候一般使用 Lambda 表达式

#### 高阶函数

高阶：参数是函数、返回值是函数

常见的高阶函数：map、reduce、filter、apply

apply 在 Python 2.3 中被移除，reduce 被放在 functools 包中

推导式和生成器表达式可以被替代为 Lambda 表达式

m = map(square, range(10))     # 迭代器
next(m)
list(m)
dir(m)

[square(x) for x in range(10)]  # 推导式

工作中最常用到的两个官方函数标准库

import itertools
import functools

#### 函数返回值

return: 返回某个值，函数运行结束
yield: 返回生成器，函数状态保留

- 编译后函数体保存的「局部变量」
print(my_line.__code__.co_varnames)  
- 编译后函数体保存的「自由变量」（也叫「外部变量」简单理解为闭包环境变量）
print(my_line.__code__.co_freevars)
- 编译后函数体保存的「自由变量」第一个值
print(my_line.__closure__[0].cell_contents)

```
# 查看函数或对象的所有属性（魔术方法）
def func():
    pass
func_magic = dir(func)

class ClassA(object):
    pass
obj = ClassA()
obj_magic = dir(obj)

set(func_magic) - set(obj_magic)
```

## 6. 函数装饰器


PEP 318 引入装饰器
PEP 3129 引入类装饰器  (Python 2.6+ )

无参数函数

对函数进行包装

装饰器被使用时会自动运行，如果以模块形式导入，装饰器在模块导入时会自动运行,。

好处：

增强而不改变原有函数
装饰器强调函数的定义态而不是运行态

#### 装饰器语法糖：

```
def decorate(func):
    print('running in module')
    def inner():
        return func()
    return inner

@decorate
def target():
    print('do something')

# 等同于
def target():
    print('do something')
target = decorate(target)
```

new = func 体现 “一切皆对象”，函数也可以被当做对象进行复制

被装饰函数：状态不同，装饰器的处理也不同

#### 被修饰函数带参数

- 函数 __name__ 会被替换成 inner 函数的 __name__

```
def outer(func):
    def inner(a, b):
        print(f'inner: {func.__name__}')
        print(a, b)
        func(a, b)
    return inner

@outer
def foo(a, b):
    print(a + b)
    print(f'foo: {foo.__name__}')

foo(1, 2)
```

输出：
```
inner: foo
1 2
3
foo: inner
```

#### 被修饰函数带不定长参数

#### 被修饰函数带返回值

```
def outer3(func):
    def inner3(*args, **kwargs):
        ret = func(*args, **kwargs)
        return ret
    return inner3

@outer3
def foo3(a,b,c):
    return (a+b+c)
```

#### 让装饰器本身带参数

```
def outer_arg(bar):
    print('exe in outer_arg')
    def outer(func):
        print('exe in outer')
        def inner(*args, **kwargs):
            ret = func(*args, **kwargs)
            print(bar)
            return ret
        return inner
    return outer

@outer_arg('foo_arg')
def foo(a, b, c):
    return (a+b+c)

foo(1,2,3)
```

#### 装饰器的堆叠

可以无限制增加装饰器。

执行顺序：装饰器从下往上依次执行

```
@classmethod
@synchronized(lock)
def foo(cls):
    pass

def foo(cls):
    pass
foo = synchronized(lock)(foo)
foo = classmethod(foo)
```

Demo

```
def html(func):
    print('exe in html')
    def decorator():
        return f'<html>{func()}</html>'
    return decorator

def body(func):
    print('exe in body')
    def decorator():
        return f'<body>{func()}</body>'
    return decorator

@html
@body
def content():
    return 'hello world'

content()

# exe in body
# exe in html
# '<html><body>hello world</body></html>'
```

#### 用函数装饰类

```
def decorator(aClass):
    class newClass(object):
        def __init__(self, args):
            self.times = 0
            self.wrapped = aClass(args)
        # 重载 display 方法
        def display(self):
            self.times += 1
            print("run times", self.times)
            self.wrapped.display()
    return newClass

@decorator
class MyClass(object):
    def __init__(self, number):
        self.number = number
    def display(self):
        print('number is ', self.number)
    
six = MyClass(6)
for i in range(6):
    six.display()

# run times 1
# number is  2
# run times 2
# number is  2
```

#### 内置装饰方法函数

functools.wraps
@wraps 接受一个函数来进行装饰
加入了复制函数名称、注释文档、参数列表等等的功能
在装饰器里面可以访问在装饰之前的函数的属性,
(如让函数的名字不被改变，等等)
@functools.wraps(wrapped, assigned=WRAPPER_ASSIGNMENTS, updated=WRAPPER_UPDATES)
用于在定义包装器函数时发起调用 update_wrapper() 作为函数装饰器
它等价于 partial(update_wrapper, wrapped=wrapped, assigned=assigned, updated=updated)

```
from functools import wraps

# 登录验证
def requires_auth(func):
    @wraps(func)
    def auth_method(*args, **kwargs):
        if not auth:
            authenticate()
        return func(*args, **kwargs)
    return auth_method

@requires_auth
def func_demo():
    pass
```

可以使用 wrapt 包替代 @wraps
https://wrapt.readthedocs.io/en/lastest/quick-start.html
@wrapt.decorator
def wrapper(func, instance, args, kwargs)
目前已经很少用，都用 @wraps 取代，部分古老框架中仍存在这种写法

```
import wrapt

def with_arguments(myarg1, myarg2):
    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs):
        return wrapped(*args, **kwargs)
    return wrapper

@with_arguments(1, 2)
def function():
    pass
```

为相同函数返回值添加缓存
functools.lru_cache(maxsize=128, typed=False)
缓存值超过 maxsize 内存大小后，结果就会被释放
typed 若为 True，则会把不同的参数类型得到的结果分开保存
```
import functools
@functools.lru_cache()
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

if __name__ == '__main__':
    import timeit
    print(timeit.timeit("fibonacci(6)", setup="from __main__ import fibonacci"))
```
（每次时间都会有细微差异）
加cache：0.06717796199973236
不加cache：4.0080318110003645



下面两个库中包含大量常用的装饰器工具：
functools
itertools
collections # 包含大量数据类型

## 7. 类装饰器

#### 带参数的类装饰器
```
class MyClass(object):
    def __init__(self, var='init_var', *args, **kwargs):   # 1. 传参方式不同
        self._v = var
        super(MyClass, self).__init__(*args, **kwargs)
    
    def __call__(self, func):                              # 2. 必须添加该方法
        @wraps(func)                                       # 3. 可以用该装饰器，保证外部 func 内部属性不变
        def wrapped_function(*args, **kwargs):
            func_name = func.__name__ + ' was called'
            print(func_name)
            return func(*args, **kwargs)
        return wrapped_function

@MyClass(100)
def myfunc():
    pass

myfunc()

# MyClass(100)(myfunc)()
```

#### 不带参数的类装饰器
```
class Count(object):
    def __init__(self, func):
        self._func = func
        self.num_calls = 0
    def __call__(self, *args, **kwargs):
        self.num_calls += 1
        print(f'num of call is {self.num_calls}')
        return self._func(*args, **kwargs)

@Count
def example():
    print('hello')

example()
print(type(example))
```

经常在类装饰器中使用的 python 自带装饰器：

wraps(func)
classmethod
staticmethod
property


新引入的内部类装饰器 dataclasses.dataclass

```
from dataclasses import dataclass
@dataclass
class MyClass(object):
    var_a: str
    var_b: str

var_1 = MyClass('x','y')
var_2 = MyClass('x','y')

var_1 == var_2

# var_a 和 var_b 不能作为类属性访问，只能作为实例属性
```

旧写法对比：

```
class MyClass(object):
    def __init__(self, var_a, var_b):
        self.var_a = var_a
        self.var_b = var_b
    def __eq__(self, other):
        if self.__class__ is not other.__class__:
            return false
        return (self.var_a, self.var_b) == (other.var_a, other.var_b)
```

## 8. 对象协议（也叫“鸭子类型”）

使用者用起来跟常规数据类型一样使用我们的类，不需要特别备注写文档。

常用的魔术方法如下：

容器类型协议

`__str__` 打印对象时，默认输出该方法的返回值，用于人阅读的字符串形式
`__repr__` 也是字符串，但是遵循原有的内容形式, 程序之间传递字符串时用该方法
`__getitem__`、`__setitem__`、`__delitem__` 字典索引操作
`__iter__` 迭代器, 可以单独使用，返回一个迭代对象，也可以跟 `__next__` 进行组合，在 `__next__` 中返回每次迭代后的值
`__call__` 可调用对象协议

比较大小的协议

`__eq__`
`__gt__`

描述符协议和属性交互协议

`__get__`
`__set__`

可哈希对象

`__hash__`

上下文管理器

with 上下文表达式的用法
`__enter__()`、`__exit__()` 实现上下文管理器

格式化输出的几种不同方式
...

typing 类型注解（TypeHint）

与鸭子类型相反的是静态类型，声明变量的时候就要指定类型，如果使用其他类型对变量赋值就会报错.

```
def func(text: str, number: int) -> str:
    return text * number
func(123, 5)
```

它只是类型注解和提示，即使传参写错类型，也不会报错。

多种字符串模板：

```
firstname = 'yin'
lastname = 'wilson'
print('hello, %s %s.' % (firstname, lastname))
print('hello, {1} {0} {other}.'.format(firstname, lastname, other='test'))
print(f'hello, {firstname} {lastname} f.')
```

## 9. 生成器(generator) 和迭代协议

yield 生成器

1. 在函数中使用 yield 关键字，可以实现生成器。
2. 生成器可以让函数返回可迭代对象。
3. yield 和 return 不同，return 返回后，函数状态终止，yield 保持函数的执行状态。返回后，函数回到之前保存的状态继续执行。
4. 函数被 yield 会暂停，局部变量也会被保存。
5. 迭代器终止时，会抛出 StopIteration 异常。

通过列表式获取创建生成器

`[i for i in range(0, 11)]   # 迭代器

替换成

`(i for i in range(0, 11))   # 生成器`

```
gene = (i for i in range(0, 11))
for i in gene:
    print(i)
# next(gene)
```

迭代器协议：

Iterables(可迭代): 包含 `__getitem__()` 或 `__iter__()` 方法的容器对象

Iterator(迭代器): 包含 `__next__()` 和 `__iter__()` 方法, 分别是 next() 和 iter() 的魔术方法

Generator(生成器): 包含 yield 语句的函数, 实现了完整的迭代器协议.

只要一个函数的定义中出现了 yield 关键词，则此函数将不再是一个函数，而成为一个 ”生成器构造函数“，调用此构造函数即可产生一个生成器对象。

```
def func():
    yield 0
type(func())  # generator
```

## 10. Python 中迭代器的特性和限制

```
import itertools

# 无限迭代器
count = itertools.count()
cyle = itertools.cycle( ('yes', 'no') )
repeat = itertools.repeat(10, times=2)

# 有限迭代器
for j in itertools.chain( 'ABC', [1, 2, 3] ):
    print(j)

# yield from 
# Python 3.3 引入, PEP-380
def chain2(*iterables):
    for i in iterables:
        yield from i   # 替代内层循环
list(chain2('ABC', [1, 2, 3]))
#['A', 'B', 'C', 1, 2, 3]
```

迭代器的限制：

字典迭代器，如果对原字典进行插入操作，字典迭代器会立即失效；
列表迭代器，尾插入操作不会损坏指向当前元素的 List 迭代器，列表会自动变长;
修改已有属性值，均不会产生影响。
迭代器一旦耗尽，永久损坏，返回 StopIterations 错误。

## 11. yield 表达式

可以利用 next()  和  send() 操控 yield 表达式

```
def jumping_range(up_to):
    index = 0
    while index < up_to:
        jump = yield index
        print(f'jump is {jump}')
        if jump is None:
            jump = 1
        index += jump
        print(f'index is {index}')

if __name__ == '__main__':
    iterator = jumping_range(6)
    print(next(iterator))        # 第一次通信停留在 yield index，得到返回值 0
    print(iterator.send(2))
    print(iterator.send(-1))
    for x in iterator:
        print(x)
```

## 12. 协程

协程类似于前端开发中 JS 的事件循环机制。

#### 协程和线程的区别：

协程是异步的，线程是同步的
协程是非抢占式的，线程是抢占式的
线程是被动调度的，协程是主动调度的
协程可以暂停函数的执行，保留上一次调用时的状态，是增强型生成器
协程是用户级的任务调度，线程是内核级的任务调度
协程适用于 IO 密集型程序，不适用于 CPU 密集型程序的处理

#### 异步编程

python 3.5 版本引入了 await 取代 yield from 方式

import asyncio
async def py35_coro():
    await stuff()

主要用来解决等待网络服务的问题，发出请求后不用一直等待，可以在收到返回后进行响应。

注意： await 接收的对象必须是 awaitable 对象

awaitable 对象定义了 __await__() 方法

awaitable 对象有三类：
1. 协程 coroutine
2. 任务 Task
3. 未来对象 Future

协程调用过程：
调用协程时，会被注册到 ioloop， 返回 coroutine 对象
用 ensure_future 封装为 Future 对象
提交给 ioloop

在 Jupyter 中执行下面代码报错 ❌：

```
import asyncio
async def main():
    print('hello')
    await asyncio.sleep(3)
    print('word')

asyncio.run(main())
```

RuntimeError: asyncio.run() cannot be called from a running event loop

解决方案如下：

That’s the reason why you don’t need to start the event loop yourself in jupyter and you can directly call await main(url).

`asyncio.run(main()) => await main()`