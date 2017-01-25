#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests
import re

# file to be written to
# file = "通用公式.txt"
file2 = "webside.html"

r = requests.get('http://tools.medsci.cn/cal/common')

#open the file for writing
fh = open(file, "w")
fh2 = open(file2, "w")
fh2.write(r.text.encode("utf-8"))
fh2.close()

fh.write("通用公式")

regex = ("<span>(.*?)</span>")


matches = re.findall(regex, r.text)

for match in matches:
	print match.encode("utf-8")