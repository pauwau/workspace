#!/usr/bin/python
# -*- coding: utf-8 -*-

from gensim.models import word2vec

print("0%")
sentences = word2vec.Text8Corpus("aozora/AllText_wakati.txt")
model = word2vec.Word2Vec(sentences, size=100,window=5)

model.save("aozora_default.model")
