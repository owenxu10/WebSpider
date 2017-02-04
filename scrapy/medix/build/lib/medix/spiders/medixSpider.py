# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from medix.items import MedixItem 

class MedixspiderSpider(scrapy.Spider):
    name = "medixSpider"
    allowed_domains = ["www.medix.cn"]
    start_urls = ['http://www.medix.cn/Medix-Overview.aspx']
    base_url = "http://www.medix.cn/Module/Medication/WesternMedicine/"

    def parseDesc(self, response):
        code = response.meta['code']
        name = response.meta['name']
        medname = response.meta['medname']

        soup = BeautifulSoup(response.text,'lxml')
        desc = soup.find( class_ = "textDescription").text

        item = MedixItem()
        item['code'] = code
        item['name'] = name
        item['medname'] = medname
        item['text'] = desc
        yield item

    def parseDetail(self, response):
        #print response.url
        code = response.meta['code']
        name = response.meta['name']
        # print code
        # print name
        soup = BeautifulSoup(response.text,'lxml')
        lists = soup.find_all('a')
        for arr in lists:
            url = self.base_url + arr.get('href')
            medname = arr.text
            yield scrapy.Request(url, 
                meta={'code': code, 'name':name, 'medname':medname}, 
                callback=self.parseDesc)

    def parsePage(self,response):
        soup = BeautifulSoup(response.text,'lxml')
        lists = soup.find_all(colspan='3')
        for arr in lists:
            url = self.base_url + arr.previous_sibling.previous_sibling.a.get('href')
            code = arr.previous_sibling.previous_sibling.a.string
            name = arr.string
            # print url
            yield scrapy.Request(url, meta={'code': code, 'name':name}, callback=self.parseDetail)

    def after_login(self, response):
        # print response.body
        url = 'http://www.medix.cn/Module/Medication/WesternMedicine/Nav.htm'
        return scrapy.Request(url, callback=self.parsePage)

    def parse(self, response):
            return scrapy.FormRequest.from_response(response,
                        formdata={'txtUserName': 'owenxu10', 'txtPassword': '101010','btnLogin':'登录'},
                        callback=self.after_login)
        



        # f = open("h4.html","w+")
        # f.write(str(soup))
        # f.close()

