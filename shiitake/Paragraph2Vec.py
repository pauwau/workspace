'''
Created on 2016/05/16

@author: mori
'''

import MeCab
from gensim.models.doc2vec import Doc2Vec
import sqlite3


"""
infer_vector(doc_words, alpha=0.1, min_alpha=0.0001, steps=5)
Infer a vector for given post-bulk training document.

Document should be a list of (word) tokens.
"""



class LabeledListTweetSentence(object):
    def __init__(self, words_list,idList):
        self.words_list = words_list
        self.idList = idList

    def __getitem__(self, index):
        t = [t for t in self]
        return t[index]
    
    def __iter__(self):
        for i, words in enumerate(self.words_list):
            yield LabeledSentence(words, ['SENT_{0}'.format(self.idList[i])])
            
            
    def n_similarity(self, ds1, ds2):
        """
        Compute cosine similarity between two sets of docvecs from the trained set, specified by int
        index or string tag. (TODO: Accept vectors of out-of-training-set docs, as if from inference.)

        """
        v1 = [self[doc] for doc in ds1]
        v2 = [self[doc] for doc in ds2]
        return dot(matutils.unitvec(array(v1).mean(axis=0)), matutils.unitvec(array(v2).mean(axis=0)))
    
    
def extractFeatureWords2(text,tagger):
    """textを形態素解析して、助詞・助動詞の含まれない単語リストを返す"""
    """
    extractFeatureWords2:助詞・助動詞および一般・固有以外の名詞を除く品詞に該当する単語リストを返す
    """
    
    node = tagger.parseToNode(text.encode('utf-8'))#textがu''形式⇒『.encode()』が必要
    featureWords = []
    while node:
        if node.feature.split(",")[0] != u'助詞' and node.feature.split(",")[0] != u'助動詞' and node.feature.split(",")[0] != u'記号':
            if node.feature.split(",")[0] == u'名詞':
                if node.feature.split(",")[1] == u'一般' or node.feature.split(",")[1] == u'固有名詞':
#             if tSentHash[node.surface] > (maxNum/10):
                    featureWords.append(node.surface)
            else:
                featureWords.append(node.surface)
        node = node.next
    return featureWords


if __name__ == '__main__':
    dicPath = "/usr/lib/mecab/dic/mecab-ipadic-neologd"
    tagger = MeCab.Tagger ("-Owakati -d "+dicPath)
#     utt = "！！！発話だよ！！！"
#     model = Doc2Vec.load("../data/hayshi.model")
#     tVec = model.infer_vector(tagger.parse(utt))
#     print(tVec)
    
    limitNum = 860000
    offset = 0
    
    conn = sqlite3.connect("/home/mori/workspace/CreateFilteredDB/tweetDataFiltered05032016.db")
    cur = conn.cursor()
    maxNum = 860000

    cnt = 0
    while offset < maxNum:
#         cur.execute('''SELECT id,in_reply_to_status_id_str,text FROM tweetData LIMIT ? OFFSET ?''',(limitNum,offset))
        cur.execute('''SELECT id,in_reply_to_status_id_str,text FROM tweetData LIMIT ? OFFSET ?''',(limitNum,offset))
        cntList = []
        tweetID = []
        tweetRepID = []
        tweetSent = []
        tweetSentAllFeatures = []
        for row in cur:
            cntList.append(cnt)
            tweetID.append(row[0])
            tweetRepID.append(row[1])
#             tweetSent.append((tagger.parse(row[2].encode('utf-8'))).strip().split(" "))
            tweetSent.append(extractFeatureWords2(row[2], tagger))
            cnt+=1
    
        offset += limitNum
        print(offset)
    

    all_sents = LabeledListTweetSentence(tweetSent,tweetID)
    model = Doc2Vec(size=300,min_count=3,window=5)
    model.build_vocab(all_sents)
    model.train(all_sents)
    model.save('hayashi.model')
    

    
