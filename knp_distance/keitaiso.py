#coding:utf-8

import MeCab

lines = open("temp.txt", 'r').read()
o = open("data.txt","w")

mecab = MeCab.Tagger("-Owakati")
MorA = [] #Morphological Analysis 形態素解析
# fileopen to registering word
#str_line = lines.encode("utf-8")
MorA.insert(1,mecab.parse(lines))
#strings = only_string_cut.only_string_cut(MorA,"\t")
for i in MorA:
	o.write(i)
