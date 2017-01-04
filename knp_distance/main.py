#! /usr/bin/python
# -*- coding: utf-8 -*-


import sys,codecs,subprocess,readline,re,string
#import syori
import ex_relates
import frame_base,topic_base
from types import *
import time
from pyknp import KNP
import word2vec


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
        #print u"素性:%s" % (tag.fstring)
        clause_list.append(tag.fstring.encode("utf-8"))

    # for c in clause_list:
    #     print c
    # for tag in result.tag_list():
    #                                                                                                                                             line_split = line2.split(" ")
    #     tmp_list.append(line_split[0])
    #     clause_list.append(line)
    # #--------------------------------------
    # #ここで各処理関数に情報を投げる
    # clause_num, clause = clause_count(tmp_list)

    # print clause_list
    #文の情報を抽出。返ってくるのはリスト
    topic = ex_relates.Ex_relates(clause_list,user_ID)


    #フレームベース発話の生成
    dist = frame_base.frame_base(user_ID,topic)
    print dist

    #トピックベースの発話生成
    #topic_base.topic_base(topic)


if __name__ == '__main__':
    user_ID = 1
    sentence = u"太郎と次郎は世界を救った。"
    end_flag = False
    knp = KNP()
    while(end_flag == False):
        #sentence = raw_input().decode("utf-8")
        start = time.time()
        #sentence = ("")
        if (sentence == ""):
            endflag = True
            print "お話出来て、楽しかったです。"
            sys.exit()
        knp_tab(sentence,user_ID,knp)
        print "time :" + str(time.time() - start)
        sys.exit()
    


