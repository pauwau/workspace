# coding:utf-8

import matplotlib.pyplot as plt
from wordcloud import WordCloud
from bs4 import BeautifulSoup
import requests
import MeCab as mc
import os
import math
import random

readfile = "test2_badwordlist_sim.txt"
outputfilename = "test2WordCloud_white"

def create_wordcloud(text):

    fpath = "/usr/share/fonts/FLOPDESIGN-FONT/FlopDesignFONT.otf"

    # ストップワードの設定
    # stop_words = [ 'てる', 'いる', 'なる', 'れる', 'する', 'ある', 'こと', 'これ', 'さん', 'して', \
    #          'くれる', 'やる', 'くださる', 'そう', 'せる', 'した',  '思う',  \
    #          'それ', 'ここ', 'ちゃん', 'くん', '', 'て','に','を','は','の', 'が', 'と', 'た', 'し', 'で', \
    #          'ない', 'も', 'な', 'い', 'か', 'ので', 'よう', '', 'れ','さ','なっ']
    stop_words = []
    wordcloud = WordCloud(background_color="white",font_path=fpath, width=1500, height=1200, \
                         stopwords=set(stop_words)).generate(text)

    #wordcloud = WordCloud(background_color="black", width=900, height=500, \
    #                      stopwords=set(stop_words)).generate(text)

    plt.figure(figsize=(15,12))
    plt.imshow(wordcloud)
    plt.axis("off")
#    plt.show()
    plt.savefig(outputfilename,bbox_inches="tight")
    
f = open(readfile,"r")
columnlist = f.read().split("\n")
wordAndScoreList = []
wordlist = []
for column in columnlist:
    if(column == None or column == ""):
        break
    if("#" not in column[0]):
        wordAndScoreList.append([column.split( )[1],column.split( )[2]])
for wordAndScore in wordAndScoreList:
    for i in range(1,math.floor(100*float(wordAndScore[1]))):
        wordlist.append(wordAndScore[0])
random.shuffle(wordlist)
create_wordcloud(" ".join(wordlist))