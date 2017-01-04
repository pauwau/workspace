# -*- coding: utf-8 -*-
'''
Created on 2016/03/01

@author: mori
'''

from os.path import join, relpath
from glob import glob
import codecs
import json
import MeCab
import matplotlib.pyplot as plt
fw = open("output.txt","w")
dicPath = "/usr/local/lib/mecab/dic/mecab-ipadic-neologd"
tagger = MeCab.Tagger ("-d " + dicPath)


def getFilenames(path):
    filenames = []
    for i in [glob(join(y, '*')) for y in glob(join(path,'*'))]:
        filenames = filenames + i
    return filenames


def getIsBreakdown(data,threshold):
    annotatorNum = 0
    Onum = 0
    Tnum = 0
    Xnum = 0
    bValue = 0
    isBreakdown = ""
    for b in data:
        annotatorNum += 1
        if b["breakdown"] == 'O':
            bValue += 0
            Onum += 1
        elif b["breakdown"] == 'T':
            bValue += 0.5
            Tnum += 1
        elif b["breakdown"] == 'X':
            bValue += 1.0
            Xnum += 1
        else:
            print("Annotation Missed?:"+b["breakdown"])
        
    #if annotatorNum != 0 and bValue/annotatorNum >= threshold:
    if (annotatorNum != 0):
        isBreakdown = u"破綻({:0>.2f})".format(bValue/annotatorNum)
    #else:
    #    isBreakdown = ""
    return [isBreakdown,Onum,Tnum,Xnum]
            
def getComments(data):
    return [c["comment"] for c in data if c["comment"] != ""]
    
def writeIsBreakdown(data,threshold,plotdata):
    isBreakdown,Onum,Tnum,Xnum = getIsBreakdown(data["annotations"], threshold)
    k = tagger.parse(data["utterance"].encode("utf-8"))
    koyuumeisiNum = k.count("固有名詞")
    if(koyuumeisiNum == 11):
        print(data["utterance"])
    outFile.write(isBreakdown+', '+str(Onum)+', '+str(Tnum)+', '+str(Xnum)+', ')
    if(not Onum + Tnum + Xnum == 0):
        plotdata.append([koyuumeisiNum,Onum,Tnum,Xnum])
    return(plotdata)
    
def writeComments(data,outFile):
    commentsList = getComments(data["annotations"])
    if commentsList != None:
        for s in commentsList:
            outFile.write("\'"+s+"\'")
        outFile.write("\n")
        
def mean(lis):
    if(len(lis) != 0):
        mean = sum(lis)/len(lis)
        return mean
    else:
        return 0


if __name__ == '__main__':
    # SumOnum = 0
    # SumTnum = 0
    # SumXnum = 0
    threshold = 0.5
    path = 'DBDC2_dev/'
    jsonFiles = getFilenames(path)
    outFile = codecs.open('OutputData/Anotator.csv', 'w','utf-8')
    plotdata = []
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
            plotdata = writeIsBreakdown(data,threshold,plotdata)
            # Onum,Tnum,Xnum = writeIsBreakdown(data,threshold)
 #           [SumOnum,SumTnum,SumXnum] = [SumOnum+Onum,SumTnum+Tnum,SumXnum+Xnum]
            writeComments(data,outFile)
  #  fw.write("SumOnum:%d\nSumTnum:%d\nSumXnum:%d\nSum:%d"%(SumOnum,SumTnum,SumXnum,(SumOnum+SumTnum+SumXnum)))
    
    [K,O,T,X] = [[],[],[],[]]
    plotdata = sorted(plotdata, key=lambda x: int(x[0]))
    # for p in plotdata:
    #     k.append(p[0])
    #     o.append(p[1])
    #     t.append(p[2])
    #     x.append(p[3])
    #     print p
    for i in range(0,13):
        K.append(i)
        O.append(mean([x[1] for x in plotdata if x[0]==i]))
        T.append(mean([x[2] for x in plotdata if x[0]==i]))
        X.append(mean([x[3] for x in plotdata if x[0]==i]))
    # plt.xlabel("koyuu")
    # plt.ylabel("Onum")
    # plt.plot(K,O)
    # plt.show()
    # plt.ylabel("Tnum")
    # plt.plot(K,T)
    # plt.show()
    # plt.ylabel("Xnum")
    # plt.plot(K,X)
    # plt.show()