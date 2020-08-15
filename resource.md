# 极客时间 · Python 训练营

## Week 预习

1. 老师的课件在哪里查看？

    点击链接: <https://pan.baidu.com/s/1bwl0b6ooKKzBi0tc_MCB_w> 密码: 1iu4

2. 相关链接
    - [ ] 《提问的智慧》： <https://github.com/ryanhanwu/How-To-Ask-Questions-The-Smart-Way/blob/master/README-zh_CN.md>
    - [ ] Python 3.7.7 官方文档： <https://docs.python.org/zh-cn/3.7/>
    - [ ] GitHub 搜索帮助： <https://help.github.com/cn/github/searching-for-information-on-github>
    - [ ] PEP8 规范： <https://www.python.org/dev/peps/pep-0008/>
    - [ ] Google Python Style Guides： <http://google.github.io/styleguide/pyguide.html>
    - [ ] Python 官方网站： <https://www.python.org>
    - [ ] 字符编码：ASCII，Unicode 和 UTF-8：<http://www.ruanyifeng.com/blog/2007/10/ascii_unicode_and_utf-8.html>

3. Git 下载地址：

    链接: <https://pan.baidu.com/s/16xpckuEBr7iSLg_0sk-D1Q> 密码:d0uv

4. Python 安装包

    - 下载地址: <https://www.python.org/downloads/>

    - 安装方法: <https://docs.python.org/zh-cn/3.7/using/windows.html>

    - Windows（用电脑浏览器):<https://github.com/wilsonyin123/geekbangpython/blob/master/install_python_windows.pdf>

5. 常用 pip 源地址
    - 豆瓣： <https://pypi.doubanio.com/simple/>
    - 清华： <https://mirrors.tuna.tsinghua.edu.cn/help/pypi/>
    - 中科大： <https://pypi.mirrors.ustc.edu.cn/simple/>
    - 阿里云： <https://mirrors.aliyun.com/pypi/simple/>

6. 修改 pip 源方式

    临时替换

    ```
    pip install -i https://pypi.tuna.tsinghua.edu.cn/simple some-package
    ```

    永久替换（先升级 pip：pip install pip -U ）
    ```
    pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
    ```

7. 虚拟环境和包
    <https://docs.python.org/zh-cn/3.7/tutorial/venv.html>

8. Visual Studio Code 下载地址
    <https://code.visualstudio.com/#alt-downloads>

9. Python 基础语法

    - [ ] Python 简介： <https://docs.python.org/zh-cn/3.7/tutorial/introduction.html>
    - [ ] Python 标准语法： <https://docs.python.org/zh-cn/3.7/tutorial/index.html>
    - [ ] Python 内置函数： <https://docs.python.org/zh-cn/3.7/library/functions.html>
    - [ ] Python 内置类型： <https://docs.python.org/zh-cn/3.7/library/stdtypes.html>
    - [ ] Python 数据类型： <https://docs.python.org/zh-cn/3.7/library/datatypes.html>
    - [ ] Python 标准库： <https://docs.python.org/zh-cn/3.7/library/index.html>
    - [ ] Python 计算器使用： <https://docs.python.org/zh-cn/3.7/tutorial/introduction.html>
    - [ ] Python 数据结构： <https://docs.python.org/zh-cn/3.7/tutorial/datastructures.html>
    - [ ] Python 其他流程控制工具 : <https://docs.python.org/zh-cn/3.7/tutorial/controlflow.html>
    - [ ] Python 中的类： <https://docs.python.org/zh-cn/3.7/tutorial/classes.html>
    - [ ] Python 定义函数： <https://docs.python.org/zh-cn/3.7/tutorial/controlflow.html#defining-functions>

10. HTML（超文本标记语言）的基础哦

    - [ ] HTML 标准语法： <https://developer.mozilla.org/zh-CN/docs/Web/HTML>L>
    - [ ] HTML 元素参考： <https://developer.mozilla.org/zh-CN/docs/Web/HTML/Element>
    - [ ] HTML 属性参考： <https://developer.mozilla.org/zh-CN/docs/Web/HTML/Attributes>
    - [ ] HTML 全局属性： <https://developer.mozilla.org/zh-CN/docs/Web/HTML/Global_attributes>
    - [ ] HTML 链接类型： <https://developer.mozilla.org/zh-CN/docs/Web/HTML/Link_types>

