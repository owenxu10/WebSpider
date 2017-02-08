# -*- coding: utf-8 -*-
import scrapy
import sys
from bs4 import BeautifulSoup

class Pa39Spider(scrapy.Spider):
    name = "pa39"
    allowed_domains = ["bbs.39.net"]
    start_urls = ['http://bbs.39.net/by/forum/2844-1-1.html',
				'http://bbs.39.net/by/forum/2844-1-2.html',
		    	'http://bbs.39.net/by/forum/2844-1-3.html',
		    	'http://bbs.39.net/by/forum/2844-1-4.html',
		    	'http://bbs.39.net/by/forum/2844-1-5.html',
		    	'http://bbs.39.net/by/forum/2844-1-6.html',
		    	'http://bbs.39.net/by/forum/2844-1-7.html',
		    	'http://bbs.39.net/by/forum/2844-1-8.html',
		    	'http://bbs.39.net/by/forum/2844-1-9.html',
		    	'http://bbs.39.net/by/forum/2844-1-10.html'
    	]
    base_url = "http://bbs.39.net"

    def parse(self, response):
    	reload(sys)                         
    	sys.setdefaultencoding('utf-8')

        content = BeautifulSoup(response.text,'lxml')
        titles = content.select('span .title a')
        # print len(titles)
        for title in titles:
        	# print title
        	topic_link = title.get('href')
        	url = self.base_url + topic_link
        	yield scrapy.Request(url,callback=self.parsePost)

    def parsePost(self, response):
    	post_id = response.url.split('/')[-1].split('.')[0]
    	filename = 'result/'+ post_id +'.txt'
    	f = open(filename, 'w+')
    	content = BeautifulSoup(response.text,"lxml")
    	post_title = content.select('a#atitle')
    	post_contents = content.select('div .con')
    	print post_id
    	f.write(post_title[0].text)
    	if(content.select('div .page > span')[-1].find('b') != None):
	    	if (content.select('div .page > span')[-1].find('b').next_sibling != None) :
	    		url = self.base_url + content.select('div .page > span')[-1].find('b').next_sibling.get('href')
	    		yield scrapy.Request(url,callback=self.parseNextPage,meta={'id':post_id})
    	for post_content in post_contents:
    		#print post_content
    		if len(post_content.select('div .main')) != 0:
    			if post_content.select('div .main')[0].get('id') != None:
    				f.write(post_content.select('div .time > span')[0].text + ":"+"\n")

    			f.write(post_content.select('div .main')[0].text+"\n\n")


    def parseNextPage(self, response):
    	filename = 'result/'+ response.meta['id']+'.txt'
    	f = open(filename, 'a')

    	content = BeautifulSoup(response.text,"lxml")

    	post_contents = content.select('div .con')
    	
    	if (content.select('div .page > span')[-1].find('b').next_sibling != None):
    		url = self.base_url + content.select('div .page > span')[-1].find('b').next_sibling.get('href')
    		yield scrapy.Request(url,callback=self.parseNextPage,meta={'id':response.meta['id']})
    	for post_content in post_contents:
    		#print post_content
    		if len(post_content.select('div .main')) != 0:
    			if post_content.select('div .main')[0].get('id') != None:
    				f.write(post_content.select('div .time > span')[0].text + ":"+"\n")

    			f.write(post_content.select('div .main')[0].text+"\n\n")

