#!/usr/bin/python
# -*- coding: utf-8 -*-
# python_twitter 1.1
# 返信件数の上限下限の設定、および三人以上の
# ユーザー間の対話、不適切な発話の除去を行うプログラム

import sqlite3
import re

read_DB = "tweet_wordnum_729_100k_dia.db"
write_DB = "tweet_wordnum_801_100k_dia_filtered.db"
tablename = "c_short"
readNums = 10000

def table_init(writecur,tablename):
	try:
		writecur.execute("CREATE TABLE " + tablename + "(tweet_id serial,sentence text,\
			user_ID serial,repfrom serial,repto serial,idstr text,dialogue_id);")
	except sqlite3.OperationalError:
		writecur.execute("DROP TABLE " + tablename)
		writecur.execute("CREATE TABLE " + tablename + "(tweet_id serial,sentence text,\
			user_ID serial,repfrom serial,repto serial,idstr text,dialogue_id);")

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

def insert_db(data_lows,cur,tablename,dia_num,id_list):
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

	if(len(id_list) != len(id_list_tuples)):
		print("***********error*************")
	for data_tuple in id_list_tuples:
		[tweet_ID,sentence,user_ID,repfrom,repto,idstr] = data_tuple
		cur.execute("INSERT INTO " \
		+ tablename + "(tweet_id,sentence,user_ID,repfrom,repto,idstr,dialogue_id) \
		VALUES(%d,'%s',%d,%d,%d,'%s',%d)" \
		%(tweet_ID,sentence,user_ID,repfrom,repto,idstr,dia_num))

def judge_data(id_list,cut_id_list):
	good_tuple = True
	set_user_ID = set([])
	if(len(id_list) < 4):
		return False
	if(len(id_list) > 10):
		return False	
	for tweet_id in id_list:
		data_low = wcur.execute( "SELECT * FROM dialogue WHERE tweet_id=" + str(tweet_id) ).fetchone()
		[tweet_ID,sentence,user_ID,repfrom,repto,idstr] = data_low
		set_user_ID.add(user_ID)
		#print(tweet_id)
		#print(cut_id_list)
		if(re.search('(https?[\w|/|:|%|#|$|&|\?|\(|\)|~|\.|=|\+|\-]+?)',sentence)):
			return False
		if(len(set_user_ID) > 2 ):
			#print("not two user:" + sentence)
			return False
		if(re.search('拡散|募集|相互|支援|sougo|rt|RT|ＲＴ|follow|フォロ|ﾌｫﾛ|１００|100|％|%',sentence)):
			#print("get follower:" + sentence)
			return False
		if(re.search('[ 　]*(rt|RT|qt|QT)[ 　]*([“”].*”|@\S+?[ 　]*:?[ 　]*.*|(\S+)?:[ 　]*.*|“\S+$)|[ 　]*(rt|RT)[ 　]*$',sentence)):
			#print("retweet:" + sentence)
			return False
		if(re.search('[#＃][0-9A-Za-z_〃々ぁ-ゖ゛-ゞァ-ヺーヽヾ一-龥０-９Ａ-Ｚａ-ｚｦ-ﾟ]+',sentence)):
			#print("hash tag:" + sentence)
			return False
		if(re.search('bot|BOT|Bot',sentence)):
			#print("user_ID:" + sentence)
			return False
		# if(re.search("(うんち|うんこ|ウンチ|ウンコ|💩|ｳﾝｺ|ｳﾝﾁ|ちんこ|チンコ|ﾁﾝｺ|ちんぽ|チンポ|ﾁﾝﾎﾟ|まんこ|マンコ|ﾏﾝｺ|淫夢|乳首|性癖|アナル|ｱﾅﾙ|屁|死ね|ケツ|尻|おっぱい|巨乳|貧乳|オナニー|クソ|糞|くそ|えろ|エロ|パコ|前立腺|デリヘル|えっち|エッチ|アダルト|セックス|せっくす|セクロス|SEX|キス|痴漢|犯す|犯さ|早漏|卑猥)",sentence)):
		# 	#print ("dangerous:" + sentence)
		# 	return False
		if(tweet_id in cut_id_list):
			print  ("Overlap tweet_id:" + str(tweet_id))
			return False
	if(len(set_user_ID) < 2 ):
		#print("only_one user:" + sentence)
		return False
	return True

def make_string_id(line):
	line = garbage_strip(str(line))
	id_list = line.split(",")
	sql_idstr = ""
	for ID in id_list:
		if(sql_idstr == ""):
			first_idstr = ID
			sql_idstr = "idstr=\'" + ID + "\'"
			pre_idstr = ID
		else:
			pre_idstr = pre_idstr + "," + ID
			sql_idstr = sql_idstr + " OR " + "idstr=\'" + pre_idstr + "\'"
	#print (sql_idstr)
	return id_list,sql_idstr,first_idstr

if __name__ == '__main__':
	conn = sqlite3.connect(read_DB)
	cur = conn.cursor()
	wcur = conn.cursor()
	writeconn = sqlite3.connect(write_DB)
	writecur = writeconn.cursor()
	offset = 0
	dia_num = 1
	cut_id_list = []
	line_num = cur.execute("select count(*) from dialogue WHERE repto = 0 ").fetchone()[0]
	table_init(writecur,tablename)
	while(offset * readNums < line_num):
		lines = cur.execute( "select idstr from dialogue WHERE repto = 0 LIMIT " + str(readNums) + " OFFSET " + str(offset * readNums)).fetchall()
		#lines = cur.execute( "select idstr from has_reply WHERE repto = 0 LIMIT " + str(readNums) + " OFFSET " + str(offset * readNums)).fetchall()
		for line in lines:
			id_list,sql_idstr,cut_id = make_string_id(line)
			#print(str(id_list) + ":" + str(len(id_list)))
			#IDリストの長さが二以下で、次の行を見る。
			if(not judge_data(id_list,cut_id_list)):
				continue
			cut_id_list.append(cut_id)
			#print("tweet_id:" + str(tweet_id))
			#検索結果が２つ有れば、上にある方のものを取ってくる。
			data_lows = wcur.execute( "SELECT * FROM dialogue WHERE " + str(sql_idstr) ).fetchall()
			insert_db(data_lows,writecur,tablename,dia_num,id_list)
			dia_num = dia_num + 1
		print("process " + str(((offset * readNums) / line_num) * 100) + "% finished") 
		offset = offset + 1
		writeconn.commit()
	print(line_num)
	print("process end")