11. W3C 标准官方文档：
    - [ ] <https://www.w3.org/standards/>

12. 常见通信端口：
    - <https://www.sojson.com/port.html>

---

## Week 01：requests 爬虫 & scrapy 爬虫

1. requests 官方文档链接：
    - [ ] <https://requests.readthedocs.io/zh_CN/latest/>

2. 课程源码

    - <https://github.com/wilsonyin123/geekbangtrain.git>
    - <https://gitee.com/wilsonyin/pythontrain.git>

3. Beautiful Soup 官方文档链接：
    - [ ] <https://www.crummy.com/software/BeautifulSoup/bs4/doc.zh/>

4. Scrapy 架构官方文档介绍：
    - [ ] <https://docs.scrapy.org/en/latest/topics/architecture.html>

5. Scrapy Xpath 官方学习文档：
    - [ ] <https://docs.scrapy.org/en/latest/topics/selectors.html#working-with-xpaths>

6. Xpath 中文文档：
    - [ ] <https://www.w3school.com.cn/xpath/index.asp>

7. Xpath 英文文档：
    - [ ] <https://www.w3.org/TR/2017/REC-xpath-31-20170321/#nt-bnf>

8. yield 表达式官方文档：
    - [ ] <https://docs.python.org/zh-cn/3.7/reference/expressions.html#yieldexpr>

9. yield 语句官方文档
    - [ ] <https://docs.python.org/zh-cn/3.7/reference/simple_stmts.html#yield>

10. Python 推导式官方文档：
    - [ ] <https://docs.python.org/zh-cn/3.7/tutorial/datastructures.html#list-comprehensions>

11. 补充说明：

    dont_filter 设置为 True，是用来解除去重功能。Scrapy 自带 url 去重功能，第二次请求之前会将已发送的请求自动进行过滤处理。
    所以将 dont_filter 设置为 True 起到的作用是解除去重功能，一旦设置成重 True，将不会去重，直接发送请求。

---

## Week 02：反爬虫机制 & 分布式爬虫

1. pretty_errors 官方文档链接：
    - [ ] <https://pypi.org/project/pretty-errors/>

2. try 语句官方文档：
    - [ ] <https://docs.python.org/zh-cn/3.7/reference/compound_stmts.html#the-try-statement>

3. with 语句官方文档：
    - [ ] <https://docs.python.org/zh-cn/3.7/reference/compound_stmts.html#the-with-statement>

4. with 语句上下文管理器官方文档：
    - [ ] <https://docs.python.org/zh-cn/3.7/reference/datamodel.html#with-statement-context-managers>

5. MySQL 官方文档手册：
    - [ ] <https://dev.mysql.com/doc/>

6. MySQL 官方下载连接：
<https://dev.mysql.com/downloads/mysql/>

7. PyMySQL 官方文档:
    - [ ] <https://pypi.org/project/PyMySQL/>

8. User-Agent 参考文档：
    - [ ] <https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Headers/User-Agent>

9. httpbin 网址：
<https://httpbin.org/>

10. WebDriver 文档：
<https://www.w3.org/TR/webdriver/>
<https://www.selenium.dev/selenium/docs/api/py/>

11. ChromeDriver 下载地址：
<https://chromedriver.storage.googleapis.com/index.html>

12. 各种语言识别库：
    - [ ] <https://github.com/tesseract-ocr/tessdata>

13. setting.py 配置项说明：

    - 用大写是一种约定行为，scrapy 自带的设置都是大写，如果要修改默认的配置项，那必须是大写（因为 scrapy 内部对这些配置的处理都是大写的）。

    - 如果是自定义的中间件或扩展和配置项，自己是可以控制配置项是否是大小写的，但建议使用者尽量遵守约定，使用全大写。

14. redis 官方网址：<https://redis.io/>

---

## Week 03：多进程、多线程

1. Twisted 学习参考文档：
    - [ ] <https://pypi.org/project/Twisted/>

2. asyncio — 异步 I/O 学习文档
    - [ ] <https://docs.python.org/zh-cn/3.7/library/asyncio.html>

3. os 模块学习文档：
    - [ ] <https://docs.python.org/zh-cn/3.7/tutorial/stdlib.html#operating-system-interface>

