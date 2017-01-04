# -*- coding: utf-8 -*-

import codecs
import re

#infile = "testin.txt"
infile = "2gm.txt"
outfile = "2gmdict.txt"
fr = codecs.open(infile,"r","utf-8")
fo = codecs.open(outfile,"w","utf-8")
lines = fr.readlines()
preword = ""
start_index = 0
for i,line in enumerate(lines):
	line = re.split(r"[\t\s]",line)
	word = line[0]
	if(word != preword):
		if(preword != ""):
			end_index = i
			fo.write("%s:%d %d\n"%(preword,start_index,end_index))
		preword = word
		start_index = i + 1

