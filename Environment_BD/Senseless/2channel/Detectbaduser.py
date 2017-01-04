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

def comment_has_badword(jsonData,uttID):
	for badword in badwordlist:
		if(badword in jsonData[uttID]["text"].encode("utf-8")):
			#print utt_text
			return True
	return False
	

fjsonfilelist = open("readjsonFileIDList.txt", 'r').read().split(",")
fjsonfilelist.pop()
dateDIR = "2ch_corpus"
writeDIR = "2ch_bad_user"
badwordfile = "badwordlist.txt"
read_file_list = []
fbad = open(badwordfile, 'r')
badwordlist = (fbad.read()).split(",")
baduser_list = []
# baduser = "Genre + _ + ID"

for ID in fjsonfilelist:
	f = open(dateDIR + "/sred" + ID +'.json', 'r')
	jsonData = json.load(f)
	i = 1
	sred_url = jsonData["dat_url"]
	print  ("read:" + sred_url)
	#fw.write("dat-url:" + jsonData["dat_url"] + "\n")
	sred_ID = re.match(r"http:\/\/([a-zA-Z0-9]*)\.open2ch\.net\/([a-zA-Z0-9]*)\/\/board\/dat\/([a-zA-Z0-9]*).dat",sred_url).group(3)
	Genre = jsonData["Genre"]
	#fw.write("Genre:" + Genre.encode("utf-8") + "title:" + jsonData["title"].encode("utf-8") + "\n")
	while(1):
		uttID = str(i)
		if(uttID in jsonData):
			if(comment_has_badword(jsonData,uttID)):
				baduser_list.append(Genre + "_" + jsonData[uttID]["date"].split("ID:")[1])
		else:
			break
		i = i + 1
	# if(int(ID) >= 10):
	# 	break
	#print "\n\nfinish\n\n"
	f.close()
	#fw.close()
print (len(baduser_list))
baduser_list = list(set(baduser_list))
print (len(baduser_list))
baduser_set = set(baduser_list)

# baduser のレスを全部取得
for ID in fjsonfilelist:
	f = open(dateDIR + "/sred" + ID +'.json', 'r')
	jsonData = json.load(f)
	fw = open(writeDIR + "/badUserRess_" + jsonData["Genre"] + ".txt","a")
	i = 0
	sred_url = jsonData["dat_url"]
	print  ("read:" + sred_url)
	while(1):
		i = i + 1
		uttID = str(i)
		if(uttID in jsonData):
			if(jsonData[uttID]["date"] == u"あぼーん"):
				#print (str(uttID) + "nothing text")
				continue
			try:
				if(baduser_set.intersection((Genre + "_" + jsonData[uttID]["date"].split("ID:")[1])) == set([])):
					sred_ID = re.match(r"http:\/\/([a-zA-Z0-9]*)\.open2ch\.net\/([a-zA-Z0-9]*)\/\/board\/dat\/([a-zA-Z0-9]*).dat",sred_url).group(3)
					(detected_text,repto) = detect_text(jsonData[uttID])
					fw.write("ID:" + jsonData[uttID]["date"].split("ID:")[1].encode("utf-8") + "\ntext:" + detected_text.encode("utf-8") + "\n\n")
				else:
					pass
			except:
				continue
				#print baduser_set.intersection(set(jsonData[uttID]["date"].split("ID:")[1]))
		else:
			break
		
	# if(int(ID) >= 10):
	# 	break
	fw.write("########################################################\n")
	f.close()
	fw.close()
	#fw.close()

# <　 … &lt;
# >　 … &gt;
# &　… &amp;
# " … &quot;