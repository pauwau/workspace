#-*- coding: utf-8 -*-

import json
import re
import textPreprocess

def replaceAll(text):
	detect_text = text.replace(u"&lt;",u"<")
	detect_text = detect_text.replace(u"&gt;",u">")
	detect_text = detect_text.replace(u"&amp;",u"&")
	detect_text = detect_text.replace(u"&quot;",u"\"")
	detect_text = detect_text.replace(u"<br>",u"\n")
	
	return detect_text

def detect_text(utt):
	text = utt["text"]
	text = replaceAll(text)
	repto = []
	#print sred_ID
	#print text
	#print "href=/test/read.cgi/%s/%s/([0-9]*)"%(Genre,sred_ID) + "\n"
	repto = re.findall(r"href=/test/read.cgi/%s/%s/([0-9]*)"%(Genre,sred_ID),text)
	text = re.sub(r"href=/test/read.cgi/%s/%s/([0-9]*)"%(Genre,sred_ID),"",text)
	text = re.sub(r"rel=\"nofollow\"","",text)
	#print type(ma)
	if(repto != []):
		#print ma
		return text,repto
	return text,repto

def comment_has_badrep(jsonData,uttID,repto):
	for badword in badwordlist:
		if(badword in jsonData[uttID]["text"].encode("utf-8")):
			for one_ref in repto:		
				if(one_ref  in jsonData):
					utt_text,repto = detect_text(jsonData[one_ref])
					fw.write("host:\n" + utt_text.encode("utf-8") + "\n")
					#print utt_text
					return True
				else:
					print ("nothing reffernce\n")
	return False
	

fjsonfilelist = open("readjsonFileIDList.txt", 'r').read().split(",")
fjsonfilelist.pop()
dateDIR = "2ch_corpus"
writeDIR = "2chWord2vecModel"
read_file_list = []
#fbad = open(badwordfile, 'r')
fw = open(writeDIR + "/alldata.txt","w")

for ID in fjsonfilelist:
	f = open(dateDIR + "/sred" + ID +'.json', 'r')
	jsonData = json.load(f)
	i = 0
	sred_url = jsonData["dat_url"]
	print  ("read:" + sred_url)
	#fw.write("dat-url:" + jsonData["dat_url"] + "\n")
	sred_ID = re.match(r"http:\/\/([a-zA-Z0-9]*)\.open2ch\.net\/([a-zA-Z0-9]*)\/\/board\/dat\/([a-zA-Z0-9]*).dat",sred_url).group(3)
	Genre = jsonData["Genre"]
	#fw.write("Genre:" + Genre.encode("utf-8") + "title:" + jsonData["title"].encode("utf-8") + "\n")
	while(1):
		i = i + 1
		uttID = str(i)
		if(uttID in jsonData):
			if(textPreprocess.SymbolCat(jsonData[uttID]["text"])):
				continue
			else:
				fw.write(jsonData[uttID]["text"].encode("utf-8") + " \n")
		else:
			break
	# if(int(ID) >= 10):
	# 	break
	#print "\n\nfinish\n\n"
	f.close()
	#fw.close()
# >　 … &gt;
# &　… &amp;
# " … &quot;