# -*- coding: utf-8 -*-
import scrapy
from medsci.items import MedsciItem 

class MedscisSpider(scrapy.Spider):
    name = "medscis"
    allowed_domains = ["tools.medsci.cn"]
    start_urls = [ 
    			    # 'http://tools.medsci.cn/cal/speclass?class=1']
    			   'http://tools.medsci.cn/cal/sysclass?class=6']

    def parseDetail(self, response):
    	print response.url
    	cate = response.meta['cate']  
    	item = MedsciItem()
        for sel in response.xpath('/html/body/div[@class=\'f_page_cont spe_content\']/div[@id=\'id_f_page_cont_r\']/div[@class=\'f_page_cont_box f_m0\']/div[@class=\'f_results_line\']'):
        		item['cate'] = cate
        		item['desc'] = sel.xpath('p[2]/text()').extract_first()
        		item['title'] = sel.xpath('p[1]/a/text()').extract_first()
        		yield item

    def parse(self, response):
    	for sel in response.xpath('/html/body/div[@class=\'f_page_cont spe_content\']/div[@class=\'f_page_cont_l m_p_c_l\']/div[@id=\'class_nav\']/ul/li/a'):
	    	url = sel.xpath('@href').extract_first()
	    	cate = sel.xpath('text()').extract_first()
	    	yield scrapy.Request(url,meta={'cate': cate},  callback=self.parseDetail)

   		