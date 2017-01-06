#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
readfile = "2gm"
fo = open("1gm.txt","w")
fr = open(readfile,"r")

file_content = fr.readlines()
length = len(file_content)
preword = ""
sumNum = 0
for i,firstLine in enumerate(file_content):
	if( (i % 1000000) == 0):
		print (str(100 * float(i)/length) + "% finished...")
	[word,temp] = firstLine.split(" ")	
	[hoge,num] = temp.split("\t")
	if(not(re.search("[\\A-Za-z!-\/:-@\[-`\{-~0-9]",word))):
		if(word != preword):	
			fo.write(preword + ":" + str(sumNum) + "\n")
			sumNum = int(num)
		else:
			sumNum += int(num)
		preword = word
