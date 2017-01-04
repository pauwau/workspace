#!/usr/bin/python
# -*- coding: utf-8 -*-
import sqlite3

read_file = "../data/twitter_id_append.txt"

f = open(read_file,"r")
# how many program finished
s = 0
sep_point = 0
count = 0
lines = f.readlines()

conn = sqlite3.connect('./sqlite.db')
cur = conn.cursor()
try:
	cur.execute("""CREATE TABLE corr2(post_id serial,comment_id serial,post text,comment text);""")
except sqlite3.OperationalError:
	print("---table corr already exist---")
	#cur.execute("""DROP TABLE corr;""")
	#cur.execute("""CREATE TABLE corr(post_id serial,comment_id serial,post text,comment text);""")

# detect correspondence from ID_list file
for index,line in enumerate(lines):
	tweet_dict = {}
	tweet_IDs = line.split(",")

	# remove \n from IDlist 
	for t in range(0,len(tweet_IDs)):
		tweet_IDs[t] = tweet_IDs[t].strip("\n")

	# # make associative array
	# for i in range(0,int(len(tweet_IDs)/2)):
	# 	tweet_dict.update({tweet_IDs[2*i]:tweet_IDs[(2*i)+1]})
	
	# detect value from DB
	cur.execute("select post_id,comment_id,post,comment from tweet")
	fetch = cur.fetchall()
	#print(sep_point)

	# search correspondence 
	for i in range(0,int(len(tweet_IDs)/2)):
		print(str(i + s) + "correspondence was found")
		post_id = tweet_IDs[2*i]
		comment_id = tweet_IDs[(2*i)+1]
		column = {"post_id":post_id,"comment_id":comment_id,"post":"","comment":""}
		#print("index : " + str(index) )
		sep=int(s/2)
#		print(type(sep))
		for fetch_column in fetch[sep_point:sep_point + 50]:
			[fetch_post_id,fetch_comment_id,fetch_post,fetch_comment] = fetch_column

			#search post by post_id
			if(int(post_id) == int(fetch_post_id)):
				column["post"] = fetch_post
			if(int(post_id) == int(fetch_comment_id)):
				column["post"] = fetch_comment
			#search comment by comment_id
			if(int(comment_id) == int(fetch_post_id)):
				column["comment"] = fetch_post
			if(int(comment_id) == int(fetch_comment_id)):
				column["comment"] = fetch_comment
			if(column["post"] != "" and column["comment"] != ""):
				sep_point = sep_point + 1
				break
		if(column["post"] == ""):
			print("text of post_id " + str(post_id) + " was not found.")
		if(column["comment"] == ""):
			print("text of comment_id " + str(comment_id) + " was not found.")
		# write correspondence to DB
		cur.execute("""INSERT INTO corr(post_id,comment_id,post,comment) VALUES(%d,%d,'%s','%s')"""\
				%(int(column["post_id"]),int(column["comment_id"]),column["post"],column["comment"]))
		conn.commit()
	print(tweet_dict)
	s = s + i + 1
cur.close()
