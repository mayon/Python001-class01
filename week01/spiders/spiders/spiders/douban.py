# -*- coding: utf-8 -*-
import scrapy
from spiders.items import SpidersItem
import lxml.etree


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
        selector = lxml.etree.HTML(response.text)
        links_xpath = '//*[@class="hd"]/a/@href'
        links = selector.xpath(links_xpath)
        for link in links:
            item = SpidersItem()
            item['link'] = str(link)
            yield scrapy.Request(url=link, meta={'item': item}, callback=self.parse2)

    def parse2(self, response):
        selector = lxml.etree.HTML(response.text)
        item = response.meta['item']
        title_xpath = '//*[@id="content"]/h1/span[1]/text()'
        content_xpath = '//*[@id="link-report"]/span[1]/text()'
        title = selector.xpath(title_xpath)
        content = selector.xpath(content_xpath)
        item['title'] = str(title[0])
        if len(content):
            item['content'] = content[0].replace(' ','').replace('\n','').replace('\u3000','')
        else:
            item['content'] = ''
        yield item

