#! /usr/bin/python
# -*- coding: utf-8 -*-

import re,string
#import data_structure

def Save(lineid,sub,dec,output_file):
    new_line = str(lineid) + "/dec:" + dec 
    for s in sub:
        if not s[1] == "-":
            input_sub = s[1] #主語
        else:
            input_sub = "-"
        new_line = new_line + "," + s[0] + ":" + input_sub
    else:
        new_line = new_line + "\n"
    f = open(output_file,"a+") # 読み書きモードで開く
    old_line = f.read() #情報を読み込む
    if re.findall(new_line,old_line) == []:
        f.write(new_line) # 引数の文字列をファイルに書き込む
        f.close() # ファイルを閉じる


def Ex_relates(clause_list,clause_num,clause,lineid,output_file):
    counter = 0
    #topic = []
    for value in clause:
        if counter == 0:
            start_pos = 1
            end_pos = value

        else:
            start_pos = end_pos + 1
            end_pos = end_pos + value

        counter += 1

        #ここから*から*の範囲（文節の範囲）で情報を抽出していく
        #情報の抽出を正規表現でしていく
        for i in range(start_pos,end_pos + 1):
            sentence = clause_list[i]
            #print sentence
            su1 = re.search(r"格解析結果:([^\s/]*)(/[^\s/]*)*:[^\s/]*:",sentence)
            su2 = re.findall(r"[;;]?([^\s:;/]*)/[^\s/]/([^\s/]*)/[\w-]/[\w-]/[\w-];",sentence)
            # for s in su2:
            #     print s[0],s[1]
            if not su1 == None:
                sub = su2
                dec = su1.group(1) #用言
                Save(lineid,sub,dec,output_file)
                #data = data_structure.info(sub,dec)
                #topic.append(data)
    
    return


