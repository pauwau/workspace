#coding: utf-8
import gensim
num_topic = 100

if __name__ == '__main__':
	f = open("lda_list.txt","w")
	lda = gensim.models.LdaModel.load('jawiki_lda.model')
	for i in range(0,num_topic):
		f.write(str(i) + ":" + lda.print_topic(i).encode("utf-8") + "\n")
		print i