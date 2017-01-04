import gensim
dictionary = gensim.corpora.Dictionary.load_from_text('jawiki_wordids.txt')
tfidf_corpus = gensim.corpora.MmCorpus('jawiki_tfidf.mm')
tfidf_index = gensim.similarities.SparseMatrixSimilarity.load('jawiki_tfidf_wimilarity.index')
query = "大学 京都"  # クエリ
query_vector = dictionary.doc2bow(query.split())
sims = tfidf_index[query_vector]
print sorted(enumerate(sims), key=lambda item: -item[1])[:10]

#この結果、122325の記事と値が近いことがわかる。
