# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class XbdataItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class MeituanItem(scrapy.Item):
    # url 信息来源
    # args 如果是post请求，保存请求参数
    # content 原始文本
    url = scrapy.Field()
    args = scrapy.Field()
    content = scrapy.Field()
    method = scrapy.Field()
    time = scrapy.Field()
    type = scrapy.Field()
