# 第二周学习笔记

## 异常捕获

##### 美化异常输出 ： `pip install pretty_errors`

##### 异常输出语法：

1. **常规**

```

try:
    pass
except Exception as e:
    print(e)
```

2. **异常链捕获**

```
try:
    pass
except (ZeroDivisionError, Exception) as e:
    print(e)
```

3. **自定义异常**

```
class UserInputError(Exception):
    def __init__(self, ErrorInfo):
        super().__init__(self, ErrorInfo)
        self.errorinfo = ErrorInfo
        self.errorinf = ErrorInfo
    def __str__(self):
        return self.errorinfo
userinput = input('Please input a number:')
try:
    if (not userinput.isdigit()):
        raise UserInputError('input error')
    else :
        print(f'your input number : {userinput}')
except UserInputError as ue:
    print(ue)
finally:
    del userinput
```

## Python + MySql 

#### MySql 常用操作

- **启动 `mysql`：** 系统偏好设置 -> mysql -> Start Mysql Server

- **查看 `mysql` 进程服务：** `ps -ef|grep mysql`

- **`mysql` 常用命令：**

```
$ /usr/local/mysql/bin/mysql -u root -p
$ root1234

mysql > create database maoyan;
mysql > show databases;
mysql > use maoyan;
mysql > show tables;
mysql > create table movie(
     > id int(4) auto_increment not null primary key, 
     > title char(200) not null, 
     > link char(200) not null, 
     > content char(200), 
     > file_tyle char(200), 
     > time char(200)
     > );
mysql > insert into movie values(null,"test movie","test movie info","http://test","喜剧","2020-12-12");
mysql > select * from moive;
+----+--------------+-------------+-----------------+------------+------------------+
| id | title        | link        | content         | file_tyle  | time             |
+----+--------------+-------------+-----------------+------------+------------------+
|  1 | test11 movie | http://test | test movie info | 喜剧       | 2020-12-12       |
+----+--------------+-------------+-----------------+------------+------------------+
mysql > quit; # or
mysql > exit;
```

#### 数据库插件 pymysql 

```
dbInfo = {
    'host': 'localhost',
    'port' : 3306,
    'user' : 'root',
    'password' : 'root1234',
    'db' : 'maoyan'
}
...
conn = pymysql.connect(
    host = self.host,
    port = self.port,
    user = self.user,
    password = self.password,
    db = self.db,
    charset = 'utf8mb4'
)

cur = conn.cursor()                             // get current cursor 
count = cur.execute('select * from maoyanDb;')  // get result count
result = cur.fetchnone()                        // fetch one result
result = cur.fetchall()                         // fetch all result

values = [(id, 'testuser' + str(id)) for id in range(4, 21)];
cur.executemany('INSERT INTO ' + table_name + ' values(%s,%s)', values);

cur.close()
conn.commit()
conn.rollback()                                // try -> except

```

## 反爬虫策略

1. **模拟浏览器：** 丰富 `header` 中自定义参数，可以参考被爬取站点在真实浏览器上的 header 。

    - fake referer
    - fake host
    - fake useragent

```
from fake_useragent import UserAgent
ua = UserAgent(verify_ssl=False)
print(f'Chrome Useragent : {ua.chrome}')
print(f'Safari Useragent: {ua.safari}')
print(f'IE Useragent: {ua.ie}')
print(f'Random Useragent: {ua.random}')
```

2. **模拟登录 cookies 验证：**

```
import requests
# 常规用法
s = requests.Session()
r = s.get('http://httpbin.org/cookies')
print(r.text)
# 上下文环境
with requests.Session() as s:
    s.get('http://httpbin.org/cookies/set/sessioncookie/123456789')
    print(r.text)
```

3. **模拟浏览器行为：**

模拟用户行为：(chrmoDriver + selenium)

```
from selenium import webdriver
import time

try:
    browser = webdriver.Chrome()
    # install chrome driver
    # http://chromdriver.storage.googleapis.com/index.html

    browser.get('https://www.douban.com')
    time.sleep(1)

    browser.switch_to_frame(browser.find_elements_by_tag_name('iframe')[0])
    btm1 = browser.find_element_by_xpath('/html/body/div[1]/div[1]/ul[1]/li[2]')
    btm1.click()

    browser.find_element_by_xpath('//*[@id="username"]').send_keys('15055495@qq.com')
    browser.find_element_by_id('password').send_keys('test123test456')
    time.sleep(1)
    browser.find_element_by_xpath('//a[contains(@class, "btn-account")]').click()

    cookies = browser.get_cookies()
    print(cookies)
    time.sleep(3)

except Exception as e:
    print(e)
finally:
    browser.close()
```

