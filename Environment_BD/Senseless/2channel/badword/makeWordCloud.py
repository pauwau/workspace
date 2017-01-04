# coding:utf-8

import matplotlib.pyplot as plt
from wordcloud import WordCloud
from bs4 import BeautifulSoup
import requests
import MeCab as mc
import os

def mecab_analysis(text):
    t = mc.Tagger("-Ochasen -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd/")
    t.parse('')
    node = t.parseToNode(text) 
    output = []
    while node:
        if node.surface != "":  # ヘッダとフッタを除外
            word_type = node.feature.split(",")[0]
            if word_type in ["形容詞", "動詞","名詞", "副詞"]:
                output.append(node.surface)
        node = node.next
        if node is None:
            break
    return output


def get_wordlist_from_QiitaURL(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "lxml")

    text = soup.body.section.get_text().replace('\n','').replace('\t','')
    return mecab_analysis(text)
    
def create_wordcloud(text):

    fpath = "/usr/share/fonts/FLOPDESIGN-FONT/FlopDesignFONT.otf"

    # ストップワードの設定
    stop_words = [ 'てる', 'いる', 'なる', 'れる', 'する', 'ある', 'こと', 'これ', 'さん', 'して', \
             'くれる', 'やる', 'くださる', 'そう', 'せる', 'した',  '思う',  \
             'それ', 'ここ', 'ちゃん', 'くん', '', 'て','に','を','は','の', 'が', 'と', 'た', 'し', 'で', \
             'ない', 'も', 'な', 'い', 'か', 'ので', 'よう', '', 'れ','さ','なっ']

    wordcloud = WordCloud(background_color="black",font_path=fpath, width=900, height=500, \
                         stopwords=set(stop_words)).generate(text)

    #wordcloud = WordCloud(background_color="black", width=900, height=500, \
    #                      stopwords=set(stop_words)).generate(text)

    plt.figure(figsize=(15,12))
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()
    
url = "http://qiita.com/minagoro0522/items/b2350bab800eddaecad3"
wordlist = get_wordlist_from_QiitaURL(url)
print(wordlist)
create_wordcloud(" ".join(wordlist))