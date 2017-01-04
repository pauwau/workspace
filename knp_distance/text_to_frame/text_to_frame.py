#! /usr/bin/python
# -*- coding: utf-8 -*-


import sys,codecs,subprocess,readline,re,string
import ex_relates
import frame_base
from types import *
#import word2vec
file_name = "ex2"
input_file = "text/" + file_name
output_file = "frame/" + file_name

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


def knp_tab(sentence,lineid):

    tmp_list = []
    clause_list = []

    echo = subprocess.Popen(['echo',sentence],
                            stdout=subprocess.PIPE,
                            )


    juman = subprocess.Popen(['juman'], 
                             stdin=echo.stdout,
                             stdout=subprocess.PIPE,
                             )


    knp = subprocess.Popen(['knp','-case','-tab'],
                           stdin = juman.stdout,
                           stdout=subprocess.PIPE,
                           )


    end_of_pipe_tab = knp.stdout

    for line in end_of_pipe_tab:
        line_split = line.split(" ")
        tmp_list.append(line_split[0])
        clause_list.append(line)
    
    echo.stdout.close()
    juman.stdout.close()
    knp.stdout.close()
    
    #--------------------------------------
    #ここで各処理関数に情報を投げる
    clause_num, clause = clause_count(tmp_list)

    #文の情報を抽出。返ってくるのはリスト
    topic = ex_relates.Ex_relates(clause_list,clause_num,clause,lineid,output_file)


    #フレームベース発話の生成
    #dist = frame_base.frame_base(user_ID,topic)
    #print dist

    #トピックベースの発話生成
    #topic_base.topic_base(topic)


if __name__ == '__main__':
    user_ID = 1

    end_flag = False
    f = open(input_file,"r") # 読み書きモードで開く
    #f = open("text/ex1","r") # 読み書きモードで開く
    lines = f.readlines()
    for line in lines:
        sea = re.search(r"(\d*),(.*)\n",line)
        lineid = sea.group(1)
        sentence = sea.group(2)
        print sentence
        #sentence = ("")
        if (sentence == ""):
            endflag = True
            print "お話出来て、楽しかったです。"
            sys.exit()
        knp_tab(sentence,lineid)
    sys.exit()
    

