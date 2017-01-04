#!/usr/bin/python
# -*- coding: utf-8 -*-

from gensim.models import word2vec

print("0%")
sentences = word2vec.Text8Corpus("corpus_wakati.txt")
model = word2vec.Word2Vec(sentences, size=100,window=5)

model.save("wikipedia_default.model")

print("25%")
model = word2vec.Word2Vec(sentences, size=300,window=5)
model.save("wikipedia_size300.model")

print("50%")
model = word2vec.Word2Vec(sentences, size=100,window=10)
model.save("wikipedia_window10.model")

print("75%")
model = word2vec.Word2Vec(sentences, size=100,window=20)
model.save("wikipedia_window20.model")