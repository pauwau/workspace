#coding:utf-8

import subprocess
import re
import time
while(1):
	word = "木 林\n木 森\n森 林"
	#word = raw_input()
	tmpt1 = time.time()
	tmp_list = []

	echo1 = subprocess.Popen(['echo',word],
		stdout=subprocess.PIPE,
		)

	word_to_word = subprocess.Popen(['./a.out','dim200vecs13iter10.bin'],
		stdin = echo1.stdout,
		stdout = subprocess.PIPE,
		)
	tmpt2 = time.time()

	dist = 0
	dist_l = word_to_word.stdout
	for temp_dist in dist_l:
		print word + " : " + str(temp_dist)
#		dist = float(line)

	tmpt3 = time.time()
	if(dist == 0):
		print ("out of dictionary word by word2vec")
	else:
		print "word_dist =" + str(dist)
	
	print "tmpt2 - tmpt1:" + str(tmpt2 - tmpt1)
	print "tmpt3 - tmpt2:" + str(tmpt3 - tmpt2)