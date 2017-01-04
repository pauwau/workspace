# -*- coding: utf-8 -*-

import urllib2, cookielib
from urlparse import parse_qs
import re
import NiconicoCommentGetter
import NiconicoSnapshotAPIWrapper
from NiconicoSnapshotAPIWrapper import *
import time
import sqlite3
import sys

output_db = "NiconicoComment8_3.db"
tablenameText = "tablename100tags.txt"

CategoryTagList = [u"エンターテイメント",u"音楽",u"歌ってみた",\
u"演奏してみた",u"踊ってみた",u"VOCALOID",u"ニコニコインディーズ",\
u"動物",u"料理",u"自然",u"旅行",u"スポーツ",u"ニコニコ動画講座",u"車載動画",u"歴史",\
u"科学",u"ニコニコ技術部",u"ニコニコ手芸部",u"作ってみた",u"政治",\
u"アニメ",u"ゲーム",u"東方",u"アイドルマスター",u"ラジオ",u"描いてみた",\
u"例のアレ",u"その他",u"ファッション"
]

def InitCommentTable(cur,tablename):
	try:
		cur.execute("""CREATE TABLE '%s'(comment text,vpos serial,commentID serial);"""%tablename)
	except sqlite3.OperationalError:
		cur.execute("DROP TABLE '%s'"%tablename)
		cur.execute("""CREATE TABLE '%s'(comment text,vpos serial,commentID serial)"""%tablename)
	return

def InsertCommentdb(output_db,index_tablename):
	conn = sqlite3.connect(output_db)
	cur = conn.cursor()
	allelementnum = cur.execute("""SELECT count(*) FROM '%s';"""%(index_tablename)).fetchone()[0]
	cur.execute("""SELECT VideoID,tag FROM '%s';"""%(index_tablename))	
	for i,[VideoID,tag] in enumerate(cur.fetchall()):
		try:
			tablename = "comment_" + str(VideoID)
			InitCommentTable(cur,tablename)
			time.sleep(5)
			CommentGetter = NiconicoCommentGetter.NiconicoCommentGetter("ii.mmi.twitter@gmail.com","TOKI8\\nari")
			commentStatus = CommentGetter.get(VideoID)
			commentStatus = sorted(commentStatus, key=lambda x: x[1])
			for j,[comment,vpos] in enumerate(commentStatus):
				try:
					cur.execute("""INSERT INTO '%s'(comment,vpos,commentID)\
					 VALUES('%s',%d,%d)""" \
					%(tablename,comment,int(vpos),j))
				except sqlite3.OperationalError:
					cur.execute("""INSERT INTO '%s'(comment,vpos,commentID)\
					 VALUES('%s',%d,%d)""" 
					 %(tablename,"error",int(vpos),j))
				except:	
					print(comment)
					print("trouble ocurred in " + str(VideoID))
					print("Unexpected error:", sys.exc_info()[0])
					cur.execute("DROP TABLE '%s'"%tablename)
					break
			conn.commit()
			print("CommentDBList processing %f%% finished..." \
						%((float(i)/(allelementnum)*100)))

		except:
			print("trouble ocurred in " + str(VideoID.encode("utf_8")) + "," + str(tag.encode("utf_8")))
			pass
	conn.close()

if __name__ == '__main__':
	# output_db = "NiconicoComment8_4.db"
	# EachTagVideoNumber = 100
	# index_tablename = "INDEX"
	output_db = "TestNiconicoComment.db"
	index_tablename = "TestINDEX"

	InsertCommentdb(output_db,index_tablename)

