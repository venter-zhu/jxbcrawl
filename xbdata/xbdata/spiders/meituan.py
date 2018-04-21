# -*- coding: utf-8 -*-
import json
import hashlib

import scrapy
from scrapy import Request, log, FormRequest
import os

RESULT_PATH = os.path.join(os.path.abspath('..'), 'result')

# 试点，目前只针对北京地区，后续应该改进，范围扩大到美团上的所有商家信息
PSOT_DATA = {
    "offset": '0',
    "limit": '15',
    "cateId": '1',
    "lineId": '0',
    "stationId": '0',
    "areaId": '17',
    "sort": "default",
    "deal_attr_23": "",
    "deal_attr_24": "",
    "deal_attr_25": "",
    "poi_attr_20043": "",
    "poi_attr_20033": ""
}


class MeituanSpider(scrapy.Spider):
    name = 'meituan'
    allowed_domains = ['meituan.com']
    start_urls = ['http://meishi.meituan.com/i/?ci=1&stid_b=1&cevent=imt%2Fhomepage%2Fcategory1%2F1']

    # parse_index
    # 获取分类链接，每个地区下面都有一个二级分类,三级分类暂且不考虑
    def parse(self, response):
        content = response.xpath('/html/body/script[8]/text()').extract_first()
        json_obj = self.get_json_str(content)
        area_list = json_obj.get('navBarData').get('areaList')
        for item in area_list:
            PSOT_DATA['areaId'] = str(item.get("id"))
            yield FormRequest(
                "http://meishi.meituan.com/i/api/channel/deal/list",
                formdata=PSOT_DATA,
                callback=self.parse_list,
            )

    def parse_category(self, response):
        pass

    def parse_list(self, response):
        json_obj = self.get_json_str(response.body.decode())
        if json_obj.get('status') == 0:
            total = json_obj.get('data').get('poiList').get('totalCount')
            item_list = json_obj.get('data').get('poiList').get('poiInfos')
        for item in item_list:
            ct_poi = item.get('ctPoi')
            poiid = item.get('poiid')
            url = "http://meishi.meituan.com/i/poi/{poiid}?ct_poi={ct_poi}"
            yield Request(url.format(poiid=poiid, ct_poi=ct_poi), callback=self.parse_detail)

    def parse_detail(self, response):
        filename = self.url_to_md5(response.url) + '.json'
        with open(os.path.join(RESULT_PATH, filename), mode='wb') as f:
            f.write(response.body)

    def get_json_str(self, content):
        # 截取json格式的数据
        if not content.startswith('window._appState = '):
            try:
                return json.loads(content)
            except json.JSONDecodeError as e:
                log.msg("JSON编码错误", _level=log.ERROR)
                return None
        json_str = content.split('window._appState = ')[1]
        json_str = json_str[:json_str.rindex("}") + 1]
        json_obj = json.loads(json_str, encoding='utf8')
        return json_obj

    def url_to_md5(self, url_str):
        # 将url编码成MD5
        m1 = hashlib.md5()
        m1.update(url_str.encode(encoding='utf-8'))
        return m1.hexdigest()