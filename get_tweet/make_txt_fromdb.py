#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3

def garbage_strip(string):
	#string  = string.replace("[","")
	#string  = string.replace("]","")
	string  = string.replace("(","")
	string  = string.replace(")","")
	#string  = string.replace("u","")
	string  = string.replace("u'","")
	string  = string.replace("'","")
	if(string[-1] == ","):
		string = string.rstrip(",")
	return string

def make_string_id(line):
	line = garbage_strip(str(line))
	id_list = line.split(",")
	id_list.reverse()
	sql_idstr = ""
	for ID in id_list:
		if(sql_idstr == ""):
			sql_idstr = "tweet_id=" + ID
		else:
			sql_idstr = sql_idstr + " OR " + "tweet_id = " + ID
	return id_list,sql_idstr

def sort_ids(data_lows,id_list,f,dia_num):
	id_list_tuples = []
	for tweet_id in id_list:
		flag = False
		for data_low in data_lows:
			if (data_low[0] == int(tweet_id)):
				id_list_tuples.append(data_low)
				flag = True
				break
		if(flag == False):
			print("###########error############")
			print("tweet_id is not found in dia_num:" + str(dia_num))
	for data_tuple in id_list_tuples:
		[tweet_ID,sentence,user_ID,repfrom,repto,idstr,dia_id] = data_tuple
		f.write(sentence)


if __name__ == '__main__':
	f = open('text.txt', 'w')
	conn = sqlite3.connect("filtered2_temp2.db")
	cur = conn.cursor()
	tablename = "c_short"
	line_num = cur.execute("select count(*) from " + tablename + " WHERE repto = 0 ").fetchone()[0]
	offset = 0
	dia_num = 1

	while(offset * 100 < line_num):
		lines = cur.execute( "select idstr FROM " + tablename + " WHERE repto = 0 LIMIT " + str(100) + " OFFSET " + str(offset * 100)).fetchall()
		for line in lines:
			id_list,sql_idstr = make_string_id(line)
			line = garbage_strip(str(line))
			id_list = line.split(",")
			id_list.reverse()
			#print(str(id_list) + ":" + str(len(id_list)))
			#IDリストの長さが二以下で、次の行を見る。
			data_lows = cur.execute( "SELECT * FROM " + tablename + " WHERE " + str(sql_idstr) ).fetchall()
			data_lows = sort_ids(data_lows,id_list,f,dia_num)
			f.write("\n")
			dia_num = dia_num + 1
		print("process " + str(((offset * 100) / line_num) * 100) + "% finished") 
		offset = offset + 1

	# raw_documents = []
	# for line in codecs.open(file_name, 'r', 'utf-8'):
	# 	raw_documents.append(line.rstrip())
