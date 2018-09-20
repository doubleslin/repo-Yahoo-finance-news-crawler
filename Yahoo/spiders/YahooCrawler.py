#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 13 22:16:37 2018

@author: doubles
"""

import scrapy
from bs4 import BeautifulSoup
from Yahoo.items import YahooItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class YahooCrawler(CrawlSpider):
    name = 'yahoo'

    symbol = 0
    start_urls = ['https://tw.stock.yahoo.com/q/h?s=' + str(1216),
                  'https://tw.stock.yahoo.com/q/h?s=' + str(1227),
                  'https://tw.stock.yahoo.com/q/h?s=' + str(1262),
                  'https://tw.stock.yahoo.com/q/h?s=' + str(1301),
                  'https://tw.stock.yahoo.com/q/h?s=' + str(1303),
                  ]

    rules = [
        Rule(LinkExtractor(allow=('s=' + str(1216) + '&pg=.*$')), callback='parse_list', follow=True),
        Rule(LinkExtractor(allow=('s=' + str(1227) + '&pg=.*$')), callback='parse_list', follow=True),
        Rule(LinkExtractor(allow=('s=' + str(1262) + '&pg=.*$')), callback='parse_list', follow=True),
        Rule(LinkExtractor(allow=('s=' + str(1301) + '&pg=.*$')), callback='parse_list', follow=True),
        Rule(LinkExtractor(allow=('s=' + str(1303) + '&pg=.*$')), callback='parse_list', follow=True),
    ]
    # start_urls = ['https://tw.stock.yahoo.com/q/h?s=' + str(symbol),
    #               ]
    # rules = [
    #     Rule(LinkExtractor(allow=('s=' + str(symbol) + '&pg=[1-2]$')), callback='parse_list', follow=True),
    # ]

    def parse_list(self, response):
        domain = 'https://tw.stock.yahoo.com'
        res = BeautifulSoup(response.text)
        data = res.find_all('table')[8]


        # 標題
        # title = data.find_all('td')[1].text

        link_size = len(data.find_all('a'))
        for i in range(link_size):
            sym_tb = res.find_all('table')[4]
            self.symbol = sym_tb.find_all('td')[0].text[0:4]

            link = domain + data.find_all('a')[i]['href']
            # print(link)
            yield scrapy.Request(link, self.parse_detail)

    def parse_detail(self, response):
        res = BeautifulSoup(response.text)
        data = res.find('td', {'class', 'yui-text-left'})
        title = data.find('h1', {'class', 'mbody1 style1'}).text.strip()
        com = data.find_all('span', {'class', 't1'})[1].text.strip().split(' ')[0]

        # string time to timestamp
        str_Time = data.find_all('span', {'class', 't1'})[0].text.strip()+':00'

        tag_p_size = len(data.find_all('p'))
        tag_br_size = len(data.find_all('br'))
        content = ''

        if tag_p_size >= tag_br_size:
            for i in range(tag_p_size):
                content += data.find_all('p')[i].text.strip()
            content = content.replace('\n', '').strip()
            # print(content)
            # print(title + ' , ' + time + ' , ' + post)
        else:
            content = data.text
            content = content.replace(title, '')
            content = content.replace(str_Time, '')
            content = content.replace(com, '')
            content = content.replace('\n', '').strip()
            # print(content)
            # print(title + ' , ' + time + ' , ' + post)

        yahooItem = YahooItem()
        yahooItem['stockno'] = self.symbol
        yahooItem['title'] = title
        yahooItem['t'] = str_Time
        yahooItem['com'] = com
        yahooItem['content'] = content
        return yahooItem