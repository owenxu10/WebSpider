# -*- coding: utf-8 -*-
import scrapy


class PabaiduSpider(scrapy.Spider):
    name = "pabaidu"
    allowed_domains = ["baidu.com"]
    start_urls = ['http://baidu.com/']

    def parse(self, response):
        pass
