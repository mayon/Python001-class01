# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from spiders.items import SpidersItem


class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/top250']

    # def parse(self, response):
    #     pass

    def start_requests(self):
        for i in range(2):
            url = 'https://movie.douban.com/top250?start=' + str(i * 25)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        title_list = soup.find_all('div', attrs={'class': 'hd'})
        for i in title_list:
            item = SpidersItem()
            title = i.find('a').find('span',).text
            link = i.find('a').get('href')
            item['title'] = title
            item['link'] = link
            yield scrapy.Request(url=link, meta={'item': item}, callback=self.parse2)

    def parse2(self, response):
        item = response.meta['item']
        soup = BeautifulSoup(response.text, 'html.parser')
        content = soup.find('div', attrs={'class': 'related-info'}).get_text().strip().replace(' ','').replace('\n','').replace('\u3000','')
        item['content'] = content
        yield item

