import requests
import random
from time import sleep
import re
import pandas as pd
import lxml.etree
import os
import pymysql

dbConfig = {
  'host': 'localhost',
  'port' : 3306,
  'user' : 'root',
  'password' : 'root1234',
  'db' : 'Douban'
}

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
  return response.text

if __name__ == '__main__':
  url = 'https://movie.douban.com/subject/34462775/comments?status=P'
  xpaths = {
    'comments': '//*[@class="comment-item"]',
    'comment_uname': './div[2]/h3/span[2]/a/text()',
    'comment_stars': './div[2]/h3/span[2]/span[2]/@class',
    'comment_time': './div[2]/h3/span[2]/span[3]/text()',
    'comment_votes': './div[2]/h3/span[1]/span/text()',
    'comment_short': './div[2]/p/span/text()',
  }
  infos = []
  selector = lxml.etree.HTML(get_page_text(url))
  comments = selector.xpath(xpaths['comments'])

  conn = pymysql.connect(
    host = dbConfig['host'],
    port = dbConfig['port'],
    user = dbConfig['user'],
    password = dbConfig['password'],
    db = dbConfig['db'],
    charset = 'utf8'
  )
  cur = conn.cursor()

  try:
    table_name = 'comment'
    sql = 'INSERT INTO ' + table_name + ' VALUES(%s,%d,%s,%d,%s);';
    
    for comment in comments:
      uname = comment.xpath(xpaths['comment_uname'])[0].strip()
      stars = comment.xpath(xpaths['comment_stars'])[0].split(' ')[0].split('star')[1].strip()
      time = comment.xpath(xpaths['comment_time'])[0].strip()
      votes = comment.xpath(xpaths['comment_votes'])[0].strip()
      short = comment.xpath(xpaths['comment_short'])[0].strip()

      print(uname, '\n', stars, '\n',time, '\n',votes, '\n',short)
      print('=' * 20)

      value = (uname, int(stars), time, int(votes), short)
      cur.execute(sql, value);

    cur.close()
    conn.commit()
  except:
    print('error')
    conn.rollback()
  conn.close()