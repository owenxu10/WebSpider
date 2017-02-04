#!/usr/bin/python
# -*- coding: UTF-8 -*-

# http://dict.bioon.com/hot.shtml

import urllib2
import re
import time

urlbase = 'http://dict.bioon.com'

urlindex = urlbase + '/hot.shtml'

urlarr = []

r =  urllib2.urlopen(urlindex)

# find page
# elite\.asp\?classid=(.\d*)
# elite\.asp\?classid=(.\d*).*>(.*[\u4e00-\u9fa5])<
regex = "elite\.asp\?classid=(.\d*)"
matches = re.findall(regex,r.read())

#get urls
for match in matches:
	url = urlbase+'/elite.asp?classid='+match
	urlarr.append(url)	

#detail from url
for url in urlarr:

	#get title
	time.sleep(5)
	r2 = urllib2.urlopen(url)
	regex2 = r"医药生物百科/知道</a> : (.*)"
	webpage = r2.read()
	matches = re.finditer(regex2, webpage)

	for match in matches:
		title = match.group(1)
		filename = title+'.txt'
		f = open(filename,"w+")
		f.write(title)
		f.write("\n")
		f.write("\n")
		print filename

	#get total pages
	regex3 = "(\d*)页"
	matches = re.findall(regex3, webpage)

	print webpage
	print matches
	#total pages
	pages = int(matches[0])+1

	#start crawl in one category
	for page in range(1,pages):
		
		requestURL = url + '&page='+ str(page)
		r3 = urllib2.urlopen(requestURL)

		webpage2 = r3.read()
		# print requestURL
		time.sleep(1)
		# print r3.read()

		regex4 = "worditem.*>(.*?)</a>"
		matches = re.findall(regex4, webpage2)
		print matches

		for match in matches:
			#write words
			f.write(match)
			f.write("\n")




