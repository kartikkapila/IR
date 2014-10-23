from sets import Set
import operator
import time

input_file = open("output.txt","r")
input_list = []
output_file = open("wordBasedOnCount.txt","w")
wordAndCount = dict()

for word in input_file :
	input_list.append(word.split("\n").pop(0))
time.sleep(5)
unique_words = Set(input_list)

for unique_word in unique_words :
	wordAndCount[unique_word] = input_list.count(unique_word)
wordsSortedBasedonCount = sorted(wordAndCount.items(), key=operator.itemgetter(1), reverse = True)
count = 0
rank = 1
for word in wordsSortedBasedonCount : 
	if count <= 25 :
		output_file.write(word[0] + " " + str(word[1]) + " " + str(rank) + "\n")
		count += 1
	else :
		if word[0][:1] == 'f':
			output_file.write(word[0] + " " + str(word[1]) + " " + str(rank) +  "\n")
			count += 1
	rank += 1
	if count == 50:
		break
