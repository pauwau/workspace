# -*- coding: utf-8 -*-

import re
import sqlite3
import time

CommentTextLowLimit = 100
CommentTextHighLimit = 5000000
EachCommentTextLowLimit = 3
TimeWindow = 2000 #ms

# def MakeVposRangeReq(vposlist):
# 	VposRangeList = []
# 	vposlist = sorted(vposlist)
# 	print vposlist
# 	for vpos in vposlist:
# 		VposRangeList = VposRangeList.append([vpos-TimeWindow,vpos+TimeWindow])
# 	for vposRange in VposRangeList:
# 		if(i == 1):

# 	return req

def InitEachCommetnTextTable(cur,tablename):
	try:
		cur.execute("""CREATE TABLE '%s'(CommentText text,num serial);"""%tablename)
	except sqlite3.OperationalError:
		cur.execute("DROP TABLE '%s'"%tablename)
		cur.execute("""CREATE TABLE '%s'(CommentText text,num serial)"""%tablename)
	return


def NearCountComment(db,IndexTablename,CountFileName,CommentTextTableName):
	print ("process start")
	f = open(CountFileName,"w")
	CommentText_TTNL = [] #TextTextNumList
	conn = sqlite3.connect(db)
	CommentTextCur = conn.cursor()
	IndexCur = conn.cursor()
	ElementCur = conn.cursor()
	# to print processing
	CommentTextNum = IndexCur.execute("""SELECT count(*) FROM '%s' WHERE num>=%d AND num<=%d;"""%(CommentTextTableName,CommentTextLowLimit,CommentTextHighLimit)).fetchone()[0]
	CommentTextCur.execute("""SELECT CommentText FROM '%s' WHERE num>=%d;"""%(CommentTextTableName,CommentTextLowLimit))	
	EachCommentTextCur = conn.cursor()
	print("Comment count start")
	# Comment Text roop
	for h,CommentText in enumerate(CommentTextCur.fetchall()):
		TextList = []
		TextNumList = []
		#print CommentText
		# Index Table roop
		IndexCur.execute("""SELECT VideoID,tag FROM '%s';"""%(IndexTablename))	
		for i,[VideoID,tag] in enumerate(IndexCur.fetchall()):
			vposlist = []
			#print i
			ElementTablename = "comment_" + str(VideoID)
			#print CommentText
			ElementCur.execute("""SELECT vpos FROM '%s' WHERE '%s'=comment;"""\
				%(ElementTablename,CommentText[0]))
			for vpos in ElementCur.fetchall():
				vposlist.append(vpos)
			for vpos in vposlist: 
				#print vpos[0]
				ElementCur.execute("""SELECT comment,commentID FROM '%s'\
					WHERE vpos>%d-%d AND vpos<%d+%d;"""\
					%(ElementTablename,vpos[0],TimeWindow,vpos[0],TimeWindow))
				for comment,commentID in ElementCur.fetchall():
					if(comment in TextList):
						TextNumList[TextList.index(comment)] = TextNumList[TextList.index(comment)] + 1 
					else:
						TextList.append(comment)
						TextNumList.append(1)
		TextTextNumList = zip(TextList,TextNumList)
		TextTextNumList = (sorted(TextTextNumList, key=lambda x: x[1]))
		TextTextNumList.reverse()
		CommentText_TTNL.append([CommentText[0],TextTextNumList])
		print("CountComment processing %f%% finished..." \
				%((float(h)/(CommentTextNum)*100)))	

	for CommentText,TextTextNumList in CommentText_TTNL:
		# tablename = CommentText
		# InitEachCommetnTextTable(EachCommentTextCur,tablename)
		f.write( "##############" + CommentText.encode("utf_8") + "##############\n")
		for Text,Num in TextTextNumList:
			if (Num > EachCommentTextLowLimit): 
				f.write(Text.encode("utf_8") + " : "  + str(Num) + "\n")
		# 		try:
		# 			TextCur.execute("""INSERT INTO '%s'(CommentText,num)\
		# 					 VALUES('%s',%d)""" %(CommentTextTableName,Text,Num))
		# 		except:
		# 			print ("error:" + Text + str(Num))
		# conn.commit()



if __name__ == '__main__':
	date = "8_9"
	#IndexTablename = "INDEX"
	ex = ""
	output_db = "NiconicoComment" + ex + date + ".db"
	#EachTagVideoNumber = 100
	index_tablename = "INDEX"
	CountFileName = "NearWordsCount" + ex + date + ".txt"
	# output_db = "TestNiconicoComment.db"
	# IndexTablename = "TestINDEX"
	CommentTextTableName = "CommentText"
	date = "8_7"
	ex = "ManyTag"
	output_db = "NiconicoComment" + ex + date + ".db"
	IndexTablename = "INDEX"
	CountFileName = "WordsCount3" + ex + date + ".txt"
	CommetnTextTableName = "CommentText"
	NearCountComment(output_db,IndexTablename,CountFileName,CommentTextTableName)