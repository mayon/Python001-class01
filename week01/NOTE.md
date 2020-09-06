# 第一周学习笔记

## 1. Requests 爬虫

- requests

```
import requests
header = {'user-agent': user_agent}                       // user_agent： 伪装成浏览器
response = requests.get(url, headers=headers)
print('Response Status  :', response.status_code)
print(response.text)
```

- BeautifulSoup（bs4）

```
from bs4 import BeautifulSoup as bs
list_url = '***'
urls = []
bs_info = bs(get_page_text(list_url), 'html.parser')
for tags in info.findAll('div', attrs={ 'class': 'hd' }):
    urls.append(tags.find('a').get('href'))
```

- lxml

```
selector = lxml.etree.HTML(response.text)
links = selector.path('//*[@class="m"]/a/@href)      # type(links) >>> list
ctn = selector.path('//*[@class="m"]/span/text())    # type(links) >>> list
```

## 2. Scrapy 爬虫

- Scrapy 架构

| 组件 | 对应爬虫三大流程 | Scrapy 项目是否需要修改 |
| - | - | - |
| 引擎 |-| 无需修改，框架已写好 |
| 调度器 |-| 无需修改，框架已写好 |
| 下载器 | 获取网页（类 request 库）| 无需修改，框架已写好 |
| 爬虫器 | 解析网页（类 BeautifulSoup 库） | 需要 |
| 管道 | 存储数据（存入 CSV/txt/MySQL 等 | 需要 |
| 下载器中间件 | 获取网页 - 定制化部分 | 一般不用 |
| 爬虫器中间件 | 获取网页 - 定制化部分 | 一般不用 |

- 创建 Scrapy 项目

```
scrapy startproject spiderName
cd spiders/spiders
scrapy genspider douban douban.com
```

```
# spiders/qipaoshui.py
import scrapy
class DoubanSpider(scrapy.Spider):
    name = 'movie'
    allowed_domains = ['douban.com']                # 限制爬虫域范围
    start_urls = ['http://douban.com/']             # 必须先发起一次请求，才能启动内置的 Twisted 异步框架

    def parse(self, response):
        pass
```

- 配置 settings.py

```
USER_AGENT = 'spiders (+http://www.yourdomain.com)'  
DOWNLOAD_DELAY = 1                              # 下载延时
ITEM_PIPELINES = {                              # 开启之后，pipelines.py 才会生效
   'smzdm.pipelines.SmzdmPipeline': 300,
}
```

- 启动 Scrapy 项目:

```
scrapy crawl spiderName
```

- XPath
  - `.` : 当前路径
  - `..` : 当前路径上一级
  - `//` : 从根路径开始找（手动写）
  - `/` : 逐级开始查找（浏览器默认给定）
  -`@href` : 取属性，如 `/div[@class="hd"]`
  -`text()` : 取 text

- 可能错误：

返回值为非 items 时，如果用 return ，会报错 TypeError: 'Request' object is not iterable。
return scrapy.Request(self.start_urls, callback=self.parse_link)
 
有两种解决方法:

1.使用yield, 把return换为yield
yield scrapy.Request(self.start_urls, callback=self.parse_link)
 
2.使用return, 加个方括号, 转化为列表
return [scrapy.Request(self.start_urls, callback=self.parse_link)]