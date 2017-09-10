# -*- coding: utf-8 -*-
__author__ = 'lius'

'''代售点'''

import json

from scrapy import log
from scrapy.http import Request
from scrapy.spider import BaseSpider

from spider.spider_12306.items import AgencyItem
from spider.spider_12306.items import CommitItemA


class agencyInfo(BaseSpider):
    name = "agencyInfo"

    start_urls = ["https://kyfw.12306.cn/otn/userCommon/allProvince"]

    custom_settings = {
            'ITEM_PIPELINES': {
                'spider_12306.pipelines.AgencySQLPipeline': 400,
            },
    }

    def parse(self, response):
        #获取省份信息
        province = json.loads(response.body.decode())

        for data in province['data']:
            url = "https://kyfw.12306.cn/otn/queryAgencySellTicket/query?province=" + data['chineseName'] +"&city=&county="
            yield Request(url, callback=self.parse_agency)

    def parse_agency(self, response):
        # 获取代售点信息
        agency = json.loads(response.body.decode())
        for data in agency["data"]["datas"]:
             log.msg(data["province"], data["city"],data["county"], data["address"],data["agency_name"],
                   data["windows_quantity"],data["start_time_am"] ,data["stop_time_pm"],log.DEBUG)
             item = AgencyItem()
             item["province"] = data["province"]
             item["city"] = data["city"]
             item["county"] = data["county"]
             item["address"] = data["address"]
             item["name"] = data["agency_name"]
             item["windows"] = data["windows_quantity"]
             item["start"] = data["start_time_am"]
             item["end"] = data["stop_time_pm"]
             yield item
        yield CommitItemA()
