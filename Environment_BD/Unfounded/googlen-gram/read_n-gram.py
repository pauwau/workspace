#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gzip
import re
filelist = ["2gm-0000","2gm-0001","2gm-0002","2gm-0003","2gm-0004","2gm-0005","2gm-0006","2gm-0007","2gm-0008"]
#readfile = "2gm"
ksad = ["この","その","あの","どの"]
fo = open("ksadnum.txt","w")
gramLines = open("1gm.txt","r").read().split("\n")
gramLines.pop()

length = len(filelist)
for i,readfile in enumerate(filelist):
	print (str(100 * float(i)/length) + "% finished...")
	fr = open(readfile,"r")
	file_content = fr.readlines()
	for i,firstLine in enumerate(file_content):
		split = firstLine.split(" ")
		if(split[0] in ksad):
			[abstword,denominator] = split[1].split("\t")
			#denominator = float(denominator)
			# if(not(re.search("[\\A-Za-z!-\/:-@\[-`\{-~0-9¥]",abstword))):
			# 	Numerator = 0
			# 	for secondLine in gramLines:
			# 		secondSplit = secondLine.split(":")
			# 		if(not(re.search("[\\A-Za-z!-\/:-@\[-`\{-~0-9]",secondSplit[0]))):
			# 			#print abstword + " : " + secondSplit[0]
			# 			#print secondSplit[0] + " " + secondSplit[1]
			# 			try:
			# 				Numerator += float(secondSplit[1])
			# 			except:
			# 				Numerator += float(secondSplit[2])							
			# 			#print ("aaaaa")
			# 	#if(Numerator != 0):
			#fo.write(abstword + ":" + str(denominator / Numerator) + "\n")
			fo.write(abstword + ":" + str(denominator) + "\n")