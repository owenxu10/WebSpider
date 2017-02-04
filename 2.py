#!/usr/bin/python
# -*- coding: UTF-8 -*-

# http://pmmp.cnki.net/cdd/Laboratory/Lab_Detail.aspx?id=929&SearchType=2

import requests
import re

f2 = open("pmmp_cnki.txt","w+")
firstline = "检查项目 | 英文名 | 别名 | 分类 \n\n"
f2.write(firstline)
title = ""
ename = "" 
alias = ""
cate = ""

# 1182
for id in range(1,1182):
	print id
	urlindex = "http://pmmp.cnki.net/cdd/Laboratory/Lab_Detail.aspx?id="+ str(id) +"&SearchType=2"
	r = requests.get(urlindex)
	webpage = r.text.encode("utf-8")

	#title
	regex = "title\">(?:\s*)(.*)"
	matches = re.findall(regex,webpage)
	if ( len(matches) != 0 ): 
		title = matches[0].strip('\r\n')
		print title

		#english name
		regex_ename = "<a name=\"ename\"><span class=\"PreCaption\">英文名：(?:.*\s*){5}<span.*>(?:[&nbsp;]*)(.*)"

		matches = re.finditer(regex_ename, webpage)

		for match in matches:
		    ename = match.group(1).strip('\r\n')

		#alias
		regex_alias = "<a name=\"alias\"><span class=\"PreCaption\">别名：(?:.*\s*){5}<span.*>(?:[&nbsp;]*)(.*)"
		matches = re.finditer(regex_alias, webpage)
		alias = " "
		for match in matches:
		    alias = match.group(1).strip('\r\n')

		print alias

		#cate
		f=open("2.html","w+")
		regex_cate = "<a name=\"aclass\"><span class=\"PreCaption\">一级分类：(?:.*\s*){5}<span.*>(?:[&nbsp;]*)(.*)"

		matches = re.finditer(regex_cate, webpage)
		
		for match in matches:
		    cate = match.group(1)

		print cate
		content = title+' | '+ ename+ ' | '+alias+' | '+cate
		print content 
		f2.write(content)



f2.close()