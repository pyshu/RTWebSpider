# -*- coding: utf-8 -*-
__author__ = 'lius'

'''客运营业站站点'''

from scrapy.spider import BaseSpider
from scrapy.http import Request
from spider_12306.items import StationItem
from spider_12306.items import CommitItemS
from scrapy import log

class stationsInfo(BaseSpider):
    name = "stationsInfo"

    start_urls = ["http://www.12306.cn/mormhweb/kyyyz/"]

    custom_settings = {
            'ITEM_PIPELINES': {
                'spider_12306.pipelines.StationSQLPipeline': 300,
            },
    }

    def parse(self,response):
        #获取铁路局名称
        railroad = response.xpath('//*[@id="secTable"]/tbody/tr/td/text()').extract()
        urls = response.xpath('//td[@class="submenu_bg"]/a/@href').extract()

        #根据规律生成url
        for i in range(0, len(railroad)):
            url1 = response.url + urls[i * 2][2:]
            yield Request(url1, callback=self.parse_station, meta={'bureau': railroad[i], 'station': True})

            url2 = response.url + urls[i * 2 + 1][2:]
            yield Request(url2, callback=self.parse_station, meta={'bureau': railroad[i], 'station': False})

    def parse_station(self, response):
        datas = response.css("table table tr")
        if len(datas) <= 2:
            return
        for i in range(0, len(datas)):
            if i < 2:
                continue
            infos = datas[i].css("td::text").extract()
            log.msg(infos,log.DEBUG)

            item = StationItem()
            item["bureau"] = response.meta["bureau"]
            item["station"] = response.meta["station"]
            item["name"] = infos[0]
            item["address"] = infos[1]
            item["passenger"] = infos[2].strip() != u""
            item["luggage"] = infos[3].strip() != u""
            item["package"] = infos[4].strip() != u""
            yield item
        yield CommitItemS()