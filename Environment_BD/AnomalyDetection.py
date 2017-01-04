# -*- coding: utf-8 -*-
from anomary import Detect 

def AnomalyDetection(string,knpParse):
	flag = Detect.Detect(string,knpParse)
	return flag

if __name__ == '__main__':
	print("Please input utteranse!->")
	string = raw_input()
	if(AnomalyDetection(string)):
		print ("this string is not Anomaly!")
	else:
		print ("this string is Anomaly!")