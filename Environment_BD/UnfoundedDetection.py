# -*- coding: utf-8 -*-
import MeCab

def UnfoundedDetection(string):
	return False

if __name__ == '__main__':
	print("Please input utteranse!->")
	string = raw_input()
	if(AnomalyDetection(string)):
		print ("this string is not unfounded!")
	else:
		print ("this string is unfounded!")