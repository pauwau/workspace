# -*- coding: utf-8 -*-
'''
Created on 2016/03/01

@author: mori
'''

from os.path import join, relpath
from glob import glob
import codecs
import json


def getFilenames(path):
    filenames = []
    for i in [glob(join(y, '*')) for y in glob(join(path,'*'))]:
        filenames = filenames + i
    return filenames


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
        isBreakdown = "破綻({:0>.2f})".format(bValue/annotatorNum)
    else:
        isBreakdown = ""
    return isBreakdown
            
def getComments(data):
    return [c["comment"] for c in data if c["comment"] != ""]
    
def writeIsBreakdown(data,threshold):
    isBreakdown = getIsBreakdown(data["annotations"], threshold)
    outFile.write(isBreakdown+', ')
    
def writeComments(data,outFile):
    commentsList = getComments(data["annotations"])
    if commentsList != None:
        for s in commentsList:
            outFile.write("\'"+s+"\'")
        outFile.write("\n")
        

if __name__ == '__main__':
    threshold = 0.5
    path = 'DBDC2_eval/'
    jsonFiles = getFilenames(path)
    outFile = codecs.open('OutputData/eval.csv', 'w','utf-8')
    
    for f in jsonFiles:
        f = codecs.open(f,'r','utf-8')
        jsonData = json.load(f)
        for data in jsonData["turns"]:
            #outFile.write(str(f) + ", ")
            #outFile.write("subset_"+jsonData["group-id"][-1]+"_")
            outFile.write(jsonData["dialogue-id"]+', ')
            #outFile.write(jsonData["group-id"][-1]+', ')
            outFile.write("{:0>2}".format(data["turn-index"])+', ')
            outFile.write(data["utterance"]+', ')
            writeIsBreakdown(data,threshold)
            writeComments(data,outFile)
    
