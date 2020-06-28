# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class SpidersPipeline:
    # def process_item(self, item, spider):
    #     return item

    # def process_item(self, item, spider):
    #     title = '影片名称：' + item['title']
    #     link = '影片链接：' + item['link']
    #     content = '影片简介：' + item['content']
    #     output = title + '\n' + link + '\n' + content + '\n\n'
    #     with open('./maoyanmovie.txt', 'a+', encoding='utf-8') as article:
    #         article.write(output)
    #     return item

    def process_item(self, item, spider):
        title = '影片名称：' + item['title']
        link = '影片链接：' + item['link']
        file_type = '影片类型：' + item['file_type']
        time = '上映时间：' + item['time']
        content = '影片简介：' + item['content']
        output = title + '\n' + link + '\n' + file_type + '\n' + time + '\n' + content + '\n\n'
        with open('./maoyanmovie.csv', 'a+', encoding='utf-8') as article:
            article.write(output)
        return item