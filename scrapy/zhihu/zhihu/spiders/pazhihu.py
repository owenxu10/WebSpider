# -*- coding: utf-8 -*-
import scrapy
import time
import json
import sys
from PIL import Image
from bs4 import BeautifulSoup
from zhihu.items import ZhihuItem
from zhihu.myconfig import UsersConfig

class PazhihuSpider(scrapy.Spider):
	name = "pazhihu"
	allowed_domains = ["zhihu.com"]
	start_urls = ['https://www.zhihu.com']
	headers={
		"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
		"Accept-Language": "en,zh-CN;q=0.8,zh;q=0.6,en-US;q=0.4",
		"Connection": "keep-alive",
		"Host": "www.zhihu.com",
		"Upgrade-Insecure-Requests": "1",
		"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
	}
	login_url = 'https://www.zhihu.com/login/email'
	resource_url = "https://www.zhihu.com/topic/19856971/hot"
	base_url = "https://www.zhihu.com"
	post_url = "https://www.zhihu.com/node/QuestionAnswerListV2"
	question_links = set()
	question_posts = []

	def start_requests(self):
		yield scrapy.Request("https://www.zhihu.com",
							  headers = self.headers,
							  callback=self.get_xsrf)

	def get_xsrf(self, response):
		soup = BeautifulSoup(response.text, 'lxml')
		xsrf = soup.input['value']
		#if lang = cn, will be the other captcha in chinese chacter
		captcha_url = 'http://www.zhihu.com/captcha.gif?r=' + str(time.time() * 1000) + "&type=login" 
		yield scrapy.Request(
			url = captcha_url,
			headers = self.headers,
			meta = {'_xsrf': xsrf},
			callback = self.get_captcha
			)

	def get_captcha(self, response):
		with open('captcha.gif', 'wb') as f:
			f.write(response.body)
		f.close()
		image = Image.open('captcha.gif')
		image.show()
		print 'Please enter captcha: '
		captcha = raw_input()

		yield scrapy.FormRequest(
			url = self.login_url,
			headers = self.headers,
			formdata = {
				'email': UsersConfig['email'],
				'password': UsersConfig['password'],
				'_xsrf': response.meta['_xsrf'],
				'remember_me': 'true',
				'captcha': captcha
			},
			callback = self.after_login
		)

	def after_login(self, response):
		yield scrapy.Request(
			url = self.resource_url,
			headers = self.headers,
			callback = self.parse_hot
			)

	def parse_hot(self, response):
		json_content = ''
		try:
			json_content = json.loads(response.text)
		except ValueError,e:
			print " not json"
		if json_content == '':
			#response is not json type
			html_content = response.text
		else:
			#response is json type
			html_content =  json_content['msg'][1]
		
		soup = BeautifulSoup (html_content, 'lxml')

		questions = soup.find_all(class_='feed-item')
		for question in questions:
			question_link = question.select('h2 a')[0].get('href')
			question_title = question.select('h2 a')[0].text
			question_id = question_link.split('/')[-1]
			if question_link not in self.question_links:
				#new question
				question_url = self.base_url + question_link
				self.question_links.add(question.select('h2 a')[0].get('href'))
				print ">>question number:"
				print len(self.question_links)
				yield scrapy.Request(
					question_url, 
					headers = self.headers,
					meta={
					"title": question_title,
					"id": question_id ,
					},
					callback = self.parse_question)

		# #get last question of curret page 
		offset =  questions[-1]['data-score']
		print offset
		start = 0
		yield scrapy.FormRequest(self.resource_url,
					headers = self.headers,
					formdata={'start': str(start), 'offset': str(offset)},
					callback=self.parse_hot)

	def parse_question(self, response):
		reload(sys)
		sys.setdefaultencoding('utf-8')

		# print response.url
		soup = BeautifulSoup(response.text,'lxml')
		question_title =  response.meta['title']
		question_id =  response.meta['id']
		first_post = soup.select('div #zh-question-detail')[0].text
		question_record = {question_id : 0}
		self.question_posts.append(question_record)
		yield scrapy.FormRequest(self.post_url,
								headers = self.headers,
								formdata = {
									'method':'next',
									'params':"{\"url_token\":"+question_id+",\"pagesize\":10,\"offset\":0}"

								},
								meta={
									"id":question_id,
									"title":question_title,
									"first_post":first_post,
									"offset":0
									},
								callback = self.parse_posts)

	def parse_posts(self, response):
		question_id = response.meta['id']
		offset = response.meta['offset']
		current_question_post = { question_id : offset}

		print offset
		json_content = json.loads(response.text)
		posts = json_content['msg']

		if len(posts) != 0: 
			# new question
			new_question_post = {question_id:0}
			if( new_question_post in self.question_posts):
				print question_id
				f = open("result/"+ question_id +".txt","w+")
				# print response.meta['title']
				f.write(response.meta['title'])
				f.write(response.meta['first_post'])

			for post in posts:
				# print response.meta['id']
				soup = BeautifulSoup(post,'lxml')
				post_content = soup.select('div .zm-editable-content')[0].text
				f = open("result/"+ question_id +".txt","a")
				f.write(u"\n\n\n回答:\n")
				f.write(post_content)
				print post_content

			offset += 10
			for question_post in self.question_posts:
				if question_post == current_question_post:
					question_post[question_id] = offset

			yield scrapy.FormRequest(self.post_url,
									headers = self.headers,
									formdata = {
										'method':'next',
										'params':"{\"url_token\":"+ question_id +",\"pagesize\":10,\"offset\":"+ str(offset) +"}"
									},
									meta={"id":response.meta['id'],"offset":offset},
									callback = self.parse_posts)




