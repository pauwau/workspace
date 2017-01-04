#-*- coding: utf-8 -*-

import re

def noiseFilter(text):
	FilteringText = URLDelete(text)
	return FilteringText

def URLDelete(text):
	while re.search(r'(https?://[a-zA-Z0-9.-/]*)', text):
	    match = re.search(r'(https?://[a-zA-Z0-9.-/]*)', text)
	    if match:
	        text =  text.replace(match.group(0)," ")
	return text

# if sentence has many symbol,this function return True.
def SymbolCat(text):
	symbolNum = 0
	charNum = 0
	for char in text:
		if(re.search("[!-/:-@[-`{-~]",char) or re.search(u"[︰-＠]",char) or re.search(u"[a-zA-Z0-9]",char)):
			symbolNum += 1
		else:
			charNum += 1
	if(symbolNum >= charNum):
		return True
	return False

def PunkDelete(morphList):
	deleteIndexList = []
	for i,morph in enumerate(morphList):
		if(re.search("[!-/:-@[-`{-~]",morph) or re.search(u"[︰-＠]",morph)):
			deleteIndexList.append(i)
	for deleteIndex in deleteIndexList.reverse():
		del morphList[deleteIndex]
	return morphList


if __name__ == '__main__':
	text ="https://twitter.com, facebook:http://facebook.com/control/event"
	text = noiseFilter(text)
	print text