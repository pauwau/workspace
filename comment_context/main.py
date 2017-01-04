#coding: utf-8
import sqlite3
import MeCab
import gensim
from gensim import corpora, models, similarities
import time
import datetime

limit = False
limit_num = 1000
database = "context.db"
ll_limit = 3

dictionary = gensim.corpora.Dictionary.load_from_text('jawiki_wordids.txt')
lsi = gensim.models.LsiModel.load('jawiki_lsi_topics200.model')


#def read_DB(cur):


def select_context(cur,vec_lsi,index,sentence):
	todaydetail  = datetime.datetime.today()
	f = open('select_log.txt', 'a')
	f.write("\n---------------------------------\n" + str(todaydetail.strftime("%Y/%m/%d %H:%M:%S")) + "\nsentence:" + sentence + "\n")
	score_array = []
	good_score_array = []
	sims_q = index[vec_lsi]
	sims_q = sorted(enumerate(sims_q), key=lambda item: -item[1])[:10]
	for i,a_low in enumerate(cur):
		if (i > limit_num and limit):
			break
		flag = 0
		score = 0
		(post_id,comment_id,post,comment,context) = a_low
		#print i
		#print "post:" + post
		#print "comment:" + comment
		#vec_lsi_p,vec_lsi_c = context.split(":")
		arti_p,arti_c = context.split(":")
		# vec_lsi_p = vec_lsi_p.split(" ")
		# vec_lsi_c = vec_lsi_c.split(" ")
		# sims_p = sims_p.split(" ")
		# sims_q = sims_q.split(" ")
		arti_p = arti_p.split(" ")
		arti_c = arti_c.split(" ")
		for l,vp in enumerate(arti_p):
			vp = vp.split(",")
			if(not vp == [u""]):
				vp = map(float,vp)
				vp[0] = int(vp[0])
			else:
				flag = 1
				continue
			arti_p[l] = tuple(vp)
		for l,vc in enumerate(arti_c):
			vc = vc.split(",")
			if(not vc == [u""]):
				vc = map(float,vc)
				vc[0] = int(vc[0])
			else:
				flag = 1
				continue
			arti_c[l] = tuple(vc)
		if(flag == 1):
			continue
		#print vec_bow_p
		#print vec_bow_c
		# print "sims_c:" + str(sims_c[:])
		# print "sims_p:" + str(sims_p[:])
		# print "sims_q:" + str(sims_q[:])
		# print "arti_c:" + str(arti_c[:])
		# print "arti_p:" + str(arti_p[:])
		for a_article in sims_q:
			if(a_article[0] in [x[0] for x in arti_p]):
				#f.write("sims_p:" + str(a_article[0]) + "\n")
				score += 1
			if(a_article[0] in [x[0] for x in arti_c]):
				#f.write("sims_c:" + str(a_article[0]) + "\n")
				score += 1
		score_array.append([i,score])
		if(score >= ll_limit):
			good_score_array.append([post_id,comment_id,post.encode("utf-8"),comment.encode("utf-8"),i,score])
	#print "score_array:" + str(score_array)
	for g_element in good_score_array:
		f.write("\ngood_score_array  i:" + str(g_element[-2]) +\
		 " score:" + str(g_element[-1]) + \
	 	"\n post:\n" + str(g_element[2]) + \
	 	"\n comment:\n" + str(g_element[3]) +  "\n\n")

	max_score = max(x[1] for x in score_array)
	print "max_score:" + str(max_score)
	f.write("\nmax_score:" + str(max_score))
	
	num_temp = 0
	for l,score in enumerate(score_array):
		if(score[1] == max_score):
			score_temp = score[1]
			num_temp = l
			break
	low = cur[num_temp]
	f.write("\n--------------------------------------------\n\n")
	f.close()
	return low

def return_comment(sentence,index):
	vec_bow = dictionary.doc2bow(sentence.split())
	print sentence.split()
	vec_lsi = lsi[vec_bow]
	if(index == None):
		conn = sqlite3.connect(database)
		cur = conn.cursor()
		#(all_low,index) = read_DB(cur)
		index = similarities.MatrixSimilarity.load('/home/pau/workspace/comment_context/deerwester.index')
		print ("read DB and loaded index")
	cur.execute("select post_id,comment_id,post,comment,context from cont")
	all_low = cur.fetchall()
	low = select_context(all_low,vec_lsi,index,sentence.encode("utf-8")) #sentence for log
	(post_id,comment_id,post,comment,context) = low
	conn.close()
	print ("###################")
	return  post,comment

if __name__ == '__main__':
	
	sentence = u"あけましておめでとうございます。"
	end_flag = False
	while(not end_flag):
		print("please input ↓")
		sentence = raw_input().decode("utf-8")
		temptime = time.time()
		if(sentence == ""):
			print("end process")
			break
		index = None
		mecab = MeCab.Tagger("-d /var/lib/mecab/dic/ipadic-utf8 -Owakati")
		sentence = sentence.encode('utf-8')
		sentence = mecab.parse(sentence)
		sentence = unicode(sentence,"utf-8")
		[selected_post,selected_comment] = return_comment(sentence,index)
		print "selected_post: " + selected_post
		print "selected_comment: " + selected_comment
		print "time: " + str(time.time() - temptime)