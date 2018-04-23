# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

# class XbdataPipeline(object):
#     def process_item(self, item, spider):
#         return item
import pymongo
from scrapy.conf import settings


class MeituanPipeline(object):

    collection_name = 'meituanList'

    def __init__(self, mongo_port, mongo_host, mongo_db):
        self.mongo_port = mongo_port
        self.mongo_db = mongo_db
        self.mongo_host = mongo_host

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_host=crawler.settings.get('MONGO_HOST'),
            mongo_db=crawler.settings.get('MONGO_DBNAME', 'items'),
            mongo_port=crawler.settings.get('MONGO_PORT')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_host, self.mongo_port)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(dict(item))
        return item