```
    browser = webdriver.Chrome()
    browser.get('https://movie.douban.com/subject/1292052/')
    time.sleep(1)

    btm1 = browser.find_element_by_xpath('//*[@id="hot-comments"]/a')
    btm1.click()
    time.sleep(10)
    print(browser.page_source)
```

文件分块下载：

```
import requests
# 小文件可以放在内存中
image_url = 'https://www.python.org/static/community_logos/python-logo-master-v3-TM.png'
response = requests.get(image_url)
with open('python_logo.png', 'wb') as f:
    f.write(response.content)
# 大文件分块写在磁盘中
file_url = 'http://test.pdf'
response2 = requests.get(file_url, stream=True)
with open('python.pdf', 'wb') as pdf:
    for chunk in response2.iter_content(chunk_size=1024):
        if chunk:
            pdf.wirte(chunk)
```

4. **验证码识别**

    - 安装依赖库：libpng， jpeg，libtiff，leptonica，`brew install leptonica`
    - 安装图像识别库：`brew install tesseract`
    - 安装 py 插件：Pillow、pytesseract 

## 中间件 middleware：

1. **爬虫中间件**
    - 爬虫优先级在 setting 中设置: 高 -> 低，低 -> 高

2. **系统代理 IP：**

- 配置系统代理 IP（项目迁移时需要改变环境配置）
```
$ export http_proxy='http://52.179.231.206:80'
```
- 开启 setting 配置
```
SPIDER_MIDDLEWARES = {
   'spiders.middlewares.SpidersSpiderMiddleware': 543,
   'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
   'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 400,
}
```

3. **自定义中间件**

一般需要重写一下四个方法：

- `process_request(request, spider)` Request 对象经过下载中间件时会被调用，优先级高的先调用
- `process_response(request,response, spider)` Response 对象胫骨哦下载中间件时会被调用，优先级高的后调用
- `process_exception(request, exception, spider)` 当 process_exception() 和 process_request() 抛出异常时会被调用
- `from_crawler(cls, crawler)` 使用 crawler 来创建中间器对象，并（必须）返回一个中间件对象

4. **随机代理 IP**

middlewares.py
```
class RandomHttpProxyMiddleware(HttpProxyMiddleware):

    def __init__(self, auth_encoding='utf-8', proxy_list = None):
        self.proxies = defaultdict(list)
        for proxy in proxy_list:
            parse = urlparse(proxy)
            self.proxies[parse.scheme].append(proxy)
        
    @classmethod
    def from_crawler(cls, crawler):
        if not crawler.settings.get('HTTP_PROXY_LIST'):
            raise NotConfigured

        http_proxy_list = crawler.settings.get('HTTP_PROXY_LIST')
        auth_encoding = crawler.settings.get('HTTPPROXY_AUTH_ENCODING', 'utf-8')
        return cls(auth_encoding, http_proxy_list)

    def _set_proxy(self, request, scheme):
        proxy = random.choice(self.proxies[scheme])
        request.meta['proxy'] = proxy
```

setting.py
```
SPIDER_MIDDLEWARES = {
   'spiders.middlewares.SpidersSpiderMiddleware': 543,
   'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
   'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': None,
   'spiders.middlewares.RandomHttpProxyMiddleware': 400,                # Add
   'spiders.middlewares.RandomUserAgentMiddleware': 400,
}
```


## 分布式爬虫（Scrapy Redis）

- scrapy 原生不支持分布式，多机之间需要 Redis 实现队列和管道的共享
- scrapy-Redis 实现了 scrapy 和 Redis 的集成：`pip install scrapy-redis`
    1. 使用 RedisSpider 类替代 Spider 类
    2. Scheduler 的 queue 由 Redis 实现
    3. item pipeline 由 Redis 实现

---

## 学习体会

不在开发岗位之后就没有碰过 MySQL，终端操作 MySQL 的命令彻底忘记，SQL 语法还记得，不过写起来错误百出，需要反复 Debug 才能正常运行。

验证码用到大量图形学的知识，跟着敲了一遍，但还是一点印象都没有，只是知道有这些工具和插件的存在，要掌握得大量反复的训练，还得吸收更多图像学相关的理论。

中间件的概念很容易理解，不过语法（套路）需要死记硬背，一时半会记不住，得多写项目实际操练才行。

总的来说，这周内容看起来知识点不多，但是涉及的面很广，辛亏有一点开发经验，才能勉强完成作业。其他跨行学习的小伙伴，估计会比较晕。

上周替换成 scrapy 后，猫眼那边一直拉不到数据，这周有一次拉到数据，结果数据的取值写错。太久没有高强度学习，希望借这次的学习机会重新找回状态。