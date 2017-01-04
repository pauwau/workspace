#-*- encoding: utf-8 -*-
from os.path import join, relpath
from glob import glob
import codecs
import json


def getFilenames(path):
    return [relpath(x, path) for x in glob(join(path, '*'))]


if __name__ == '__main__':
	alldata = {}
	writefile1 = open("alldata.csv","w")
	writefile2 = open("EBdata.csv","w")
	path = '/home/pau/workspace/hatankennsyutuchallenge/anotation_csv/'
	foldernames = getFilenames(path)
	for foldername in foldernames:
		filenames = getFilenames(path + "/" + foldername + "/")
		for filename in filenames:
			filepath = path + "/" + foldername + "/" + filename
			try:
				f = open(filepath,"r")
				alltext = f.read()
			except:
				f = open(filepath,"r",encoding='Shift_JIS')
				alltext = f.read()
			lines = alltext.split("\n")
			#csvファイルは最後に改行があるため、余計な要素が一つ入ってしまう
			del lines[-1]
			for line in lines:
				if("\"" in line):
					[dID,Sys,uID,utterance1,utterance2,isbreakdown,hoge,kind]  = line.split(",")
					utterance = utterance1 + "," + utterance2
				else:
					[dID,Sys,uID,utterance,isbreakdown,hoge,kind]  = line.split(",")
				if(len(uID) == 1):
					uID = "0" + uID
				ID = int(dID+uID)
				if(ID not in alldata):
					alldata.update({ID:[utterance,Sys,isbreakdown,kind,"",""]})
				elif(alldata[ID][4] != ""):
					alldata.update({ID:[utterance,Sys,isbreakdown,alldata[ID][3],alldata[ID][4],kind]})
				else:
					alldata.update({ID:[utterance,Sys,isbreakdown,alldata[ID][3],kind,""]})					
			# print (filepath)
			# print (dID+Sys+uID+utterance+isbreakdown+hoge+kind)
	for a in sorted(alldata.keys()):
		writefile1.write("%s,%s,%s,%s,%s,%s,%s\n"%(a,alldata[a][0],alldata[a][1],alldata[a][2],alldata[a][3],alldata[a][4],alldata[a][5]))
		if(alldata[a][3] == "環境" or alldata[a][4] == "環境" or alldata[a][5] == "環境"):
			writefile2.write("%s,%s,%s,%s,%s,%s,%s\n"%(a,alldata[a][0],alldata[a][1],alldata[a][2],alldata[a][3],alldata[a][4],alldata[a][5]))
	writefile1.close()
	writefile2.close()