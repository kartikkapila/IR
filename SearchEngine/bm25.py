import operator
import math
import sys

invertedIndex = open(sys.argv[1], "r")
queries = open(sys.argv[2], "r")
noOfDocumentsToRank = sys.argv[3]

tokenInput = open("tokens.txt", "r")
rankOutput = open(sys.argv[4], "w")

index = dict()
tokens = dict()
score = dict()

noOfDocuments = 0
docLen = 0
avdl = 0
k1 = 1.2
b = 0.75
k2 = 100

for line in invertedIndex :
	if "#" in line :
		word = line.split(" ").pop(1).split("\n").pop(0)
		continue
	docIdsandCountList = line.split("\n").pop(0).split(" ")
	docIdsandCountList.pop()
	while len(docIdsandCountList) != 0 :
		if word not in index and word :
			index[word] = []
		left = docIdsandCountList.pop(0)
		right = docIdsandCountList.pop(0)
		index[word].append((left, right))


for line in tokenInput :
	inputList = line.split(" ")
	docId = inputList.pop(0)
	noOfDocuments += 1
	if docId not in tokens :
		lengthOfDoc = inputList.pop(0)
		docLen += int(lengthOfDoc)
		tokens[docId] = lengthOfDoc

avdl = float(docLen) / noOfDocuments

# evaluate queries
def findNoOfTimeTermOccursInQuery(term, query) :
	count = 0
	for terms in query.split(" ") :
		if terms == term :
			count += 1
	return count

def retrieveInvertedListforTerm(term) :
	if term in index :
		return index[term]
	else :
		return []

def calculateK(dl) :
	return 1.2 * (0.25 + (0.75 * float(dl)/avdl))

def isDocinList(term, docId) :
	for doc in index[term] :
		if doc[0] == docId :
			return True
	return False

def findCountinDoc(term, docId) :
	for docs in index[term]:
		if docs[0] == docId :
			return docs[1]
	return 0

def calculateBM25Score(invertedListofTerm, query) :
	for docs in invertedListofTerm :
		docId = docs[0]
		if docId in score :
			continue
		K = calculateK(tokens[docId])
		bm25Score = 0
		for term in query.split(" ") :
			if term == "" :
				continue
			ni = len(retrieveInvertedListforTerm(term))
			qfi = findNoOfTimeTermOccursInQuery(term, query)
			if isDocinList(term, docId) :
				fi = float(findCountinDoc(term, docId))
			else :
				fi = 0
			firstPart = math.log((noOfDocuments - ni + 0.5) / (ni + 0.5))
                        secondPart = ((k1 + 1) * fi) * ((k2 + 1) * qfi)
                        thirdPart = (K + fi) * (k2 + qfi)
                        bm25Score = bm25Score + (firstPart * (float(secondPart) / thirdPart))
		score[docId] = bm25Score

def findBM25Score(query) :
	invertedListofTerm = []
	for term in query.split(" ") :
		if term == "" :
			continue
		invertedListofTerm += retrieveInvertedListforTerm(term)
	calculateBM25Score(invertedListofTerm, query)

def printDocRanks(queryId) :
	global score
	rank = 1
	count = 0
	sorted_score = sorted(score.items(), key=operator.itemgetter(1), reverse=True)
	for score in sorted_score :
		if count == int(noOfDocumentsToRank) :
			break
		rankOutput.write(queryId + " " + "Q0" + " " + score[0] + " " + str(rank) + " " + str(score[1]) + " " +  "IR" + "\n")
		rank += 1
		count += 1

for line in queries :
	queryId = line.split("\t").pop(0)
	query = line.split("\t").pop(1).split("\n").pop(0)
	findBM25Score(query)
	printDocRanks(queryId)
	score = dict()
