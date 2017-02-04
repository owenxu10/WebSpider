# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from medlive.items import MedliveItem 

#1001-1743
class MedlivespiderSpider(scrapy.Spider):
    name = "medliveSpider"
    allowed_domains = ["http://disease.medlive.cn/wiki/"]
    start_urls = ['http://disease.medlive.cn/wiki/essentials_10001001']
    base_url = 'http://disease.medlive.cn'
    number = 10001001

    def parseText(self,response):
    	# $('div .editor_mirror >ul')[0].innerText
    	name = response.meta['name']
    	subname = response.meta['subname']
    	print response.url
    	soup = BeautifulSoup(response.text,'lxml')
    	text = soup.select("div .knw_thorough > div .bd")[0].text
    	item = MedliveItem()
    	item['name'] = name
    	item['subname'] = subname
    	item['desc'] = text
    	yield item

    def parse(self, response):
    	print response.url
        soup = BeautifulSoup(response.text,'lxml')
        title = soup.select("div .hd > h3")[0]
        #print title
        name = title.span.text
        name = name[0:name.index(' ')]
        #print name

        chapters = soup.select("div .chapter > dl > dd > a")
        for chapter in chapters:
        	if (chapter.get('class') is not None) and (chapter.get('class')[0] == u"nodata"):
        		# print chapter.get('class')[0]
        		continue
        	else:
        		url = self.base_url + chapter.get('href')
        		subname = chapter.text
	        	yield scrapy.Request(url, meta = {'name' : name,'subname' : subname}, 
							 callback=self.parseText, dont_filter=True )
		self.number += 1
		nexturl = self.base_url + "/wiki/essentials_" + str(self.number)
		print self.number
		yield scrapy.Request(nexturl, callback=self.parse, dont_filter=True )

	    

