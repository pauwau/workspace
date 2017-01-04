# encoding: utf-8

import MeCab

dicPath = "/usr/local/lib/mecab/dic/mecab-ipadic-neologd"
tagger = MeCab.Tagger ("-Owakati -d " + dicPath)

def Detect(string):
	string = string.encode('utf-8')
	node = tagger.parseToNode(string).next
	flag = False
	while node:
		if node.feature.split(",")[0] == "形容詞":
			#print (string)
			flag = True
		node = node.next
	return flag


if __name__ == '__main__':
	string = u"世界は広いですね"
	print (string + ":" + str(detect_adj(string))) 
	string = u"我こそ魔王"
	print (string + ":" + str(detect_adj(string)))