# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json

class JDPipeline(object):
    def open_spider(self, spider):
        try:
            if spider.name=='jdStart':
                self.file = open('jd.json', "w", encoding="utf-8")
        except Exception as err:
            print(err)
    def process_item(self, item, spider):
            dict_item = dict(item)
            json_str = json.dumps(dict_item, ensure_ascii=False) + "\n"
            self.file.write(json_str)
            return item
    def close_spider(self, spider):
        self.file.close()