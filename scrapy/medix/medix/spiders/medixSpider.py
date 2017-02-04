# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from medix.items import MedixItem 

class MedixspiderSpider(scrapy.Spider):
    name = "medixSpider"
    allowed_domains = ["www.medix.cn"]
    start_urls = ['http://www.medix.cn/Medix-Overview.aspx']
    base_url = "http://www.medix.cn/Module/Library/MedicalJournal/"

    def parseDesc(self, response):
        desc_text = ''
        #print response.text
        code = response.meta['code']
        name = response.meta['name']

        soup = BeautifulSoup(response.text,'lxml')
        item = MedixItem()
        
        item['code'] = code
        item['name'] = name
        item['medname'] = soup.find(id="textTitle").text.strip()
        item['text'] = soup.find(class_="textDescription").text.strip()
        print item['text']
        yield item
                
                
    def parseDetail(self, response):
        #print response.url
        # print response.text
        code = response.meta['code']
        name = response.meta['name']
        pageurl = ''
        # print code
        # print name
        soup = BeautifulSoup(response.text,'lxml')
        lists = soup.find_all('a')

        pages = soup.find(id="ResultsPageDiv").find_all('a')
        for arr in lists:
            url = self.base_url + arr.get('href')
            yield scrapy.Request(url, 
                meta={'code': code, 'name':name}, 
                callback=self.parseDesc)

        for page in pages:
            search_url = "http://www.medix.cn/Module/Library/MedicalJournal/Search.aspx"
            if (page.text == u"下一页" ):
                pageurl = search_url + page.get('href')
                #print pageurl
                yield scrapy.Request(pageurl, 
                    meta={'code': code, 'name':name}, 
                    callback=self.parseDetail)

            

    def parsePage(self,response):

        soup = BeautifulSoup(response.text,'lxml')
        #print response.text
        lists = soup.find_all('tr',valign="top")
        for arr in lists:
            #print arr
            # url = self.base_url + arr.previous_sibling.previous_sibling.a.get('href')
            # code = arr.previous_sibling.previous_sibling.a.string
            # name = arr.string
            url = self.base_url + arr.a.get('href')
            code = arr.a.text
            name = arr.find_all('td')[2].text
            yield scrapy.Request(url, meta={'code': code, 'name':name}, callback=self.parseDetail)

    def after_login(self, response):
        # print response.body
        url = 'http://www.medix.cn/Module/Library/MedicalJournal/Nav.htm'
        return scrapy.Request(url, callback=self.parsePage)

    def parse(self, response):
            return scrapy.FormRequest.from_response(response,
                        formdata={'txtUserName': 'owenxu10', 'txtPassword': '101010','btnLogin':'登录'},
                        callback=self.after_login)
        



        # f = open("h4.html","w+")
        # f.write(str(soup))
        # f.close()

