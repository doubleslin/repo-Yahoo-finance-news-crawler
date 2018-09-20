# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


# class YahooPipeline(object):
#     def process_item(self, item, spider):
#         return item

import  time
import pymysql
from scrapy import log
from Yahoo.items import YahooItem, WantogooItem
from Yahoo import settings

class YahooPipeline(object):

    def open_spider(self, spider):
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            port=3306,
            charset='utf8',
            use_unicode=True)
        self.cursor = self.connect.cursor()

    def close_spider(self, spider):
        self.connect.commit()
        self.connect.close()

    def process_item(self, item, spider):
        if isinstance(item, YahooItem):
            return self.handleYahoo(item, spider)
        if isinstance(item, WantogooItem):
            return self.handleWantgoo(item, spider)


    def handleYahoo(self, item, spider):
        try:
            sql = 'INSERT INTO TTLNEWS VALUES (%s, %s, %s, %s, %s);'
            val = (item['stockno'], item['t'], item['title'], item['com'], item['content'])
            self.cursor.execute(sql, val)
        except Exception as error:
            log(error)
        return item

    def handleWantgoo(self, item, spider):
        symbol_list = item['symbol_list']
        name_list = item['name_list']

        for (symbol, name) in zip(symbol_list, name_list):
            print(symbol.text.strip())
            print(name.text.strip())
            try:
                # 插入資料
                sql = "INSERT INTO STOCKSYMBOL VALUES (%s, %s);"
                val = (str(symbol.text.strip()), str(name.text.strip()))
                self.cursor.execute(sql, val)
                time.sleep(0.5)
            except Exception as error:
                pass
                # log(error)
        return item
