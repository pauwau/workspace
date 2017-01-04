#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

file_name = sys.argv[1]

fr = open( file_name , 'r')
file_name = file_name.replace(".txt","")
fo = open( "append_" + file_name + ".txt","w")
id_list = []

lines = fr.read()
#各IDごとに分割する
split_lines = lines.split('\r\n')
for line in split_lines:
	line = line.split(",")
	id_list.extend(line)

if(id_list[-1] == ""):
	id_list = id_list[0:-1]
#print id_list

#100個のIDを横に並べて書き込んでいく

count = 1
for a_id in id_list:
	if(not count >= 100):
		fo.write(a_id + ",")
	else:
		fo.write(a_id + "\n")
		count = 0
	count = count + 1