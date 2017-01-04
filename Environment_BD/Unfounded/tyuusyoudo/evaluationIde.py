# -*- coding: utf-8 -*-
'''
Created on 2016/09/01

@author: hayashi
'''

from os.path import join, relpath
from glob import glob
import codecs
import json
import DetectedUF_by_abst


def getFilenames(path):
    return [relpath(x, path) for x in glob(join(path, '*'))]

        # filenames = []
        # for i in [glob(join(y, '*')) for y in glob(join(path,'*'))]:
        #     filenames = filenames + i
        # return filenames


def getIsBreakdown(data,threshold):
    annotatorNum = 0
    bValue = 0
    isBreakdown = ""
    for b in data:
        annotatorNum += 1
        if b["breakdown"] == 'O':
            bValue += 0
        elif b["breakdown"] == 'T':
            bValue += 0.5
        elif b["breakdown"] == 'X':
            bValue += 1.0
        else:
            print("Annotation Missed?:"+b["breakdown"])
        
    if annotatorNum != 0 and bValue/annotatorNum >= threshold:
        isBreakdown = u"破綻({:0>.2f})".format(bValue/annotatorNum)
    else:
        isBreakdown = u""
    return isBreakdown

            
def getComments(data):
    return [c["comment"] for c in data if c["comment"] != ""]

    
def writeIsBreakdown(data,threshold):
    isBreakdown = getIsBreakdown(data["annotations"], threshold)
    outFile.write(isBreakdown+', ')
    return isBreakdown

    
def writeComments(data,outFile):
    commentsList = getComments(data["annotations"])
    if commentsList != None:
        for s in commentsList:
            outFile.write("\'"+s+"\'")


def writeconclusion(data):   
    conclusion = DetectedUF_by_abst.Detect(data["utterance"])
    outFile.write(str(conclusion)+', ')
    return conclusion


def writePath(data,foldername):
    outFile.write(str(foldername)+', ')


if __name__ == '__main__':
    [TP,FN,FP,TN] = [0,0,0,0]
    threshold = 0.5
    path = '/home/pau/workspace/hatankennsyutuchallenge/DBDC2_dev/'
    #foldernamelist = ["DCM","DIT","IRS"]
    foldernamelist = ["DCM"]
    foldernamelist_len = len(foldernamelist)
    for j,foldername in enumerate(foldernamelist):
        jsonFiles = getFilenames(path+foldername+"/")
        outFile = codecs.open('EvaluationData' + foldername + '.csv', 'w','utf-8')
        leng = len(jsonFiles)
        for i,f in enumerate(jsonFiles):
            f = codecs.open(path + foldername + "/" + f,'r','utf-8')
            jsonData = json.load(f)
            for data in jsonData["turns"]:
                outFile.write(jsonData["dialogue-id"]+', ')
                outFile.write("{:0>2}".format(data["turn-index"])+', ')
                outFile.write(data["utterance"]+', ')
                turnIndex = int(data["turn-index"])
                if(turnIndex%2 == 0 and turnIndex != 0):
                    isBreakdown = writeIsBreakdown(data,threshold)
                    conclusion = writeconclusion(data)
                    writeComments(data,outFile)
                    writePath(data,foldername)
                    if(conclusion):
                        print(data["utterance"])
                        if(isBreakdown == u""):
                            TP += 1
                        else:
                            FP += 1
                    else:
                        if(isBreakdown == u""):
                            FN += 1
                        else:
                            TN += 1                    
                outFile.write("\n")
            print("%f %% finished..."%(((float(i)/(leng*foldernamelist_len)) +float(j)/foldernamelist_len) * 100) )
    print("TP:%d\nFN:%d\nFP:%d\nTN:%d\n"%(TP,FN,FP,TN))
    print("Accuracy:%d%%\n"%(float(TP+TN)/(TP+FN+FP+TN)*100))
    print("precision:%d%%\n"%(float(TP)/(TP+FP)*100))
    print("Recall:%d%%\n"%(float(TP)/(TP+FN)*100))
    print("N-precision:%d%%\n"%(float(TN)/(TN+FN)*100))
    print("N-recall:%d%%\n"%(float(TN)/(TN+FP)*100))