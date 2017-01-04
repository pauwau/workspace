#!/usr/bin/python
# -*- coding: utf-8 -*-
# python_twitter 1.1
# 返信件数の上限下限の設定、および三人以上の
# ユーザー間の対話、不適切な発話の除去を行うプログラム

import sqlite3
import re
import MeCab

read_DB = "tweet_wordnum_1229_100k.db"
tablename = "tweet"
badwordListdir = "badword/"
#badwordfilename = "badword2_Cut.txt"
badwordfilename = "sortedbadwordlist.txt"
writefilename = "SenselessUtteranse.txt"
readNums = 10000
maxUtteranceNum = 20
minUtteranceNum = 6
badwordlist = open(badwordListdir + badwordfilename,"r").read()
badwordlist = badwordlist.split("\n")
badwordlist.pop()
tagger = MeCab.Tagger("-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd -Owakati")

def atmarkDelete(sentence):
  sentence = re.sub(r'@[0-9a-zA-Z_]+', " ", sentence)
  return sentence

def judge_data(line):
	outputbadwordlist = []
	parsedLine = tagger.parse(line).split(" ")
	for badword in badwordlist:
		if(badword in parsedLine):
			outputbadwordlist.append(badword)
	return outputbadwordlist


if __name__ == '__main__':
	conn = sqlite3.connect(read_DB)
	cur = conn.cursor()
	offset = 0
	cut_id_list = []
	fw = open(writefilename,"w")
	lines = cur.execute( "select sentence from  " + tablename).fetchall()
	line_num = len(lines)
	#lines = cur.execute( "select idstr from has_reply WHERE repto = 0 LIMIT " + str(readNums) + " OFFSET " + str(offset * readNums)).fetchall()
	for dia_num,line in enumerate(lines):
		#IDリストの長さが二以下で、次の行を見る。
		outputbadwordlist = judge_data(line[0])
		#print (badword)
		if(outputbadwordlist != []):
			for badword in outputbadwordlist:
				fw.write(badword + " ")
			fw.write("\n" + line[0] + "\n\n") 
		#print("tweet_id:" + str(tweet_id))
		#検索結果が２つ有れば、上にある方のものを取ってくる。

		# if((dia_num % 100) == 0):
		# 	print("process " + str((float(dia_num) / len(lines)) * 100) + "% finished")
	offset = offset + 1
	print(line_num)
	print("process end")
