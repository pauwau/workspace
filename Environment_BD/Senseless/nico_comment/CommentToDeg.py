# -*- coding: utf-8 -*-

import re
import sqlite3
import time

def InitCommetnTextTable(cur,tablename):
	try:
		cur.execute("""CREATE TABLE '%s'(CommentText text,num serial);"""%tablename)
	except sqlite3.OperationalError:
		cur.execute("DROP TABLE '%s'"%tablename)
		cur.execute("""CREATE TABLE '%s'(CommentText text,num serial)"""%tablename)
	return

def CountComment(db,IndexTablename,CommetnTextTableName):
	TextList = []
	TextNumList = []
	conn = sqlite3.connect(db)
	IndexCur = conn.cursor()
	ElementCur = conn.cursor()
	TextCur = conn.cursor()
	InitCommetnTextTable(TextCur,CommetnTextTableName)
	allelementnum = IndexCur.execute("""SELECT count(*) FROM '%s';"""%(IndexTablename)).fetchone()[0]
	IndexCur.execute("""SELECT VideoID,tag FROM '%s';"""%(IndexTablename))	
	for i,[VideoID,tag] in enumerate(IndexCur.fetchall()):
		ElementTablename = "comment_" + str(VideoID)
		ElementCur.execute("""SELECT comment,vpos,commentID FROM '%s';"""%(ElementTablename))
		for comment,vpos,commentID in ElementCur.fetchall():
			if(comment in TextList):
				#print comment
				TextNumList[TextList.index(comment)] = TextNumList[TextList.index(comment)] + 1 
			else:
				if(comment != u"1"):
					TextList.append(comment)
					TextNumList.append(1)
				else:
					print "######################"

		print("CountComment processing %f%% finished..." \
					%((float(i)/(allelementnum)*100)))	
	TextTextNumList = zip(TextList,TextNumList)
	TextTextNumList = (sorted(TextTextNumList, key=lambda x: x[1]))
	TextTextNumList.reverse()
	#print TextTextNumList
	for Text,Num in TextTextNumList:
		if (Num > 1): 
			try:
				TextCur.execute("""INSERT INTO '%s'(CommentText,num)\
						 VALUES('%s',%d)""" %(CommentTextTableName,Text,Num))
			except:
				print ("error:" + Text + str(Num))
	conn.commit()

if __name__ == '__main__':
	output_db = "TestNiconicoComment.db"
	IndexTablename = "TestINDEX"
	CommentTextTableName = "CommentText"
	date = "8_7"
	ex = "ManyTag"
	output_db = "NiconicoComment" + ex + date + ".db"
	EachTagVideoNumber = 100
	IndexTablename = "INDEX"
	CountFileName = "WordsCount" + ex + date + ".txt"
	CommetnTextTableName = "CommentText"
	CountComment(output_db,IndexTablename,CommentTextTableName)