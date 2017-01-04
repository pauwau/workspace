#-*- coding: utf-8 -*-

import json
import re

read_file_list = []

ID_higher_limit = 17500
ID_lower_limit = 1
dateDIR = "2ch_corpus"
fw = open('readjsonFileIDList.txt', 'w')
for ID in range(ID_lower_limit,ID_higher_limit):
	ID = str(ID)
	try:
		f = open(dateDIR + "/sred" + ID +'.json', 'r')
	except:
		print ID  + " is not found"
		continue
	read_file_list.append(ID)

for i in read_file_list:
	fw.write(i + ",")