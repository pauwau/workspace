#coding:utf-8
#import logging
import gensim
import MeCab
#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from gensim import corpora, models, similarities
dictionary = gensim.corpora.Dictionary.load_from_text('jawiki_wordids.txt')
corpus = gensim.corpora.MmCorpus('jawiki_tfidf.mm') 
lsi = gensim.models.LsiModel.load('jawiki_lsi_topics200.model')
print ("loading dictionary was finished.")
mecab = MeCab.Tagger("-d /var/lib/mecab/dic/ipadic-utf8 -Owakati")
raw_doc = "値が少なすぎて大変だ"
doc = mecab.parse(raw_doc)
print doc
doc = unicode(doc,"utf-8")

vec_bow = dictionary.doc2bow(doc.lower().split())

# convert the query to LSI space
vec_lsi = lsi[vec_bow]
#print vec_lsi

# transform corpus to LSI space and index it
index = similarities.MatrixSimilarity.load('deerwester.index')

sims = index[vec_lsi]
print "sims: " + str(sims)
print "len" + str(len(sims))
sims = sorted(enumerate(sims), key=lambda item: -item[1])[1]
print "sims: " + str(sims)
print "topic:" + str(lsi.print_topic(sims))