4. multiprocessing – 基于进程的并行学习文档：
    - [ ] <https://docs.python.org/zh-cn/3.7/library/multiprocessing.html>

5. 进程之间的两种通信通道：
    - [ ] <https://docs.python.org/zh-cn/3.7/library/multiprocessing.html#exchanging-objects-between-processes>

6. 管道和队列参考文档：
    - [ ] <https://docs.python.org/zh-cn/3.7/library/multiprocessing.html#pipes-and-queues>

7. 进程间的同步学习文档：
    - [ ] <https://docs.python.org/zh-cn/3.7/library/multiprocessing.html#synchronization-between-processes>

8. 进程池学习文档：
    - [ ] <https://docs.python.org/zh-cn/3.7/library/multiprocessing.html#module-multiprocessing.pool>

9. 迭代器学习文档：
    - [ ] <https://docs.python.org/zh-cn/3.7/library/stdtypes.html#iterator-types>

10. 基于线程的并行学习文档：
    - [ ] <https://docs.python.org/zh-cn/3.7/library/threading.html>

11. 基于进程的并行学习文档：
    - [ ] <https://docs.python.org/zh-cn/3.7/library/multiprocessing.html>

12. 底层多线程 API：
    - [ ] <https://docs.python.org/zh-cn/3.7/library/_thread.html>

13. 锁对象学习文档：
    - [ ] <https://docs.python.org/zh-cn/3.7/library/threading.html#lock-objects>

14. 递归锁对象：
    - [ ] <https://docs.python.org/zh-cn/3.7/library/threading.html#rlock-objects>

15. queue 学习文档：
    - [ ] <https://docs.python.org/zh-cn/3.7/library/queue.html>

16. concurrent.futures - 线程池执行器：
    - [ ] <https://docs.python.org/zh-cn/3.7/library/concurrent.futures.html#threadpoolexecutor>

17. concurrent.futures - 进程池执行器：
    - [ ] <https://docs.python.org/zh-cn/3.7/library/concurrent.futures.html#processpoolexecutor>

---

## week 04：数据清洗与预处理

1. `pandas` 中文文档：
    - [ ] <https://www.pypandas.cn/docs/>

2. `sklearn-pandas` 安装参考文档：
    - [ ] <https://pypi.org/project/sklearn-pandas/1.5.0/>

3. Numpy 学习文档：
    - [ ] <https://numpy.org/doc/>

4. matplotlib 学习文档：
    - [ ] <https://matplotlib.org/contents.html>

5. DataFrame 学习文档：
    - [ ] <https://pandas.pydata.org/pandas-docs/stable/reference/frame.html>

6. Pandas 计算功能操作文档：
    - [ ] <https://pandas.pydata.org/docs/user_guide/computation.html#method-summary>

7. MySQL 数据库多表连接学习文档：
    - [ ] <https://dev.mysql.com/doc/refman/8.0/en/join.html>

8. plot 学习文档：
    - [ ] <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.plot.html>

9. seaborn 学习文档：
    - [ ] <http://seaborn.pydata.org/tutorial.html>

10. jieba 学习文档：
    - [ ] <https://github.com/fxsjy/jieba/blob/master/README.md>

11. snowNLP 参考学习地址：
    - [ ] <https://github.com/isnowfy/snownlp/blob/master/README.md>

---

## week 06：Django Web 开发入门

1. Django 官方文档：
    - 注意：查看文档时，版本号要跟使用的 Django 版本号相同
    - [ ] <https://docs.djangoproject.com/zh-hans/3.0/>

2. Bootstrap 模板：
    - <https://getbootstrap.com/>

---

## week 07：面向对象编程

---

## week 08：Python 高阶语法

1. collections 官方文档：
    - [ ] https://docs.python.org/zh-cn/3.7/library/collections.html

2. Flask 快速 Web 框架：
    - [ ] https://flask.palletsprojects.com/en/1.1.x/

3. aiohttp 快速 Web 框架：
    - [ ] https://hubertroy.gitbooks.io/aiohttp-chinese-documentation/content/

4. 《fluent python》

5. ioloop
https://docs.python.org/zh-cn/3/library/asyncio-tack.html


---

## week 09：Django Web 开发进阶