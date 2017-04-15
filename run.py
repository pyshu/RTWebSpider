# -*- coding: utf-8 -*-

# import the spiders you want to run
from spider_12306.spiders.stationsInfo import stationsInfo
from spider_12306.spiders.agencyInfo import agencyInfo
from spider_12306.spiders.scheduleInfo import ScheduleSpider
from spider_12306.spiders.ticketsInfo import TicketsSpider

# scrapy api imports
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerProcess
# from scrapy.settings import Settings
from scrapy.utils.project import get_project_settings

settings = get_project_settings()

crawler = CrawlerProcess(settings)

@defer.inlineCallbacks
def crawl():
    yield crawler.crawl(stationsInfo)
    yield crawler.crawl(agencyInfo)
    yield crawler.crawl(ScheduleSpider)
    yield crawler.crawl(TicketsSpider)

crawl()
crawler.start()
