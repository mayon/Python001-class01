# 学习笔记

### 1. Python 中的类：

在 Python 中，一切皆对象，即数据与相关行为的集合。

- 古典类：V2.2 以前，Python 内置的数据类型和自定义的 class 定义的类，父类不相同。模拟出来的 list 和 dict 跟原生的数据结构不一样。
- 新式类：V2.2 以后

### 2. 类的定义
内置属性不能增加属性和方法
setattr(list, 'newattr', 'value') # TypeError

```
class Human2(object):   # 不加 (object) 是 Python2 中的写法，不过在 3 中依然会被认为是新式类，为避免混淆，必须加上
    _age = 0            # 人为约定，不可修改
    __fly = False       # 私有属性，强制不允许修改，Python 会自动改其变量名
                        # '_Human2__fly': False

Human2.__dict__         # 魔术方法，会随着环境发生而改变其值
```

显示 Object 类的所有子类
print( ().__class__.__bases__[0].__subclasses__() )
() # tuple
().__class__ # <class 'tuple'>
().__class__.__bases__ # <class 'object'>  # 父类
().__class__.__bases__[0].__subclasses__() # 父类下所有子类

### 3. 类的方法：

以下三种方法在内存中都归属于类

普通方法：至少一个 self 参数表示该方法的对象
def instance_method(self):
    pass
类方法：
- 至少一个 cls 参数，表示该方法的类
- 构造函数，默认只有一个 __new__ 构造函数，但无法满足所有的需求
- 所以，可以用类方法来模拟 java 定义多个构造函数的情况
@classmethod
def class_method(cls):
    pass
静态方法：由类直接调用，无参数，不能使用类属性和示例属性
@staticmethod
def static_method();
    pass

### 4. 类的属性

在类中，可以对示例获取属性这一行为进行拦截，可以对指定属性进行特殊处理：
- `__getattr__()`: 只能拦截未定义属性
- `__getattribute__()`: 可以拦截全部属性，优先级比 __getattr__() 高

属性描述符 property

- 描述器：实现特定协议（描述符）的类
```
property 类需要实现 __get__ , __set__ , __delete__ 方法

class Teacher:
    def __init__(self, name):
        self.name = name
    def __get__(self, instance, owner):       # self: 自身；instance: 引用它的实例；owner: 引用它的实例所属的类
        print(f'__set__{instance} {owner}')
        return self.name
    def __set__(self, instance, value):
        print(f'__set__{instance} {value}')
        self.name = value
    def __delete__(self, instance):
        print(f'__set__{instance}')
        del self.name
pythonTeacher = Teacher('yin')
```

- 装饰器：将方法封装成属性
  - 封装时：被装饰函数最好使用同一个方法名，如下例 gender
  - 说明：使用 setter 并不能真正意义上实现无法写入，属性值 gender 被改名为 _Article_gender
```
class Human(object):
    def __init__(self):
        self._gender = None
    @property
    def gender(self):         # 可以当做计算属性来用
        return self._gender
    @gender.setter            # 可以对值进行验证和过滤
    def gender(self, value):
        self._gender = value
    @gender.deleter
    def gender(self):
        del self._gender
```

- property:  Django 里常用的封装方法
    ```
    gender = property(get_, set_, del_, 'other property')
    ```

  - property 本质并不是函数，而是特殊类，实现了数据描述符的类
  - 如果一个对象同时定义了 __get__() 和 __set()__ 方法，则称为数据描述符
  - 如果仅定义了 __get__() 方法，则称为非数据描述符

  - property 的优点：
    1. 代码更简洁，可读性、可维护性更强
    2. 更好的管理属性的访问
    3. 控制属性访问权限，提高数据安全性

### 5. 类的继承

多继承：mixing

重载：Python 没有实现

多态：鸭子类型，动态语言

新式类：

新式类和经典类的区别：当前类或者父类集成了 Object 类，那么该类便是新式类，否则便是经典类

object 和 type 的关系：

- object 和 type 都属于 type 类（class 'type')
- type 类由 type 元类自身创建的。object 类是由元类 type 创建
- object 的父类为空，没有继承任何类
- type 的父类为 object 类（class 'object'）

类的继承：

