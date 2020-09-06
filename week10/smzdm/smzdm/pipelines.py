# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from smzdm.mydb import ConnDB


class SmzdmPipeline:
    def process_item(self, item, spider):
        # title = item['title']
        # link = item['link']
        # tag = item['tag']
        # value = (title, link, tag)
        # db = ConnDB()
        # db.insert_goods(value)

        author = item['author']
        comment_time = item['comment_time']
        content = item['content']
        goods_title = item['goods_title']
        goods_author = item['goods_author']
        created_time = item['created_time']
        tag = item['tag']
        value = (author, comment_time, content, goods_title, goods_author, created_time, tag)

        db = ConnDB()
        db.insert_comment(value)
        # output = f'|{author}|\t|{comment_time}|\t|{content}|\t|{goods_title}|\t|{goods_author}|\n\n'
        # with open('./comment.txt', 'a+', encoding='utf-8') as article:
        #     article.write(output)
        #     article.close()

        return item
