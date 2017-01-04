# -*- coding: utf-8 -*-

import codecs
import re

word = u"人間"
f = codecs.open("3gm.txt","r","utf-8")
lines = f.readlines()
#wordlen = len(word)
end_flag = False

for i,line in enumerate(lines):
	if(word in line):
		line = re.split(r"[\t\s]",line)
		if(line[0] == word and int(line[3]) > 1000):
			print("%s %s %s\t%s"%(line[0],line[1],line[2],line[3]))
			#print("%s %s\t%s"%(line[0],line[1],line[2]))
			end_flag = True
	elif(end_flag):
		exit()

# fdict = codecs.open("2gmdict.txt","r","utf-8")
# dictlines = fdict.readlines()
# for dline in dictlines:
# 	if(word in dline):
# 		dline = re.split(r"[:\t\s]",dline)
# 		if(word == dline[0]):
# 			start_index = dline[1]
# 			end_index = dline[2]
# 			print start_index
# 			print end_index
# for i,line in enumerate(lines):
# 	if(i >= start_index and i <= end_index):
# 		print line[0] + " " + line[1] + "\t" + line[2]
