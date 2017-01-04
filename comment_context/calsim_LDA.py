#coding:utf-8
#import logging
import gensim
import MeCab
from gensim import corpora, models, similarities
import time

f = open('dialogue.txt', 'w')
dictionary = gensim.corpora.Dictionary.load_from_text('Topic_Model/hatena2_wordids.txt')
corpus = gensim.corpora.MmCorpus('Topic_Model/hatena2_tfidf.mm') 
# lda のモデルは200次元
lda = gensim.models.LdaModel.load('Topic_Model/hatena2_lda.model')
#lda = gensim.models.LsiModel.load('jawiki_lsi_topics200.model')
#print (lda)
#print (lda.print_topic(6))
# for i in range(0,300):

# 	print (i)
# 	print (lda.print_topic(i))


print ("loading dictionary was finished.")
mecab = MeCab.Tagger("-d /var/lib/mecab/dic/ipadic-utf8 -Owakati")
raw_doc = "はい💦\n雪とかで余計に遅れてるんですかね💦"
his = "青い封筒まだ届いていないひといますか？？？💦 \
\nわたしもまだ届いてません( ´›ω‹｀) \
よかった💦\n電話しても混雑してるのか通じない泣"
doc = mecab.parse(raw_doc)
print doc
doc = unicode(doc,"utf-8")

vec_bow = dictionary.doc2bow(doc.split())
print vec_bow
# convert the query to LSI space
vec_lda = lda[vec_bow]
print vec_lda
for element_lda_vec in vec_lda:
	print(lda.print_topic(element_lda_vec[0]))

# # transform corpus to LSI space and index it
# index = similarities.MatrixSimilarity.load("Topic_Model//hatena2_bow.mm.index")
# #lda_index = similarities.MatrixSimilarity(lda_model[bow_corpus])

# sims = index[vec_lda]
# print "sims: " + str(sims)
# print "len" + str(len(sims))
# sims = sorted(enumerate(sims), key=lambda item: -item[1])[1]
# print "sims: " + str(sims)
# print "topic:" + str(lda.print_topic(sims))