- 单一继承

- 多重继承

- 菱形继承（钻石继承）

- 继承顺序：钻石继承
```
class BaseClass(object):
    num_base_calls = 0
    def call_me(self):
        print('Calling method on Base Class')
        self.num_base_calls += 1
class LeftSubClass(BaseClass):
    num_left_calls = 0
    def call_me(self):
        print('Calling method on Left Subclass')
        self.num_left_calls += 1
class RightSubClass(object):
    num_right_calls = 0
    def call_me(self):
        print('Calling method on Right Subclass')
        self.num_right_calls += 1

class Subclass(LeftSubClass, RightSubClass):
    pass

a = Subclass()
a.call_me()
print(Subclass.mro())

# [<class '__main__.Subclass'>, <class '__main__.LeftSubClass'>, <class '__main__.RightSubClass'>, <class '__main__.BaseClass'>, <class 'object'>]

# [<class '__main__.Subclass'>, <class '__main__.LeftSubClass'>, <class '__main__.BaseClass'>, <class '__main__.RightSubClass'>, <class 'object'>]

# 执行 call_me，查找顺序是
#          5 object
#         3 BaseClass
# 2 LeftSubClass 4 RightSubClass      
#         1 Subclass

# 先找 1，没有找 2，3 和 4 的父类都适合 5，从左往右找，先找 3，再找 4，最后找 5.
```

继承机制 MRO

- MRO 采用 C3 算法
- `Subclass.mro()` 查看继承链顺序
- 于有向无环图类似：
  - DAG（Directed Acyclic Graph）
  - DAG 原本是一种数据结构，因为 DAG 的拓扑结构带来的优异特性，经常被用于处理动态规划、寻求最短路径的场景。


### 6. 设计模式

SOLID 设计原则 

- 单一责任原则 The Single Responsibility Principle ： 职责越多，复杂度越高，职责过多时，大类拆小类
- 开放封闭原则 The Open Closed Principle：如果有新的功能，应该新增而不是修改，比如引入 @classmethod
- 里氏替换原则 The Liskov Substitution Principle：要求子类必须完整覆盖父类的所有方法
- 依赖倒置原则 The Dependency Inversion Principle：高层模块不应该依赖低层模块，如果有依赖必须建立两者之间的抽象，进行解耦
- 接口分离原则 The Interface Segregation Principle：接口是模块之间相互交流的抽象协议，一个接口的方法应该是模块刚好需要的

设计模式

- 有 22 种设计模式，常用的有两种：`单例模式` 和 `工厂模式`

单例模式

1. 对象只存在一个实例
2. __init__ 和 __new__ 的区别：
  - __new__ 是示例创建之前被调用，返回该示例对象，是静态方法
  - __init__ 是示例对象创建完成后被调用，是实例方法
  - __new__ 先被调用，__init__ 后背调用
  - __new__ 的返回值（实例 ）将传递给 __init__ 方法的第一个参数，__init__ 给这个实例设置相关参数

3. 三种创建单例模式的方法：
  1. 装饰器实现单实例模式
  2. `__new__` 方式实现单例模式
  3. 利用模块创建单例模式

工厂模式

1. 静态工厂模式创建方法
2. 动态工厂模式创建方法

元类：

- 元类是创建类的类，是类的模板
- 元类是用来控制如何创建类的，正如类是创建对象的模板一样
- 元类的实例为类，正如类的实例为对象
- 创建元类的两种方法
1.class
2.type
  - type：类名，父类的元祖，包含属性的字典
```
# 用元类来创建类
def hi(self):
    print('Hi metaclass')

Foo = type('Foo', (), {'say_hi': hi})
foo = Foo()
foo.say_hi()
```

抽象基类：

- 抽象基类（abstract base class， ABC）用来确保派生类实现了基类中的特定方法。
- 使用抽象基类的好处：
  - 避免继承错误，使类层次易于理解和维护
  - 抽象基类是无法实例化的
  - 如果忘记其中一个子类中实现忌口方法，要尽早报错

Mixin 模式：

在程序运行过程中，重定义类的继承，即动态继承。好处：

- 可以在不修改任何源代码的情况下，对已有类进行扩展
- 进行组件的划分
