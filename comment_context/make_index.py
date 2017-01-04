#coding: utf-8
#import logging
import gensim
#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from gensim import corpora, models, similarities
dictionary = gensim.corpora.Dictionary.load_from_text('jawiki_wordids.txt')
corpus = gensim.corpora.MmCorpus('jawiki_tfidf.mm') 
lsi = gensim.models.LsiModel.load('jawiki_lsi_topics200.model')
print "loading dictionary was finished."

index = similarities.MatrixSimilarity(lsi[corpus]) # transform corpus to LSI space and index it
index.save('/tmp/deerwester.index')
