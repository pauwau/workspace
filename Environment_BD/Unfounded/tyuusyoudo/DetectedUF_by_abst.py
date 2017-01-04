# -*- coding: utf-8 -*-
'''
Created on 2016/09/18

@author: hayashi
'''
from pyknp import KNP
import mojimoji
import MeCab

readfilename = "sortedabst_over10.csv"

Threshold = 0.7

def Detect(string):
	# if(type(string) == type(unicode(""))):
	# 	string = string.encode("utf_8")
	rf = open(readfilename,"r")
	dicPath = "/usr/local/lib/mecab/dic/mecab-ipadic-neologd"
	tagger = MeCab.Tagger ("-Owakati -d " + dicPath)
	keitaiso = tagger.parse(string).split()
	lines = rf.read().split("\n")
	abst_array = []
	for line in lines:
		if(line == ""):
			break
		else:
			abst_array.append(line.split(","))

	abst_array = sorted(abst_array, key=lambda x: float(x[1])/float(x[2]))
#	string.decode("utf_8")
	for k in keitaiso:
#		k = k.decode("utf_8")
		for a in abst_array:
			#print(a[0])
			#print k
			if(k == a[0]):
				abstractValue = float(a[1])/float(a[2])
				if(abstractValue > Threshold):
					knp = KNP()
					#print a[0]
					result = knp.parse(mojimoji.han_to_zen(string))
					for bnst in result.bnst_list():
						if(len(bnst.children) != 0):
							for mrph in bnst.mrph_list():
								if(mrph.hinsi == u"名詞" ):
									print (a[0])
									return True
	return False

if __name__ == '__main__':
	flag = Detect(string)
	print ("process finished...!!")
