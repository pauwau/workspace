#! /usr/bin/python
#coding:utf-8
from pyknp import KNP
from pyknp import Juman

#input raw
#input_line = raw_input()
# input_line = unicode(input_line)
data = u"私は元気です。"

jum = Juman()

jum_line = jum.analysis(data.encode("utf-8"))
#analyze raw
# mecab = MeCab.Tagger()
# # mec_line = mecab.parse(input_line)
# data = data.encode('shift-jis')
# knp = KNP(option = '-tab -anaphora')
# knp_line = knp.parse(data)

#keep information
#f = open('test.txt', 'w') # 書き込みモードで開く
#f.write(input_line) # 引数の文字列をファイルに書き込む
#f.close() # ファイルを閉じる

#select flame

#generate utterance

#print mec_line
print jum_line 
#print knp_line