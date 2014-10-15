from sets import Set
from math import log
import re
import operator
import sys

P = Set()
NP = Set()
Si = Set()
M = dict()
Mcopy = dict()
L = dict()
PR = dict()
newPR = dict()
d = 0.85
d1 = 1 - d
perplexity_list = []

infile = sys.argv[1]

input_file = open(infile,"r")
perplexity_output = open("perplexity.txt","w")

def getPage(line) :
	return line.split().pop(0)

def getInLinks(line) :
	if " " not in line :
		return []
	listOfInLinksForLine = line.split() 
	listOfInLinksForLine.pop(0) 
	return Set(listOfInLinksForLine)

def hasNotConverged() :
	H = 0
	for p in P :
		H += PR[p] * log(1.0/PR[p], 2)
	perplexity = 2**H
	perplexity_output.write(str(perplexity))
	perplexity_output.write("\n")
	length_of_perplexity_list = len(perplexity_list)
	if length_of_perplexity_list > 0 :
		if abs(perplexity_list[length_of_perplexity_list - 1] - perplexity) < 1 :
			perplexity_list.append(perplexity)
		else :
			del  perplexity_list[:]
	else :
		perplexity_list.append(perplexity)
	if len(perplexity_list) == 4 :
		return False
	return True

def initialize() :
	for line in input_file :
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
#count = 1
#while count <= 100 :
while hasNotConverged() :
	sinkPR = 0
	for sink in Si :
		sinkPR += PR[sink]
	for p in P :
		newPR[p] = d1/N
		newPR[p] += d*sinkPR/N
		for q in M[p]:
			newPR[p] += d*PR[q]/L[q]
	for p in P :
		PR[p] = newPR[p]

file_of_sorted_items = open("sortedPageRank.txt","w")
sorted_list = sorted(PR.items(), key=operator.itemgetter(1), reverse=True)
top50 = 1
for p in sorted_list :
	file_of_sorted_items.write(p[0] + " " + str(p[1]))
	file_of_sorted_items.write("\n")
	top50 += 1
	if top50 > 50 :
		break

for key, value in M.items() :
	Mcopy[key] = len(value)

file_of_sorted_items_inLinks = open("sortedInLinks.txt","w")
sorted_list = sorted(Mcopy.items(), key=operator.itemgetter(1), reverse=True)
top50 = 1
for p in sorted_list :
	file_of_sorted_items_inLinks.write(p[0] + " " + str(p[1]))
	file_of_sorted_items_inLinks.write("\n")
	top50 += 1
	if top50 > 50:
		break
input_file.close()
perplexity_output.close()
file_of_sorted_items.close()
file_of_sorted_items_inLinks.close()
