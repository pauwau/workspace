#!/usr/bin/python
# -*- coding: utf-8 -*-

from gensim.models import word2vec

path = "/home/pau/workspace/Environment_Bankruptcy/Unfounded/word2vecModel/"
fname = path + "wikipedia_default.model"

if __name__ == '__main__':
	model = word2vec.Word2Vec.load(fname)  # you can continue training with the loaded model!
	string1 = u"量"
	string2 = u"多い"
	svalue = model.similarity(string1,string2)
	print("%s-%s : %f"%(string1,string2,svalue))
