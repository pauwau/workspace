# -*- coding: utf-8 -*-

Banwords = r"((ぱい)|(パイ)|(射精)|(中出し)|(エロ)|(ずり)|(♂)|(ぶりぶり)|(うんこ)|(うんち)|(タマキーン)|(ちんこ)|(ちんちん)|(妊娠)|(勃起)|(シコシコ)|(抜)|(SEX)|(孕)|(童貞)|(生理)|(処女)|(パンツ)|(ぱんつ)|(ﾊﾟﾝﾂ)|(萌)|(乳)|(オナ)|(しこしこ)|(ペニス)|(ぺにす)|(アナル)|(ドピュ)|(ﾄﾞﾋﾟｭ)|(マンすじ)|(クチュ)|(くちゅ)|(包茎)|(セックス)|(下着)|(まんこ)|(裸)|(おまん)|(おっき)|(モザイク)|(○))"
import sqlite3
import re
import unicodedata
WordNumLowLimit = 1
WordNumHighLimit = 10


#True: delete column..... False: No Delete
def JudgeColumn(comment):
	#print type(comment)
	try:
		unicodedata.normalize( 'NFKC', comment)
	except:
		return True
	SameCharg = re.compile(r"(.)\1{2,}").search(comment)
	OnlyAlphabetg = re.compile(r"\A\w*\Z").search(comment)
	NoJapaneseg = re.compile(r"[^\x01-\x7E\xA1-\xDF]").search(comment)
	Numberg = re.compile(r"[123456789]").search(comment)
	if(SameCharg):
		print "SameChar3,True:" + comment
		return True
	if(OnlyAlphabetg):
		print "OnlyAlphabet,True:" + comment
		return True
	if(not NoJapaneseg):
		print "NoJapanese,True:" + comment
		return True
	if(Numberg):
		print "Number,True:" + comment
		return True
	if(len(comment) <=WordNumLowLimit or len(comment) > WordNumHighLimit):
		print "Len of Comment bad,True:" + comment
		return True

	# process in str type
	comment = comment.encode("utf_8")
	OnlyNumg = re.compile(r"\A[０１２３３４５６７８９0-9\s]+\Z").search(comment)
	Bang = re.compile(Banwords).search(comment)
	if(Bang):
		print "Ban comment,True:" + comment
		return True
	if(OnlyNumg):
		print "Only Num,True:" + comment
		return True
	else:
		return False

def DeleteColumn(db,IndexTablename):
	conn = sqlite3.connect(db)
	IndexCur = conn.cursor()
	ElementCur = conn.cursor()
	allelementnum = IndexCur.execute("""SELECT count(*) FROM '%s';"""%(IndexTablename)).fetchone()[0]
	IndexCur.execute("""SELECT VideoID,tag FROM '%s';"""%(IndexTablename))	
	for i,[VideoID,tag] in enumerate(IndexCur.fetchall()):
		ElementTablename = "comment_" + str(VideoID)
		ElementCur.execute("""SELECT comment,vpos,commentID FROM '%s';"""%(ElementTablename))
		for comment,vpos,commentID in ElementCur.fetchall():
			if(JudgeColumn(comment)):
				ElementCur.execute("""DELETE FROM '%s'WHERE commentID=%d;"""%(ElementTablename,commentID))
		conn.commit()
		print("delete VideoIDList processing %f%% finished..." \
					%((float(i)/(allelementnum)*100)))


if __name__ == '__main__':
	date = "8_7"
	ex = "ManyTag"
	db = "NiconicoComment" + ex + date + ".db"
	EachTagVideoNumber = 100
	IndexTablename = "INDEX"
	CountFileName = "WordsCount" + ex + date + ".txt"
	# db = "TestNiconicoComment.db"
	# IndexTablename = "TestINDEX"
	DeleteColumn(db,IndexTablename)