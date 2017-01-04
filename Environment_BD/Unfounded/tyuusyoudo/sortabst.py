# -*- coding: utf-8 -*-
'''
Created on 2016/09/18

@author: hayashi
'''
if __name__ == '__main__':
	rf = file("abst.csv","r")
	rw0 = file("sortedabst_over0.csv","w")
	rw10 = file("sortedabst_over10.csv","w")
	rw100 = file("sortedabst_over100.csv","w")
	rw1000 = file("sortedabst_over1000.csv","w")

	lines = rf.read().split("\n")
	arrayover1000 = []
	arrayover100 = []
	arrayover10 = []
	arrayover0 = []
	for line in lines:
		if(line == ""):
			break
		if(int(line.split(",")[2]) > 1000):
			arrayover1000.append(line.split(","))
		elif(int(line.split(",")[2]) > 100):
			arrayover100.append(line.split(","))
		elif(int(line.split(",")[2]) > 10):
			arrayover10.append(line.split(","))
		else:
			arrayover0.append(line.split(","))
	arrayover0 = sorted(arrayover0, key=lambda x: float(x[1])/float(x[2]))
	arrayover10 = sorted(arrayover10, key=lambda x: float(x[1])/float(x[2]))
	arrayover100 = sorted(arrayover100, key=lambda x: float(x[1])/float(x[2]))
	arrayover1000 = sorted(arrayover1000, key=lambda x: float(x[1])/float(x[2]))
	for a in arrayover0:
		rw0.write("%s,%s,%s\n"%(a[0],a[1],a[2]))
	for a in arrayover10:
		rw10.write("%s,%s,%s\n"%(a[0],a[1],a[2]))
	for a in arrayover100:
		rw100.write("%s,%s,%s\n"%(a[0],a[1],a[2]))
	for a in arrayover1000:
		rw1000.write("%s,%s,%s\n"%(a[0],a[1],a[2]))
	print ("process finished...!!")
