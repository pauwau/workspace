# -*- coding: utf-8 -*-

import MeCab
import re
from pyknp import KNP
import gc
import mojimoji

kyokuseijisyoPath = "kyokuseijisyo"
wordnetPath = "wordnet_python"
dicPath = "/usr/local/lib/mecab/dic/mecab-ipadic-neologd"
filem = "meisi.trim"
# ぼけ	n	〜である・になる（状態）客観
filey = "yougen.pn"
# ポジ（評価）	目 を 奪う
filen = "OutputNGwords.txt"
fw = open("output.txt","w")
tagger = MeCab.Tagger ("-Owakati -d " + dicPath)

def convutf(string):
	if(type(string) == type(unicode(""))):
		string = string.encode("utf_8")
	return string


def DetectNGwords(string):
	string = convutf(string)
	fn = open(wordnetPath + "/" + filen,"r")
	fnlines = fn.read().split("\n")
	nlist = []
	keitaiso = tagger.parse(string)
	for k in keitaiso.split():
		if(k in fnlines):
			nlist.append(k)
			fw.write(k)
	return nlist


# 極性辞書にある発話中の名詞を完全一致で抽出
def DetectMeisi(string):
	string = convutf(string)
	fm = open(kyokuseijisyoPath + "/" + filem,"r")
	fmlines = fm.readlines()
	mlist = []
	mdic = {}
	for fmline in fmlines:
		lis = fmline.split("\t")
		mdic[lis[0]] = lis[1]
	keitaiso = tagger.parse(string)
	for k in keitaiso.split():
		if(k in mdic):
			f = mdic[k]
		else:
			f = "f"
		mlist.append([k,f])
	return mlist

# 極性辞書にある発話中の用言を完全一致で抽出
def DetectYougen(string):
	string = convutf(string)
	fy = open(kyokuseijisyoPath + "/" + filey,"r")
	fylines = fy.readlines()
	ydic = {}
	for fyline in fylines:
		lis = fyline.split("\t")
		dic = [lis[1],lis[0]]
		pattern = re.compile('[\s]')
		ydic[pattern.sub("",dic[0])] = dic[1]
	ylist = []
	for y in ydic.keys():
		if(y == ""):
			continue
		if(y in string):
			f = ydic[y]
		else:
			f = "f"
		if(f != "f"):
			ylist.append([y,f])
	return ylist


def Detect(string):
	knp = KNP()
	try:
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
			if(DetectNGwords("".join(mrph.midasi for mrph in bnst.mrph_list())) != []):
				if(bnst.parent):
					mlist = DetectMeisi("".join(mrph.midasi for mrph in bnst.parent.mrph_list()))
					ylist = DetectYougen("".join(mrph.midasi for mrph in bnst.parent.mrph_list()))
					for m in mlist:
						fw.write("%s\t%s\n"%(m[0],m[1]))
						if(m[1] == "p"):
							Flag = True
					for y in ylist:
						fw.write("%s\t%s\n"%(y[0],y[1]))
						if("ポジ" in y[1]):
							Flag = True
		#発話中にポジとネガがあれば「一般常識との矛盾」
		if(Flag):
			print (string)
			return False
	except Exception as e:
		print (str(e))
		return True
	return True


if __name__ == '__main__':
	fr = open("testinput.txt","r")
	for string in fr.read().split("\n"):
		if(len(string) == 0):
			continue			
		print (string)
		if(Detect(string)):
			print ("this string is not Anomaly!\n")
		else:
			print ("this string is Anomaly!\n")