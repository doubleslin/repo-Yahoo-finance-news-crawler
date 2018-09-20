# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class YahooItem(scrapy.Item):
    # define the fields for your item here like:
    stockno = scrapy.Field()
    title = scrapy.Field()
    t = scrapy.Field()
    com = scrapy.Field()
    content = scrapy.Field()
    # pass


class WantogooItem(scrapy.Item):
    # define the fields for your item here like:
    symbol_list = scrapy.Field()
    name_list = scrapy.Field()
    # pass