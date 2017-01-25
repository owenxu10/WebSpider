# -*- coding: utf-8 -*-
from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from t.items import tItem


class tSPider(Spider):
    name = "t"
    allowed_domains = ["http://dict.bioon.com"]
    start_urls = [
        "http://dict.bioon.com/hot.shtml",
                
    ]

    def parse(self, response):
        # flag = 0;
        for sel in response.xpath('//table[3]/tr/td/table/tr/td'):
             item = tItem()
        #     # if flag == 0:
             item['title'] = sel.extract()
             # item['title'] = sel.xpath('a/span/text()').extract()
        # #     flag = 1
        # # else:
        #     item['year'] = sel.xpath('text()').extract()
        #         # flag = 0
             yield item