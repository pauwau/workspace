#coding:utf-8

import subprocess
import re

if __name__ == '__main__':
	word = "ネコ イヌ 人"
	tmp_list = []
	echo = subprocess.Popen(['echo',word],
	                         stdout=subprocess.PIPE,
	                         )
	
	word2vec = subprocess.Popen(['./distance','dim200vecs13iter10.bin'],
								stdin = echo.stdout,
								stdout = subprocess.PIPE,
								)

	end_of_pipe_tab = word2vec.stdout
	fscanf(f, "%lld", words);
	fscanf(f, "%lld", size);
	vocab = (char *)malloc((long long)words * max_w * sizeof(char));
	for (a = 0; a < N; a++) bestw[a] = (char *)malloc(max_size * sizeof(char));
	M = (float *)malloc((long long)words * (long long)size * sizeof(float));
	if (M == NULL) {
		printf("Cannot allocate memory: %lld MB    %lld  %lld\n", (long long)words * size * sizeof(float) / 1048576, words, size);
		return -1;
	}
	for (b = 0; b < words; b++):
		a = 0;
		while (1):
			vocab[b * max_w + a] = fgetc(f);
			if (feof(f) || (vocab[b * max_w + a] == ' ')):
				break
			if ((a < max_w) && (vocab[b * max_w + a] != '\n')):
				a = a + 1
			vocab[b * max_w + a] = 0
			for (a = 0; a < size; a++) fread(&M[a + b * size], sizeof(float), 1, f)
			len = 0
			for (a = 0; a < size; a++):
				len += M[a + b * size] * M[a + b * size];
			len = sqrt(len)
			for (a = 0; a < size; a++) M[a + b * size] /= len;
		fclose(f);
	# flag = False
	# for line in end_of_pipe_tab:
	# 	line_split = line.split(" ")
	# 	tmp_list.append(line_split[0])
	# 	if("Enter word or sentence (EXIT to break):" in line and flag):
	# 		break
	# 	flag = True
	# 	print line,
	# print "end of process"