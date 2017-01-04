#!/usr/bin/python
# -*- coding: utf-8 -*-

from gensim.models import word2vec
from pyknp import KNP
import mojimoji

fw = open("outputkw.txt","w")
lower_threshold = 0.2
use_hinsilist = [u"名詞",u"動詞",u"形容詞",u"形容動詞",u"連体詞",u"助詞"]
AssertionWord = [u"です",u"だ"] #Assertion は断定の意味

def convutf(string):
	if(type(string) == type(unicode(""))):
		string = string.encode("utf_8")
	return string


def Detect(string,model):
	knp = KNP()
	# try:
	string = convutf(string)
	Flag = False
	# nlist = DetectNGwords(string)
	# mlist = DetectMeisi(string)
	# ylist = DetectYougen(string)
	fw.write("###" + string + "###\n")
	string = string.decode("utf_8")
	if(string == ""):
		return True
	string = mojimoji.han_to_zen(string)
	knpParsed = knp.parse(string)
	for bnst in knpParsed.bnst_list():
		maxSvalue = 0
		for m1 in bnst.mrph_list():
			#print("%s:%s"%(m1.midasi,m1.hinsi))
			if(bnst.parent and m1.hinsi in use_hinsilist):
				for m2 in bnst.parent.mrph_list():
					if(list(set([mrph.midasi for mrph in bnst.parent.mrph_list()]) & set(AssertionWord))):
						try:
							svalue = model.similarity(m1.midasi,m2.midasi)
						except:
							#print("word is not in dic")
							continue
						if(svalue > maxSvalue and m2.hinsi in use_hinsilist):
							maxSvalue = svalue
							maxmrphs = [m1.midasi,m2.midasi]
		if(maxSvalue < lower_threshold and maxSvalue != 0):
			fw.write("%s-%s:%f\n"%(maxmrphs[0].encode("utf_8"),maxmrphs[1].encode("utf_8"),svalue))
			Flag = True
	#発話中にポジとネガがあれば「一般常識との矛盾」
	if(Flag):
		#print (string)
		return True
	# except Exception as e:
	# 	print (str(e))
	# 	return False
	return False

if __name__ == '__main__':
	path = "/home/pau/workspace/Environment_Bankruptcy/Unfounded/word2vecModel/"
	fname = path + "wikipedia_default.model"
	model = word2vec.Word2Vec.load(fname)  # you can continue training with the loaded model!
	string1 = u"バレー"
	string2 = u"有名"
	svalue = model.similarity(string1,string2)
	print("%s-%s : %f"%(string1,string2,svalue))
