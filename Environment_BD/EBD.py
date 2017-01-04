# -*- coding: utf-8 -*-

import AnomalyDetection # 矛盾
import SenselessDetection # 非常識
import UnfoundedDetection # 無根拠
from pyknp import KNP

def EBD(string):
	knp = KNP()
	knpParse = knp.parse(string)
	if(AnomalyDetection.AnomalyDetection(string,parseknp)):
		print ("Anomaly Detected")
	if(SenselessDetection.SenselessDetection(string)):
		print ("Senseless Detected")
	if(UnfoundedDetection.UnfoundedDetection(string)):
		print ("Unfounded Detected")
	print ("process end")
	return True

if __name__ == '__main__':
	string = u"クレジットを明記していただければ，商用利用も可能です．"
	EBD(string)