# encoding: utf-8

import re

fr = open("aozora/AllText.txt","r")
fw = open("aozora/SeparateAllText.txt","w")

lines = fr.readlines()

linenum = len(lines)
for i,line in enumerate(lines):
	DeleteNumList = []
	Sentences = filter(lambda w: len(w) > 0, re.split(r'\s|"|,|\.|。|「|」|\n|\t', line))
	for j,s in enumerate(Sentences):
		if((len(s) < 5) or (re.search(r"\A[\s\w\!\-\/\:\-\@\[\-\`\{\-\~]*\Z",s)) or (len(s) > 50)):
			DeleteNumList.append(j)
	if(DeleteNumList != []):
		DeleteNumList.reverse()		
		for DeleteNum in DeleteNumList:
			del Sentences[DeleteNum]
	for Sentence in Sentences:
		fw.write(Sentence + "\n")
	if(i % 100000 == 0):
		print("process %f %% finished..."%((float(i)/linenum) * 100))