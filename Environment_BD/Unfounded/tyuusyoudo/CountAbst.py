#-*- encoding: utf-8 -*-
from pyknp import KNP
import sys
import codecs
import time
import csv
import gc
import mojimoji
sys.stdin = codecs.getreader('utf_8')(sys.stdin)
sys.stdout = codecs.getwriter('utf_8')(sys.stdout)


readfile = "aozora/SeparateAllText.txt"
outputfile_name = "abst"
# Use KNP in subprocess mode
# if you don't need case analysis
# knp = KNP(option='-dpnd -tab')
#result = knp.parse(u"太郎は歌舞伎町の風俗街で豪遊しているので、夜の帝王と呼ばれている。")

diclist = {} # [{noun:[abstractnum,allnum]}]

def getChildrenNum(text):
	#print(text)
	part_diclist = {}
	try:
		result = knp.parse(text)
	except Exception as e:
		print text
		print "errormessage:" + str(e)
		return part_diclist
	for bnst in result.bnst_list():
		if(len(bnst.children) == 0):
			abstractnum = 0
		else:
			abstractnum = 1
		# print u"ID:%s, 見出し:%s,children:%s"\
		# %(bnst.bnst_id, "".join(mrph.midasi for mrph in bnst.mrph_list()),"".join(str(x.bnst_id) for x in bnst.children))
		for mrph in bnst.mrph_list():
			if(mrph.hinsi == u"名詞"):
				if(mrph.midasi not in part_diclist):
					part_diclist[mrph.midasi] = [abstractnum,1]
				else:
					part_diclist[mrph.midasi] = \
					[part_diclist[mrph.midasi][0]+abstractnum,part_diclist[mrph.midasi][1]+1]					
	return part_diclist

### test
# text1 = u"太郎は歌舞伎町の風俗街で豪遊しているので、街の夜の帝王と呼ばれている。"
# text2 = u"帝王の最後はクリスマスの夜だった。"
# lines = [text1,text2]
# for line in lines:
# 	if(diclist == {}):
# 		diclist = getChildrenNum(text1)
# 	else:
# 		part_diclist = getChildrenNum(text2)
# 		for p in part_diclist:
# 			if(p not in diclist):
# 				diclist[p] = part_diclist[p]
# 			else:
# 				diclist[p] = [diclist[p][0]+part_diclist[p][0],diclist[p][1]+part_diclist[p][1]]
# 	for i,d in enumerate(diclist):
# 		print d,
# 		print diclist[d]

fr = codecs.open(readfile,"r","utf_8")
lines = fr.readlines()
Alllinenum = len(lines)
diclist = {}
print("Alllinenum : %d"%Alllinenum)
for i,line in enumerate(lines):
	line = mojimoji.han_to_zen(line)
	knp = KNP()
	gc.collect()
	#print line
	if(i % 100 == 0):
		print("line %d process %f %% finished..."%(i,((float(i)/Alllinenum) * 100)))
	if(diclist == {}):
		diclist = getChildrenNum(line)
	else:
		part_diclist = getChildrenNum(line)
		for p in part_diclist:
			if(p not in diclist):
				diclist[p] = part_diclist[p]
			else:
				diclist[p] = [diclist[p][0]+part_diclist[p][0],diclist[p][1]+part_diclist[p][1]]
fw = open(outputfile_name + ".csv","w")
csvWriter = csv.writer(fw)
for i,d in enumerate(diclist):
	if(i == 0):
		writelist = [d.encode("utf_8")]
	# print d,
	# print diclist[d]
	for v in diclist[d]:
		writelist.append(v)
	csvWriter.writerow((d.encode("utf_8"),diclist[d][0],diclist[d][1]))
sys.exit()



# # loop for bunsetsu
# for bnst in result.bnst_list():
#     # print u"ID:%s, 見出し:%s, 係り受けタイプ:%s, 親文節ID:%s, 素性:%s" \
#     # % (bnst.bnst_id, "".join(mrph.midasi for mrph in bnst.mrph_list()), bnst.dpndtype, bnst.parent_id, bnst.fstring)
#     # print u"ID:%s, 見出し:%s,children:%s"\
#     # %(bnst.bnst_id, "".join(mrph.midasi for mrph in bnst.mrph_list()),"".join(str(x.bnst_id) for x in bnst.children))
#     for mrph in bnst.mrph_list():
#         print u"sent:%s, hinsi:%s"%(mrph.midasi,mrph.hinsi)
