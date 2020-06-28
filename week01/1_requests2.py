import requests
import random
from time import sleep
import re
import pandas as pd
import lxml.etree
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
  return response.text

def get_pages_xpath_info(urls, host = '', xpaths = [], xpath = ''):
  infos = [];
  for url in urls:
    selector = lxml.etree.HTML(get_page_text(host + url))
    if xpath:
      infos += selector.xpath(xpath)
    for xp in xpaths:
      infos += selector.xpath(xp)
    sleep(2)
  return infos

def saveToCSV(file_data, file_name):
  pd_movie = pd.DataFrame(data = file_data)
  path = os.path.abspath(os.path.dirname(__file__))
  pd_movie.to_csv(path + '/' + file_name + '.csv', encoding='utf8', index=False, header=False)

def doubanRobot():
  list_num = 2;
  list_perpage = 25
  list_url = 'https://movie.douban.com/top250?start={page}&filter='
  url_xpath = '//*[@class="hd"]/a/@href'
  info_xpaths = [
    '//*[@id="content"]/h1/span[1]/text()',
    '//*[@id="info"]/span[10]/text()',
    '//*[@id="interest_sectl"]/div[1]/div[2]/strong/text()'
  ];
  file_name = '1_db_requests2'
  
  list_urls = tuple((re.sub('{page}', str(page * list_perpage), list_url)) for page in range(list_num))
  film_urls = get_pages_xpath_info(list_urls, xpath = url_xpath)
  film_infos = get_pages_xpath_info(film_urls, xpaths = info_xpaths);
  saveToCSV(film_infos, file_name);
  print('Douban Film Infos : ', film_infos)

def maoyanRobot():
  list_num = 2
  list_perpage = 30
  list_url = 'https://maoyan.com/films?showType=3&offset={page}'
  url_xpath = '//*[@class="movie-item-hover"]/a/@href'
  info_xpaths = [
    '//*[@class="movie-brief-container"]/h1/text()',
    '//*[@class="movie-brief-container"]/div/text()',
    '//*[@class="movie-brief-container"]/ul/li[1]/a[1]/text()',
    '//*[@class="movie-brief-container"]/ul/li[1]/a[2]/text()',
    '//*[@class="movie-brief-container"]/ul/li[3]/text()'
  ];
  file_name = '1_my_requests2'
  url_host = 'https://maoyan.com'
  
  list_urls = tuple((re.sub('{page}', str(page * list_perpage), list_url)) for page in range(list_num))
  film_urls = get_pages_xpath_info(list_urls, xpath = url_xpath)
  film_infos = get_pages_xpath_info(film_urls, xpaths = info_xpaths, host = url_host);
  saveToCSV(film_infos, file_name);
  print('Maoyan Film Infos : ', film_infos)

doubanRobot()
maoyanRobot()