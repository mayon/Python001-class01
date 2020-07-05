# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# from mydb import ConnDB

class SpidersPipeline:
    # def process_item(self, item, spider):
    #     return item

    def process_item(self, item, spider):
        title = item['title']
        link = item['link']
        file_type = item['file_type']
        time = item['time']
        content = item['content']

        output = title + '\n' + link + '\n' + file_type + '\n' + time + '\n' + content + '\n\n'
        with open('./maoyanmovie.csv', 'a+', encoding='utf-8') as article:
            article.write(output)
        
        # value = (title, link, file_type, time, content)
        # db = ConnDB()
        # db.run(value)

        return item