# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from med126.items import Med126Item 

class MedspiderSpider(scrapy.Spider):
    name = "medSpider"
    allowed_domains = ["http://m.med126.com/"]
    start_urls = ['http://m.med126.com/lunwen/zhongtu/?ClassID=16']
    base_url = 'http://m.med126.com/lunwen/zhongtu/'



    def parse(self, response):
    	print response.url
    	soup = BeautifulSoup(response.text,'lxml')
    	lists = soup.find_all('li')
    	sublists =  lists[1:len(lists)-1]
    	for list in sublists:
    		#print list
    		item = Med126Item()
    		item['number'] = list.span.text 
    		if list.a:
    			url = self.base_url + list.a.get('href')
    			print url
    			yield scrapy.Request(url , callback=self.parse,dont_filter=True)

    			item['name'] = list.a.text
    			yield item

    		else:
    			item['name'] = list.span.next_element.next_element
    			yield item

