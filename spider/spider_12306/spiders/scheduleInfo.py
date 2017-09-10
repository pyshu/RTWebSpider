# _*_ coding : utf-8 _*_
__author__ = 'lius'

import datetime
import json

from scrapy.http import Request
from scrapy.spider import BaseSpider

from spider.spider_12306.items import BriefItem
from spider.spider_12306.items import CommitItem
from spider.spider_12306.items import InfoItem


class ScheduleSpider(BaseSpider):
    name = 'scheduleInfo'

    custom_settings = {
            'ITEM_PIPELINES': {
                'spider_12306.pipelines.SQLPipeline': 350,
            },
    }

    def start_requests(self):
        url = "https://kyfw.12306.cn/otn/queryTrainInfo/getTrainName?date="

        t = (datetime.datetime.now() + datetime.timedelta(days = 3)).strftime("%Y-%m-%d")

        s_url = url + t
        self.logger.debug("start url " + s_url)
        yield Request(s_url, callback = self.parse, meta = {"t":t})

    def parse(self, response):
        datas = json.loads(response.body.decode())
        url = "https://kyfw.12306.cn/otn/czxx/queryByTrainNo?"
        for data in datas["data"]:
            item = BriefItem()
            briefs = data["station_train_code"].split("(")
            item["train_no"] = data["train_no"]
            item["code"] = briefs[0]
            briefs = briefs[1].split("-")
            item["start"] = briefs[0]
            item["end"] = briefs[1][:-1]
            yield item

            params = u"train_no=" + data["train_no"] + u"&from_station_telecode=BBB&to_station_telecode=BBB&depart_date=" + response.meta["t"]

            yield Request(url + params, callback = self.parse_train_schedule, meta = {"train_no":data["train_no"]})

    def parse_train_schedule(self, response):
        stations = json.loads(response.body.decode())

        datas = stations["data"]["data"]
        size = len(datas)
        for i in range(0, size):
            data = datas[i]

            info = InfoItem()
            info["train_no"] = response.meta["train_no"];
            info["no"] = int(data["station_no"])
            info["station"] = data["station_name"]

            if data["arrive_time"] == "----" and data["stopover_time"] == "----" :
                info["type"] = 0
            elif data["stopover_time"] == "----":
                info["type"] = 1
            else:
                info["type"] = 2
                
            if data["start_time"] != "----":
                info["start_time"] = data["start_time"] + ":00";
            else:
                info["start_time"] = None
            if data["arrive_time"] != "----":
                info["arrive_time"] = data["arrive_time"] + ":00";
            else:
                info["arrive_time"] = None
            if data["stopover_time"] != "----":
                info["stopover_time"] = data["stopover_time"] + ":00";
            else:
                info["stopover_time"] = None

            yield info
        yield CommitItem()
