#-*- coding: utf-8 -*-

def TrueORFalse(i,answer2,overlap):
	if(i in answer2):
		return False
	if(len(answer2) == 1):
		if (answer2 + [i] in overlap):
			print "#########"
			return False
	return True

def overlapcounter(overlap,answer2,overlapcount):
	overlap2 = [[answer2[0],answer2[1]],[answer2[0],answer2[2]],[answer2[0],answer2[1]]]
	for o in overlap2:
		if (o in overlap):
			overlapcount(overlap.index(o)) = overlapcount(overlap.index(o)) + 1
		else:
			overlap.append(o)
			overlapcount.append(1)

if __name__ == '__main__':
	SourceArray = [10,10,7,7,7,7,7,7,7,7,7,7]
	Array = ["a","b","c","d","e","f","g","h","i","j","k","l",]
	answer1 = []
	overlap = []
	overlapcount = []
	while True:
		answer2 = []
		if(SourceArray == [0,0,0,0,0,0,0,0,0,0,0,0]):
			print SourceArray
			break
		for i in Array:
			flag = False
			if(TrueORFalse(i,answer2,overlap) and SourceArray[Array.index(i)] != 0):
				
				#print answer2
				answer2.append(Array[Array.index(i)])
				print answer2
				for a in overlap:
					if (answer2 == a):
						#print "########"
						flag == True
						break
				if (flag):
					answer2 = []
					continue
			if(len(answer2) > 2):
				answer1.append(answer2)
				for b in answer2:
					SourceArray[Array.index(b)] = SourceArray[Array.index(b)] - 1 
				overlap.append([answer2[0],answer2[1]])
				overlap.append([answer2[0],answer2[2]])
				overlap.append([answer2[1],answer2[2]])
				break
	print overlap
	print answer1
	print ("end process")
