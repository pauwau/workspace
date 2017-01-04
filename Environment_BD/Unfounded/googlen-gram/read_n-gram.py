#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gzip
import re
filelist = ["2gm-0000","2gm-0001","2gm-0002","2gm-0003","2gm-0004","2gm-0005","2gm-0006","2gm-0007","2gm-0008"]
ksad = ["この","その","あの","どの"]
fo = open("test.txt","w")

for filename in filelist:
	fr = open(filename,"r")
	file_content = fr.readlines()
	for line in file_content:
		split = line.split(" ")
		if(split[0] in ksad):
			[word,num] = split[1].split("\t")
			if(not(re.search("[A-Za-z!-/:-@[-`{-~0-9！”＃＄％＆’（）＝〜｜｛｝＊＋｀＜＞？＿]",word))):
				fo.write(word + ":" + num)
