#coding: utf-8
import sqlite3
import MeCab
import gensim
from gensim import corpora, models, similarities
Midstream = 0

def detect_context(law,mecab,dictionary,lsi,index):
    #print len(law)
    (post_id,comment_id,post,comment) = law
    if(type(post) == int):
        post = str(post)
    if(type(comment) == int):
        comment = str(comment)
    #print post
    post = post.encode('utf-8')
    doc_p = mecab.parse(post)
    doc_p = unicode(doc_p,"utf-8")
    vec_bow_p = dictionary.doc2bow(doc_p.split())
    comment = comment.encode('utf-8')
    doc_c = mecab.parse(comment)
    doc_c = unicode(doc_c,"utf-8")
    vec_bow_c = dictionary.doc2bow(doc_c.split())
    vec_lsi_p = lsi[vec_bow_p]
    vec_lsi_c = lsi[vec_bow_c]
    sims_p = index[vec_lsi_p]
    sims_c = index[vec_lsi_c]
    sims_p = sorted(enumerate(sims_p), key=lambda item: -item[1])[:10]
    sims_c = sorted(enumerate(sims_c), key=lambda item: -item[1])[:10]
    #print sims_p
    p_d = ""
    c_d = ""
    for plist in sims_p:
        p = list(plist)
        psl = ",".join(map(str,p))
        if(p_d == ""):
            p_d = psl
        else:
            p_d = p_d + " " + psl
    for clist in sims_c:
        c = list(clist)
        csl = ",".join(map(str,c))
        if(c_d == ""):
            c_d = csl
        else:
            c_d = c_d + " " + csl
    context = p_d + ":" + c_d
    #print context
    return context

def save_context(law,context,count,scur,sconn):
    try:
        scur.execute("""CREATE TABLE cont(post_id serial,comment_id serial,post text,comment text,context text);""")
        print ("made Table!!")
    except sqlite3.OperationalError:
        print str(count) + " process finished"
        # print("---table cont already exist---")
        # scur.execute("""DROP TABLE cont;""")
        # scur.execute("""CREATE TABLE cont(post_id serial,comment_id serial,post text,comment text,context text);""")        
    (post_id,comment_id,post,comment) = law
    scur.execute("""INSERT into cont(post_id,comment_id,post,comment,context) VALUES(%d,%d,'%s','%s','%s');"""\
    %(post_id,comment_id,post,comment,context))
    if(not count % 10):
        sconn.commit()
        print "commit!!!"
    return True

if __name__ == '__main__':
    conn = sqlite3.connect("arrenged_tweets2.db")
    cur = conn.cursor()
    cur.execute("select post_id,comment_id,post,comment from pairs")
    sconn = sqlite3.connect('./context.db')
    scur = sconn.cursor()
    fetch = cur.fetchall()
    count = 0
    mecab = MeCab.Tagger("-d /var/lib/mecab/dic/ipadic-utf8 -Owakati")
    dictionary = gensim.corpora.Dictionary.load_from_text('jawiki_wordids.txt')
    lsi = gensim.models.LsiModel.load('jawiki_lsi_topics200.model')
    try:
        index = similarities.MatrixSimilarity.load('/tmp/deerwester.index')
    except:
        print ("make index file. please wait.")
        corpus = gensim.corpora.MmCorpus('jawiki_tfidf.mm')
        index = similarities.MatrixSimilarity(lsi[corpus])
        index.save('/tmp/deerwester.index')
    # 
    # lsi = gensim.models.LsiModel.load('jawiki_lsi_topics200.model')
    for fetch_law in fetch:
        #print fetch
        if(count < Midstream):
            count += 1
            i += 1
            continue
        context = detect_context(fetch_law,mecab,dictionary,lsi,index)
        #print context
        if(not save_context(fetch_law,context,count,scur,sconn)):
            print "missed save"
        count += 1
    sconn.commit()
    conn.close()
    sconn.close()