# -*- coding: utf-8 -*-
import scrapy
from spiders.items import SpidersItem
import lxml.etree


class MaoyanSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/films?showType=3&offset=']

    # def parse(self, response):
    #     pass

    def start_requests(self):
        for i in range(2):
            url = 'https://maoyan.com/films?showType=3&offset=' + str(i * 30)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        selector = lxml.etree.HTML(response.text)
        links_xpath = '//*[@class="movie-item-hover"]/a/@href'
        links = selector.xpath(links_xpath)
        print('-------------------------')
        print(links)
        print('-------------------------')
        for link in links:
            item = SpidersItem()
            item['link'] = str('https://maoyan.com' + link)
            yield scrapy.Request(url=item['link'], meta={'item': item}, callback=self.parse2)

    def parse2(self, response):
        selector = lxml.etree.HTML(response.text)
        item = response.meta['item']
        title = selector.xpath('//*[@class="movie-brief-container"]/h1/text()')
        file_type = selector.xpath('//*[@class="movie-brief-container"]/ul/li[1]/a[1]/text()')
        time = selector.xpath('//*[@class="movie-brief-container"]/ul/li[3]/text()')
        content = selector.xpath('//*[@id="app"]/div/div[1]/div/div[3]/div[1]/div[1]/div[2]/span/text()')
        item['title'] = str(title[0])
        item['file_type'] = str(file_type[0])
        item['time'] = str(time[0])
        item['content'] = str(content[0])
        print(item)
        print('-------------------------')
        yield item

