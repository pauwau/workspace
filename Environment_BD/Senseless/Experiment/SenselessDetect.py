#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gensim.models import word2vec
import MeCab

modeldir = "/home/pau/workspace/Environment_BD/Senseless/2channel/2chWord2vecModel/"
modelNum = "sample.model"
#made by pre research
badwordDic1 = "/home/pau/workspace/Environment_BD/Senseless/2channel/badword/prebadwordlist1.txt"
#made by human
badwordDic2 = "/home/pau/workspace/Environment_BD/Senseless/2channel/badword/prebadwordlist2.txt"
Dic1f = open(badwordDic1,"r").read().split("\n")
Dic2f = open(badwordDic2,"r").read().split("\n")
Diclist = [Dic1f,Dic2f]
Dic1f.pop()
Dic2f.pop()
tagger = MeCab.Tagger("-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd -Owakati")
# 学習済みモデルのロード
model = word2vec.Word2Vec.load(modeldir + modelNum)
testfile = open("writetest.txt","w")

def SenselessDetect(text):
	#print (Dic2f)
	scorelist = []
	simpleSumScore = 0
	squareSumScore = 0
	maxSumScore = 0
	NmaxSumScore = 0
	parseText = tagger.parse(text)
	TextLength = len(parseText)
	for dic in Diclist:
		for uttword in parseText:
			if(uttword in model):
				maxtemp = 0
				maxlist = [0,0,0]
				for badword in Dic2f:
					if(badword in model):
						simpleSumScore += model.similarity(uttword,badword)
						squareSumScore += (model.similarity(uttword,badword)) ** 2
						maxtemp = max(model.similarity(uttword,badword),maxtemp)
						maxlist.append(model.similarity(uttword,badword))
						maxlist.sort(reverse=True)
						maxlist.pop()
			else:
				pass
			maxSumScore += maxtemp
			NmaxSumScore += sum(maxlist)
		simpleSumScore = simpleSumScore / TextLength
		squareSumScore = squareSumScore / TextLength
		maxSumScore = maxSumScore / TextLength
		NmaxSumScore = NmaxSumScore / TextLength
		scorelist.append([simpleSumScore,squareSumScore,maxSumScore,NmaxSumScore])
	return scorelist

if __name__ == '__main__':
	text = "貴方は馬鹿ですね"
	scorelist = SenselessDetect(text)
	testfile.write(text + "\n" + "Dic1" + str(scorelist[0]) + "\n" + "Dic2" + str(scorelist[1]) + "\n\n")
	text = "ご飯がすすむなぁー！"
	scorelist = SenselessDetect(text)
	testfile.write(text + "\n" + "Dic1" + str(scorelist[0]) + "\n" + "Dic2" + str(scorelist[1]) + "\n\n")
	text = "どうして人間は愚かなの？"
	scorelist = SenselessDetect(text)
	testfile.write(text + "\n" + "Dic1" + str(scorelist[0]) + "\n" + "Dic2" + str(scorelist[1]) + "\n\n")
	text = "こなぁぁーーーゆきぃぃーーーねぇねぇ、さっきまで降ってなかったじゃん"
	scorelist = SenselessDetect(text)
	testfile.write(text + "\n" + "Dic1" + str(scorelist[0]) + "\n" + "Dic2" + str(scorelist[1]) + "\n\n")
	text = "お前はいい奴だなぁ"
	scorelist = SenselessDetect(text)
	testfile.write(text + "\n" + "Dic1" + str(scorelist[0]) + "\n" + "Dic2" + str(scorelist[1]) + "\n\n")
	exit()