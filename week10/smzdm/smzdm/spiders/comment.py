# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from smzdm.items import GoodsItem
from smzdm.items import CommentItem
import time

class CommentSpider(scrapy.Spider):
    name = 'comment'
    allowed_domains = ['smzdm.com']
    start_urls = ['https://www.smzdm.com/fenlei/zhinengshouji/h5c4s0f0t0p1/#feed-main/']

    # def parse(self, response):
    #     pass

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0], callback=self.request_comment)

    def parse_goods(self, response):
        items = []
        goods_list = Selector(response=response).xpath('//li[@class="feed-row-wide"]')
        for i in goods_list[:10]:
            item = GoodsItem()
            title = i.xpath('./div/div[2]/h5/a/text()').extract_first().strip()
            link = i.xpath('./div/div[2]/h5/a/@href').extract_first().strip()
            item['title'] = title
            item['link'] = link
            item['tag'] = 'zhinengshouji'
            items.append(item)
        return items

    def request_comment(self, response):
        goods_list = Selector(response=response).xpath('//div[@class="z-feed-foot-l"]')
        # print(goods_list)
        for goods in goods_list[:10]:
            comment_url = goods.xpath('./a[2]/@href').extract_first().strip().replace('#comments','')
            comment_num = goods.xpath('./a[2]/span/text()').extract_first().strip()
            comment_pages = int(int(comment_num) / 30) + 1
            print(f'{comment_url}\t{comment_num}\t{comment_pages}')
            for i in range(comment_pages):
                url = comment_url
                if i > 0:
                    url += '/p' + str(i + 1) +'/#comments'
                print(url)
                yield scrapy.Request(url=url, callback=self.parse_comment)

    def parse_comment(self, response):
        items = []
        selector = Selector(response=response)
        goods_title = selector.xpath('//h1[@class="title J_title"]/text()').extract_first().strip()
        goods_author = selector.xpath('//span[@class="name"]/text()').extract_first().strip()
        # print(f'{goods_title}\t{goods_author}\t')

        comment_list = selector.xpath('//div[@class="comment_conBox"]')
        # print(comment_list)
        for cmt in comment_list:
            author = cmt.xpath('./div[1]/a/span/text()').extract_first().strip()
            if author == goods_author + '（爆料人）':
                author = goods_author
            content = cmt.xpath('./div[@class="comment_conWrap"]/div[1]/p/span/text()').extract_first().strip()
            comment_time = cmt.xpath('./div[1]/div[1]/text()').extract_first().strip()
            # print(f'{author}\t{content}\t{comment_time}\t')
            item = CommentItem()
            item['author'] = author
            item['content'] = content
            item['comment_time'] = self.deal_timestr(comment_time)
            item['goods_title'] = goods_title
            item['goods_author'] = goods_author
            item['created_time'] = time.strftime("%Y-%m-%d %H:%M", time.localtime())
            item['tag'] = 'zhinengshouji'
            items.append(item)
        return items

    def deal_timestr(self, timestr):
        newtime = timestr
        if '分钟前' not in timestr and '小时前' not in timestr:
            newtime = time.strftime("%Y", time.localtime()) + '-' + newtime
        return newtime