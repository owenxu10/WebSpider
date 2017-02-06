# -*- coding: utf-8 -*-
import scrapy

from bs4 import BeautifulSoup
from tianya.items import TianyaItem 

class PatianyaSpider(scrapy.Spider):
    name = "patianya"
    allowed_domains = ["bbs.tianya.cn/"]
    start_urls = ['http://bbs.tianya.cn/list.jsp?item=100&sub=14']
    base_url = "http://bbs.tianya.cn"

    def parse_post(self, response):
    	print response.url
    	item = TianyaItem()
    	item['title'] = response.meta['title']
    	item['author'] = response.meta['author']
    	item['click_number'] = response.meta['click_number']
    	item['response_number'] = response.meta['response_number']
    	item['response_time'] = response.meta['response_time']
    	soup = BeautifulSoup(response.text,'lxml')
    	contents = soup.select('div .bbs-content')
    	item['first_post'] = contents[0].text.strip()
    	contents.pop(0)
    	other_posts =''
    	for content in contents:
    		other_posts = other_posts + u"回复:"+ '\n' + content.text.strip() + '\n\n'
    	item['other_posts'] = other_posts
    	yield item

    def parse(self, response):
        print response.url
    	soup = BeautifulSoup(response.text,'lxml')
    	next_links = soup.select('div .links > a')
    	for link in next_links:
    		if(link.text == u'下一页'):
    			next_page = self.base_url + link.get('href')
    			yield scrapy.Request(next_page, callback = self.parse, dont_filter=True)

    	posts = soup.find_all('tr', class_='bg')
    	for post in posts:
    		title = post.select('td')[0].text.strip()
    		author = post.select('td')[1].text.strip()
    		click_number = post.select('td')[2].text.strip()
    		response_number = post.select('td')[3].text.strip()
    		response_time = post.select('td')[4].text.strip()
    		post_link = self.base_url + post.select('td > a')[0].get('href')

    		yield scrapy.Request(post_link, 
					    		meta={
					    			'title':title,
					    			'author':author,
					    			'click_number':click_number,
					    			'response_number':response_number,
					    			'response_time':response_time
				    			},
				    			callback = self.parse_post , dont_filter=True)
