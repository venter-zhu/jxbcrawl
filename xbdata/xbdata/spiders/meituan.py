# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import json

# 试点，目前只针对北京地区，后续应该改进，范围扩大到美团上的所有商家信息


class MeituanSpider(scrapy.Spider):
    name = 'meituan'
    allowed_domains = ['meituan.com']
    start_urls = ['https://meishi.meituan.com/i/?ci=1&stid_b=1&cevent=imt%2Fhomepage%2Fcategory1%2F1']

    # parse_index
    # 获取分类链接，每个地区下面都有一个二级分类
    def parse(self, response):
        content = response.xpath(r'/html/body/script[8]/text()').extract_first()
        if not content.startswith('window._appState = '):
            return
        json_str = content.split('window._appState = ')[1]
        json_str = json_str[:json_str.rindex("}") + 1]
        json_obj = json.loads(json_str, encoding='utf8')
        url_info = json_obj.get('filters').get('areas')
        for url in url_info:
            yield Request(url.get('url'), callback=self.parse_category)

    def parse_category(self, response):
        pass

    def parse_list(self, response):
        pass

    def parse_detail(self, response):
        pass
