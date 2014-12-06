import time
import sys

corpus_input = open(sys.argv[1])
invertedIndexOutput = open(sys.argv[2],"w")
tokens = open("tokens.txt", "w")
docId = 0
previousDocId = -1
invertedIndex = dict()

def updateCountofWord(word, docId) :
	index = -1
	for docIdsAndTermFrequency in invertedIndex[word] :
		index += 1
		if docIdsAndTermFrequency[0] == docId :
			termCount = docIdsAndTermFrequency[1] + 1
			del invertedIndex[word][index]
			invertedIndex[word].append((docId, termCount))

def docIdPresent(word, docId) :
	for docIdsAndTermFrequency in invertedIndex[word] :
		if docIdsAndTermFrequency[0] == docId :
			return True
	return False

def main() :
	global previousDocId
	global docId

	for line in corpus_input :
		if "#" in line :
			if previousDocId != -1 :
				tokens.write(str(docId) + " " + str(wordCount) + "\n")
				previousDocId = docId
			else :
				previousDocId = docId
			docId = line.split(" ").pop(1).split("\n").pop(0)
			wordCount = 0
			continue
		for word in line.split(" ") :
			if "\n" in word :
				word = word.split("\n").pop(0)
			if word == '' :
				continue
			wordCount += 1
			if word in invertedIndex :
				if docIdPresent(word, docId) :
					updateCountofWord(word,docId)
				else :
					invertedIndex[word].append((docId,1))
			else :
				invertedIndex[word] = [(docId,1)]
	
	tokens.write(str(docId) + " " + str(wordCount) + "\n")
main()
for key in invertedIndex :
	invertedIndexOutput.write("# " + key + "\n")
	for value in invertedIndex[key] :
		invertedIndexOutput.write(str(value[0]) + " " + str(value[1]) + " ")
	invertedIndexOutput.write("\n")
