#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
low_limit = 500

N = "3"
readfile = N + "-gram.txt"
outfile = N + "-gramfilter.txt"
fr = open(readfile,"r")
fo = open(outfile,"w")

lines = fr.readlines()
for line in lines:
	if(" : " in line):
		element = line.split(" : ")
		if(int(element[1]) > low_limit and len(element[0]) > 2):
			fo.write(element[0] + " : " + element[1])
fo.close()