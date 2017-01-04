#coding:utf-8

import subprocess
import re

def distance(wordlist):
	input_echo = "\n".join(map(str,wordlist))
	tmp_list = []
	distlist = []

	echo1 = subprocess.Popen(['echo',input_echo],
		stdout=subprocess.PIPE,
		)

	word_to_word = subprocess.Popen(['./a.out','dim200vecs13iter10.bin'],
		stdin = echo1.stdout,
		stdout = subprocess.PIPE,
		)
	i = 0
	dist = 0
	end_of_pipe_tab1 = word_to_word.stdout
	for line in end_of_pipe_tab1:
		#print wordlist[i] + " : " + str(line)
		dist = float(line)
		distlist.append(line)
		i += 1
		if(len(wordlist) <= i):
			break
	#print distlist
	return distlist