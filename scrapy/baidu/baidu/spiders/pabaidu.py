# -*- coding: utf-8 -*-
import scrapy
import sys
from bs4 import BeautifulSoup

class PabaiduSpider(scrapy.Spider):
    name = "pabaidu"
    allowed_domains = ["baidu.com"]
    # start_urls = ['https://zhidao.baidu.com/list?cid=115?fr=daohang']
    url_left = "https://zhidao.baidu.com/list?cid=115?fr=daohang&rn=30&pn="
    url_middle = 0
    url_right = "&_pjax=#j-question-list-pjax-container"


    def start_requests(self):
    	url = self.url_left+str(self.url_middle)+self.url_right
    	f = open("zhidao.txt","w+")
    	yield scrapy.Request( url, callback=self.parse)

    def parse(self, response):
    	reload(sys)                         
        sys.setdefaultencoding('utf-8')  
 
    	soup = BeautifulSoup(response.text,'lxml')
    	f = open("zhidao.txt","a")
    	questions = soup.select('div .question-title')
    	for question in questions:
    		print question
    		f.write(question.text.strip()+'\n\n')
    	self.url_middle += 30
    	url = self.url_left + str(self.url_middle) + self.url_right
    	if self.url_middle != 990:
    		yield scrapy.Request(url, callback=self.parse)