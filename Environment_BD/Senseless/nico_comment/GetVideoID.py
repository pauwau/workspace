# -*- coding: utf-8 -*-

from urlparse import parse_qs
import NiconicoSnapshotAPIWrapper
from NiconicoSnapshotAPIWrapper import *
import time
import sqlite3

def InitVideoIDTable(cur,tablename):
	try:
		cur.execute("""CREATE TABLE '%s'(VideoID text,tag text);"""%tablename)
	except sqlite3.OperationalError:
		cur.execute("DROP TABLE '%s'"%tablename)
		cur.execute("""CREATE TABLE '%s'(VideoID text,tag text)"""%tablename)
	return

def MakeVideoIDdb(output_db,EachTagVideoNumber,index_tablename,CategoryTagList):
	conn = sqlite3.connect(output_db)
	cur = conn.cursor()
	InitVideoIDTable(cur,index_tablename)

	api = NiconicoSnapshotAPIWrapper('NiconicoSnapshotAPIWrapper')
	VideoIDList = []
	VideoIDIndexList = []
	for i,CategoryTag in enumerate(CategoryTagList):
		try:
			response  = api.query(CategoryTag,size = EachTagVideoNumber, sort_by = 'comment_counter')
			for j,DividedResponse in enumerate(response[1]):
				time.sleep(3)
				if(not DividedResponse[u"cmsid"] in VideoIDList):
					VideoIDList.append(DividedResponse[u"cmsid"])
					VideoIDIndexList.append(i-1)
				print("VideoIDList processing %f%% finished..." \
					%((float(i*EachTagVideoNumber + j)/(len(CategoryTagList*EachTagVideoNumber))*100)))
		except:
			print("trouble ocurred in " + CategoryTag)
	for i,VideoID in enumerate(VideoIDList):
		cur.execute("""INSERT INTO \
					'%s'(VideoID,tag) \
					VALUES('%s','%s')"""%(index_tablename,str(VideoID),\
						CategoryTagList[VideoIDIndexList[i-1]].encode("utf_8")))
	conn.commit()
	conn.close()


if __name__ == '__main__':
	output_db = "TestNiconicoComment.db"
	EachTagVideoNumber = 30
	index_tablename = "TestINDEX"
	CategoryTagList = [u"エンターテイメント",u"音楽",u"歌ってみた",\
u"演奏してみた",u"踊ってみた",u"VOCALOID",u"ニコニコインディーズ",\
u"動物",u"料理",u"自然",u"旅行",u"スポーツ",u"ニコニコ動画講座",u"車載動画",u"歴史",\
u"科学",u"ニコニコ技術部",u"ニコニコ手芸部",u"作ってみた",u"政治",\
u"アニメ",u"ゲーム",u"東方",u"アイドルマスター",u"ラジオ",u"描いてみた",\
u"例のアレ",u"その他",u"ファッション"
]

	MakeVideoIDdb(output_db,EachTagVideoNumber,index_tablename,CategoryTagList)		