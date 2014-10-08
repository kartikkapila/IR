from sets import Set
import re

P = Set()
NP = Set()
Si = Set()
M = dict()
L = dict()
PR = dict()
newPR = dict()
d = 0.85
d1 = 0.15
file = open("test1.txt","r")


def getPage(line) :
	return line.split().pop(0)

def getInLinks(line) :
	if " " not in line :
		return []
	listOfInLinksForLine = line.split() 
	listOfInLinksForLine.pop(0) 
	return listOfInLinksForLine

def initialize() :
	for line in file:
		page = getPage(str(line))
		P.add(page)
		M[page] = Set()
		listOfInLinks = getInLinks(str(line))
		for inLink in listOfInLinks :
			M[page].add(str(inLink))
			NP.add(str(inLink))
			if str(inLink) in L :
				L[str(inLink)] = L[str(inLink)] + 1
			else :	
				L[str(inLink)] = 1
initialize()
Si = P.difference(NP)

N = len(P)

for p in P :
	PR[p] = 1.0/N
count = 1
while count <= 10 :
	sinkPR = 0
	for sink in Si :
		sinkPR += PR[sink]
	for p in P :
		newPR[p] = d1/N
		newPR[p] += d*sinkPR/N
		for q in M[p]:
			newPR[p] += d*PR[q]/L[q]
	for p in P:
		PR[p] = newPR[p]
 	count += 1

for p in P :
	print p
	print PR[p]


