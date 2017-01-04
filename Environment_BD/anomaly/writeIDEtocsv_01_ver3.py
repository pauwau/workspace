# -*- coding: utf-8 -*-
'''
Created on 2016/09/01

@author: hayashi
'''

from os.path import join, relpath
from glob import glob
import codecs
import json
import Detect_ver2
import Detect_ver2_onlykyoku

#DCM,IRS,DITのフォルダが入ったフォルダを指す必要がある
path = './DBDC2_dev/'
#しいたけ君に言われた形式のCSVファイルのつもり
outFile = codecs.open('eval_EvaluationData_onlykyoku.csv', 'w','utf-8')


#フォルダ内の各ファイル名を取得する
def getFilenames(path):
    return [relpath(x, path) for x in glob(join(path, '*'))]


# 各発話をdetectモジュールに入力し、0,1をcsvファイルに書き込む
def writeconclusion(data):   
    conclusion = Detect_ver2.Detect(data["utterance"])
    # conclusion = Detect_ver2_onlykyoku.Detect(data["utterance"])
    if(conclusion):
        outFile.write("0"+', ')
    else:
        outFile.write("1"+', ')
    return conclusion


# 各発話を識別するための情報を書き込む
def writeID(data,foldername,dialogue_id):
    outFile.write(str(foldername)+', '+ str(dialogue_id) +', ' + str(data["turn-index"])+', ' + data["utterance"])


if __name__ == '__main__':
    foldernamelist = sorted(["DCM","DIT","IRS"])
    #各フォルダ名について処理を行う
    for foldername in foldernamelist:
        jsonFiles = sorted(getFilenames(path+foldername+"/"))
        #各ファイル名についての処理を行う
        for f in jsonFiles:
            f = codecs.open(path + foldername + "/" + f,'r','utf-8')
            jsonData = json.load(f)
            dialogue_id = jsonData["dialogue-id"]
            #各ターンの発話について処理を行う
            for data in jsonData["turns"]:
                turnIndex = int(data["turn-index"])
                #初めのシステム発話とユーザ発話を除く発話について処理を行う
                if(turnIndex%2 == 0 and turnIndex != 0):
                    conclusion = writeconclusion(data)
                    writeID(data,foldername,dialogue_id)
                    outFile.write("\n")
