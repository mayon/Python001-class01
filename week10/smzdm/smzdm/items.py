# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SmzdmItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class GoodsItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    tag = scrapy.Field()

class CommentItem(scrapy.Item):
    author = scrapy.Field()
    comment_time = scrapy.Field()
    content = scrapy.Field()
    goods_title = scrapy.Field()
    goods_author = scrapy.Field()
    created_time = scrapy.Field()
    tag = scrapy.Field()