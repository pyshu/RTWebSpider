# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql.cursors
from scrapy import log

from spider_12306.items import CommitItemS
from spider_12306.items import CommitItemA

from spider_12306.items import CommitItem
from spider_12306.items import BriefItem
from spider_12306.items import InfoItem

from spider_12306.items import BriefDeltaItem
from spider_12306.items import StationNameItem
from spider_12306.items import TicketItem

class StationSQLPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(host = 'localhost', port = 3306,
                                        user = 'root',
                                        password = '12345',
                                        db = 'train',
                                        charset = 'utf8')
        self.cursor = self.conn.cursor()
        self.sql = "INSERT IGNORE INTO `stations` (`bureau`, `station`,\
                `name`, `address`, `passenger`, `luggage`,\
                `package`) VALUES\
                (%s, %s, %s, %s, %s, %s, %s)"

    def process_item(self, item, spider):
        if isinstance(item, CommitItemS):
            self.conn.commit()
        else:
            self.cursor.execute(self.sql, (item["bureau"],
                                           item["station"],
                                           item["name"],
                                           item["address"],
                                           item["passenger"],
                                           item["luggage"],
                                           item["package"]))

class AgencySQLPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(host = 'localhost', port = 3306,user = 'root',password = '12345',db = 'train',charset = 'utf8')
        self.cursor = self.conn.cursor()
        self.sql = "INSERT IGNORE INTO `agencys` (`province`, `city`, `county`,\
            `address`, `name`, `windows`, `start`, `end`) VALUES\
            (%s, %s, %s, %s, %s, %s, %s, %s)"

    def process_item(self, item, spider):
        if isinstance(item, CommitItemA):
            self.conn.commit()
        else:
            self.cursor.execute(self.sql, (
                item["province"],
                item["city"],
                item["county"],
                item["address"],
                item["name"],
                item["windows"],
                item["start"],
                item["end"]))


class SQLPipeline(object):
        def __init__(self):
            self.conn = pymysql.connect(host='localhost', port=3306,
                                        user='root',
                                        password='12345',
                                        db='train',
                                        charset='utf8')
            self.cursor = self.conn.cursor()
            self.brief_sql = "INSERT IGNORE INTO `train_briefs` VALUES\
                        (%s, %s, %s, %s, %s)"
            self.info_sql = "INSERT IGNORE INTO `train_infos` VALUES\
                        (%s, %s, %s, %s, %s, %s, %s)"
            self.update_brief = "UPDATE `train_briefs` SET \
                        `seat_type` = %s WHERE `code` = %s"
            self.station_sql = "INSERT IGNORE INTO `train_stations` VALUES\
                        (%s, %s)"
            self.tickets_sql = "INSERT IGNORE INTO `train_tickets` VALUES\
                        (%s, %s, %s, %s, %s, %s, %s, %s,\
                        %s, %s, %s, %s, %s, %s)"

        def process_item(self, item, spider):
            try:
                if isinstance(item, CommitItem):
                    self.conn.commit()
                elif isinstance(item, BriefDeltaItem):
                    self.cursor.execute(self.update_brief, (item["seat_type"],
                                                            item["code"]))
                elif isinstance(item, StationNameItem):
                    self.cursor.execute(self.station_sql, (item["name"],
                                                           item["code"]))
                elif isinstance(item, BriefItem):
                    self.cursor.execute(self.brief_sql, (
                        item["code"],
                        item["train_no"],
                        item["start"],
                        item["end"],"null"))
                elif isinstance(item, InfoItem):
                    self.cursor.execute(self.info_sql, (
                        item["train_no"],
                        item["no"],
                        item["station"], item["type"],
                        item["start_time"], item["arrive_time"],
                        item["stopover_time"]))
                elif isinstance(item, TicketItem):
                    self.cursor.execute(self.tickets_sql, (item["train_no"],
                                                           item["start"], item["end"], item["swz"],
                                                           item["tz"], item["zy"], item["ze"],
                                                           item["gr"], item["rw"], item["yw"],
                                                           item["rz"], item["yz"], item["wz"],
                                                           item["qt"]))
                else:
                    pass
            except Exception as e:
                log.msg("excute sql fail.", log.WARNING)
                log.msg(str(e), log.WARNING)