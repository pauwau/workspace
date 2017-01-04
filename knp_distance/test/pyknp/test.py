#! /usr/bin/python
# -*- coding: utf-8 -*-


import sys,codecs,subprocess,readline,re,string
#import syori
#import ex_relates
#import frame_base,topic_base
from types import *
import time
from pyknp import KNP
#import word2vec

def clause_count(tmp_list):
## 節の数と各節が何行文の情報を持っているのか調べる関数    

    ## clause_numは節の数,リストclauseは各節が何行の情報を持っているか。
    clause_num = 0
    clause = []
    c_num = -1

    #print "-----------------------------"

    for tmp in tmp_list:
 
       
        if tmp == "*":   
            ## 前の節が何行分の情報を持っていたか。リストに追加する
            clause.append(c_num)
            
            ## c_numの数を初期化
            c_num = 1
            
            ## clause_numの数をひとつ増やす
            clause_num += 1
            
        ## 処理の都合上、最後の節はカウントできないので、無理やりだけど、こうする 
        elif tmp == "EOS\n":
            
            ## EOSの前には。、？！の記号しかないと仮定して-1する
            c_num = c_num - 1
            clause.append(c_num)

        else:            
            c_num += 1

    clause.pop(0)
    #print "Number of Clauses is",clause_num
    #print "List of lines in each clause",clause

    return clause_num,clause


def knp_tab(sentence,user_ID,knp):

    tmp_list = []
    clause_list = []

    # echo = subprocess.Popen(['echo',sentence],
    #                         stdout=subprocess.PIPE,
    #                         )


    # juman = subprocess.Popen(['juman'], 
    #                          stdin=echo.stdout,
    #                          stdout=subprocess.PIPE,
    #                          )


    # knp = subprocess.Popen(['knp','-case','-tab'],
    #                        stdin = juman.stdout,
    #                        stdout=subprocess.PIPE,
    #                        )


    result = knp.parse(sentence)

    for tag in result.tag_list():
        print u"素性:%s" % (tag.fstring)

    # for tag in result.tag_list():
    #                                                                                                                                             line_split = line2.split(" ")
    #     tmp_list.append(line_split[0])
    #     clause_list.append(line)
    # #--------------------------------------
    # #ここで各処理関数に情報を投げる
    # clause_num, clause = clause_count(tmp_list)

    # print clause_list
    #文の情報を抽出。返ってくるのはリスト
    topic = ex_relates.Ex_relates(clause_list,clause_num,clause,user_ID)


    #フレームベース発話の生成
    #dist = frame_base.frame_base(user_ID,topic)
    #print dist

    #トピックベースの発話生成
    #topic_base.topic_base(topic)


if __name__ == '__main__':
    user_ID = 1
    sentence = u"太郎と次郎は世界を救った。"
    end_flag = False
    knp = KNP()
    while(end_flag == False):
        #sentence = raw_input("→")
        start = time.time()
        #sentence = ("")
        if (sentence == ""):
            endflag = True
            print "お話出来て、楽しかったです。"
            sys.exit()
        knp_tab(sentence,user_ID,knp)
        print "time :" + str(time.time() - start)
    sys.exit()
    


