#!/usr/bin/python
# -*- coding: utf-8 -*-
# python_twitter 1.1

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

if __name__ == '__main__':
	f = open('filtered2_dialogue.txt', 'w')
	conn = sqlite3.connect("filtered2.db")
	cur = conn.cursor()
	wcur = conn.cursor()
	end = False
	offset = 0
	line_num = cur.execute("select count(*) from c_short").fetchone()[0]
	while(offset * 100 < line_num):
		try:
			lines = cur.execute( "select idstr from c_short WHERE repto = 0 LIMIT " + str(offset + 100) + " OFFSET " + str(offset)).fetchall()
		except:
			print("accept DB error.")
			end = True
		for line in lines:
			line = garbage_strip(str(line))
			id_list = line.split(",")
			id_list.reverse()
			for tweet_id in id_list:
				#print(id_list)
				flag = 0
				slines = wcur.execute( "SELECT sentence FROM c_short WHERE tweet_id=" + str(tweet_id) ).fetchall()
				for sentence in slines:
					if (flag == 1):
						break
					string = garbage_strip(str(sentence))
					print (string)
					f.write(string+ "\n")
					flag = 1
			else:
				f.write("\n")
		print("process " + str((float(offset * 100) / line_num) * 100) + "% finished") 
		offset = offset + 1
	print(line_num)
	print("process end")