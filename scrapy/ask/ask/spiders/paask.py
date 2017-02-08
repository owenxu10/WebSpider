# -*- coding: utf-8 -*-
import scrapy
import sys
from bs4 import BeautifulSoup

class PaaskSpider(scrapy.Spider):
    name = "paask"
    allowed_domains = ["www.120ask.com"]
    start_urls = ['http://www.120ask.com/list/tijianke/all/1']
    base_url = 'http://www.120ask.com/list/tijianke/all/'
    num = 1
    def parse(self, response):
        reload(sys)                         
        sys.setdefaultencoding('utf-8')  
        content = BeautifulSoup(response.text,'lxml')
        questions = content.select('div .h-left-p')
        for question in questions:
        	question_url = question.select('a')[0].get('href')
        	yield scrapy.Request(question_url, callback = self.parseQuestion)
        
        self.num += 1
        if self.num != 201:
        	url = self.base_url + str(self.num)
        	yield scrapy.Request(url, callback = self.parse)

    def parseQuestion(self, response):
    	content = BeautifulSoup(response.text, 'lxml')
    	question_id = response.url.split('/')[-1].split('.')[0]
    	filename = 'result/' + question_id + '.txt'
    	f = open(filename,'w+')
    	question_title = content.select('h1')[0].text
    	question_content = content.select('div .b_askcont')[0].text
    	f.write(question_title)
    	f.write(question_content)

    	question_responses = content.select('div.b_anscontc')
    	for question_response in question_responses:
    		response_content = question_response.select('div.b_anscont_cont')[0].text
    		f.write(u"医生回复:"+"\n")
    		f.write(response_content)

    		response_add_contents = question_response.select('div.b_ansaddbox')
    		if len(response_add_contents) != 0:
    			f.write(response_add_contents[0].text)