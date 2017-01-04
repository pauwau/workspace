#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import subprocess
import MeCab
#import commands as cmd

mecab = MeCab.Tagger("-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd -Owakati")

# テキスト -> 単語(形態素)集合
def text2bow(objlist,N):
    bow = []
    ngram = {}
    for obj in objlist:
        print ("read " + obj +  "\n")
        text = open(obj,"r").read()
        sptexts = text.split("。")
        for num,sptext in enumerate(sptexts):
            if((num % 100000) == 0):
                print(obj + " " + str((float(num) * 100)/len(sptexts)) + "% finished!\n")
            words = mecab.parse(sptext)
            if(words == None):
                continue
                words = words.replace('\n','')
            words = words.split(' ')
            for i in range(len(words)):
                cw = ""
                if i >= N-1:
                    for j in reversed(range(N)):
                        cw += words[i-j]
                else:
                    continue
                if(len(cw) < 20):
                    if(cw in ngram):
                        ngram[cw] = ngram[cw] + 1
                    else:
                        ngram[cw] = 1
    return ngram

# 出力
def output_Ngram(ngram,f):

    for i in ngram.items():
    	#print (i[0] + " : " + str(i[1]) + "\n")
        f.write(i[0] + " : " + str(i[1]) + "\n")

def main():
    inputfilenamelist = ["AA/wiki_00","AA/wiki_01","AA/wiki_02","AA/wiki_03","AA/wiki_04"]
    #inputfilenamelist = ["test.txt"]
    N = 3
    for i in range(3,4):
        output_filename = str(i) + "-gram.txt"
        f = open(output_filename,"w")

        # input: ファイルの場合
        print ("start readfile!")
        ngram = text2bow(inputfilenamelist,i)


        print ("start output n-gram!")
        output_Ngram(ngram,f)

if __name__ == "__main__":

    main()