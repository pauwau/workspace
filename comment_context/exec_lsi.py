lsi = gensim.models.LsiModel(corpus=tfidf_corpus, id2word=dictionary, num_topics=300)
lsi.save('jawiki_lsi_topics300.model')  # せっかく計算したので保存
