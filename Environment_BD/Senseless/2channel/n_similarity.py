#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gensim.models import word2vec
import sys 
import os

writedir = "badword/"
writeFileNum = "badword2_Cut.txt"
readdir = "badword/"
#readFileNum = "test2_badwordlist.txt"
readFileNum = "sortedbadwordlist.txt"
modeldir = "2chWord2vecModel/"
modelNum = "sample.model"
Delimiter = "\n"
NearWordsNum = 30
#threshold = 0.5  #time of badwordlist1
threshold = 1.0 #time of badwordlist2

# 学習済みモデルのロード
model = word2vec.Word2Vec.load(modeldir + modelNum)

# 入力された単語から近い単語をn個表示する
def s(posi,outputlist, nega=[], n=NearWordsNum):
    cnt = 1 # 表示した単語の個数カウント用
    # 学習済みモデルから cos距離が最も近い単語n個(topn個)を表示する
    # f.write("##############" + posi[0] + "##############\n")
    try:
        result = model.most_similar(positive = posi, negative = nega, topn = n)
    except:
        return    

    for r in result:
        if (str(r[0]) in outputdict):
            outputdict[str(r[0])] = outputdict[str(r[0])] + r[1]
        else:
            outputdict[str(r[0])] = r[1]
        # f.write(str(cnt) + ' ' + r[0] + ' ' + str(r[1]) + '\n')
        cnt += 1
    # print(len(outputlist))
    # print("##################################\n")


if __name__ == '__main__':
    outputdict = {}
    f = open(readdir + writeFileNum,"w")
    fr = open(readdir + readFileNum,"r")
    badwordlist = fr.read().split(Delimiter)
    for badword in badwordlist:
        #word = sys.argv[1]
        #word = unicode(word, 'utf-8')
        if(badword != "\n" and badword != ""):
            s([badword],outputdict)
    outputdict = sorted(outputdict.items(), key=lambda x: x[1])
    outputdict.reverse()
    for o in outputdict:
        if(o[1] > 1.0):
            f.write(o[0] + "\n")
        #f.write(o[0] + ":" + str(o[1]) + "\n")
