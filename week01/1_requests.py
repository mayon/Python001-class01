import requests
import random
from time import sleep
import re
import pandas as pd
import lxml.etree
from bs4 import BeautifulSoup as bs
import os

def get_user_agent():
  ua_list = [
    "Mozilla/5.0 (compatible; U; ABrowse 0.6; Syllable) AppleWebKit/420+ (KHTML, like Gecko)",
    "Mozilla/5.0 (compatible; U; ABrowse 0.6;  Syllable) AppleWebKit/420+ (KHTML, like Gecko)",
    "Mozilla/5.0 (compatible; ABrowse 0.4; Syllable)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser 1.98.744; .NET CLR 3.5.30729)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser 1.98.744; .NET CLR   3.5.30729)",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0;   Acoo Browser; GTB5; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1;   SV1) ; InfoPath.1; .NET CLR 3.5.30729; .NET CLR 3.0.30618)",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SV1; Acoo Browser; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; Avant Browser)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1;   .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; GTB5; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; Maxthon; InfoPath.1; .NET CLR 3.5.30729; .NET CLR 3.0.30618)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; GTB5;",
  ];
  return random.choice(ua_list)

def get_page_text(url):
  headers = {
    'user-agent': get_user_agent(),
    'Accept': "*/*",
    'Accept-Language': 'en-AU,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,la;q=0.6',
    'Content-Type': 'text/plain',
    'Connection': 'keep-alive',
    'Origin': 'https://maoyan.com',
    'Referer': 'https://maoyan.com/films?showType=3',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
  }
  response = requests.get(url, headers=headers)
  print("------------------")
  print('Request Url      :', url)
  print('Response Status  :', response.status_code)
  return response.text;

def robot(listUrl, multiplier, find_film_urls_fun, xpaths, file_name):
  # Get film urls
  film_urls = []
  page_num = 2;
  list_urls = tuple((re.sub('{page}', str(page * multiplier), listUrl)) for page in range(page_num))
  for list_url in list_urls:
    bs_info = bs(get_page_text(list_url), 'html.parser')
    film_urls += find_film_urls_fun(bs_info)
    sleep(2)

  # Get film infos
  film_infos = [];
  for film_url in film_urls:
    selector = lxml.etree.HTML(get_page_text(film_url))
    for lxml_xpath in xpaths:
      lxml_info = selector.xpath(lxml_xpath)
      if (len(lxml_info)):
        film_infos.append(lxml_info[0]);
    sleep(2)

  # Save film infos
  pd_movie = pd.DataFrame(data = film_infos)
  path = os.path.abspath(os.path.dirname(__file__))
  pd_movie.to_csv(path + '/' + file_name + '.csv', encoding='utf8', index=False, header=False)

def doubanRobot():
  list_url = 'https://movie.douban.com/top250?start={page}&filter='
  multiplier = 25
  xpaths = [
    '//*[@id="content"]/h1/span[1]/text()',
    '//*[@id="info"]/span[10]/text()',
    '//*[@id="interest_sectl"]/div[1]/div[2]/strong/text()'
  ];
  file_name = '1_db_requests'

  def find_film_urls(info):
    urls = []
    for tags in info.findAll('div', attrs={ 'class': 'hd' }):
      for atag in tags.findAll('a'):
        urls.append(atag.get('href'))
    print('Douban Film Urls : ', urls)
    return urls

  robot(list_url, multiplier, find_film_urls, xpaths, file_name)

def maoyanRobot():
  list_url = 'https://maoyan.com/films?showType=2&offset={page}'
  multiplier = 30
  xpaths = [
    '//*[@class="movie-brief-container"]/h1/text()',
    '//*[@class="movie-brief-container"]/div/text()',
    '//*[@class="movie-brief-container"]/ul/li[1]/a[1]/text()',
    '//*[@class="movie-brief-container"]/ul/li[1]/a[2]/text()',
    '//*[@class="movie-brief-container"]/ul/li[3]/text()'
  ];
  file_name = '1_my_requests'

  def find_film_urls(info):
    print('Maoyan Page Title: ', re.findall('<title>(.+?)</title>', str(info))[0])
    urls = []
    for tags in info.findAll('div', attrs={ 'class': 'movie-item-hover' }):
      for atag in tags.findAll('a'):
        urls.append('https://maoyan.com' + atag.get('href'))
    print('Maoyan Film Urls : ', urls)
    return urls

  robot(list_url, multiplier, find_film_urls, xpaths, file_name)

doubanRobot()
maoyanRobot()