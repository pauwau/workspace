#coding:utf-8

import re,glob,MeCab
import lxml.html
import requests

# for file in glob.glob('aozorabunko-master/cards/*/files/*.html'):
#     print file, '-'*20
#     out_file = open("temp.txt",'a')
#     for line in open(file, 'r'):
#     	out_file.write(line)

for file in glob.glob('aozorabunko-master/cards/*/files/*.html'):
	print file, '-'*20
	out_file = open("temp2.txt",'a')
	lines = open(file, 'r').read()
	# rlines = lines.replace("\n","")
	# rlines = rlines.replace("<br />","")
	# rlines = rlines.replace("<ruby>","")
	# rlines = rlines.replace("</ruby>","")
	# rlines = rlines.replace("<rp>","")
	# rlines = rlines.replace("</rp>","")
	# rlines = rlines.replace("<rt>","")
	# rlines = rlines.replace("</rt>","")
	# rlines = rlines.replace("<rb>","")
	# rlines = rlines.replace("</rb>","")
	# rlines = rlines.replace("<span>","")
	# rlines = rlines.replace("</span>","")
	#print rlines
	#target_url = file
	#target_html = requests.get(target_url).text
	doc = lxml.html.fromstring(lines)
	#text_content()メソッドはそのタグ以下にあるすべてのテキストを取得する
	contents = doc.xpath('//div[@class="main_text"]')
	#contents = doc.xpath('//body')
	for content in contents:
		#for c in content:
		text = content.text_content()
	text = text.replace("\n","")
	p = re.compile(u'（\S+）')
	text2 = p.sub(u'',text)
	print text2
	t = text2.encode("utf-8")
	out_file.write(t)
