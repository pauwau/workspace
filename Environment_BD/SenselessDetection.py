# -*- coding: utf-8 -*-

def SenselessDetection(string):
	return False

if __name__ == '__main__':
	print("Please input utteranse!->")
	string = raw_input()
	if(AnomalyDetection(string)):
		print ("this string is not Senseless!")
	else:
		print ("this string is Senseless!")