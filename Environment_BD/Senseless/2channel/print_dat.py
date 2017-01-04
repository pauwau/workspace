#-*- coding: utf-8 -*-

import urllib
from lxml.html import fromstring
from urllib.request import urlopen
from collections import Counter, defaultdict
import MeCab
import sys,re

url = 'http://open.open2ch.net/uravip//board/dat/1441102863.dat'
doc = fromstring(urlopen(url).read().decode('utf-8', errors='ignore'))

req = urllib.request.Request(url)
with urllib.request.urlopen(req) as response:
   the_page = response.read()
print(url + "\n\n")
pageString = the_page.decode("Sjis")
sredList = pageString.split("\n")
print(sredList) 