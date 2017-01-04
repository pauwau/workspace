#-*- coding: utf-8 -*-

import json
import re

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
	for one_ref in repto:		
		if(one_ref  in jsonData):
			for badword in badwordlist:
				if(badword in jsonData[one_ref]["text"].encode("utf-8")):
					utt_text,repto = detect_text(jsonData[one_ref])
					fw.write("ID:" + one_ref.encode("utf-8") + "...host:\n" + utt_text.encode("utf-8") + "\n")
					#print utt_text
					return True
		else:
			print ("nothing reffernce\n")
	return False
	

ID_higher_limit = 17500
ID_lower_limit = 1
dateDIR = "2ch_corpus"
writeDIR = "2ch_text_badhost"
badwordfile = "badwordlist.txt"
fbad = open(badwordfile, 'r')
badwordlist = (fbad.read()).split(",")

for ID in range(ID_lower_limit,ID_higher_limit):
	ID = str(ID)
	try:
		f = open(dateDIR + "/sred" + ID +'.json', 'r')
	except:
		print ID  + " is not found"
		continue
	fw = open(writeDIR + "/sred" + ID +'.txt', 'w')

	jsonData = json.load(f)

	i = 1
	dat_url = jsonData["dat_url"]
	sred_url = "http://" + jsonData["server"] + ".open2ch.net/test/read.cgi/" + jsonData["Genre"] + "/" + jsonData["url"] + "/l1000"
	#print dat_url + "\n"
	print sred_url
	sred_ID = jsonData["url"]
	Genre = jsonData["Genre"]
	fw.write("sred_url:" + sred_url + "\n")
	fw.write("dat_url:" + jsonData["dat_url"].encode("utf-8") + "\nGenre:" + Genre.encode("utf-8") + "\ntitle:" + jsonData["title"].encode("utf-8") + "\n")
	fw.write("\n---------------------------------------------\n")
	while(1):
		i = i + 1
		uttID = str(i)
		if(uttID in jsonData):
			(detected_text,repto) = detect_text(jsonData[uttID])
			if(comment_has_badrep(jsonData,uttID,repto)):
				fw.write("ID;" + uttID + "...comment:\n" + detected_text.encode("utf-8") + "\n---------------------------------------------\n")
		else:
			break
	#print "\n\nfinish\n\n"
	f.close()
	fw.close()

# <　 … &lt;
# >　 … &gt;
# &　… &amp;
# " … &quot;