from sets import Set
import operator
import time
import math

input_file = open("output.txt","r")
input_list = []
output_file = open("wordBasedOnCount.txt","w")
all_words = open("alldata.txt","w")
output_log_rank = open("log_rank.txt","w")
output_log_frequency = open("log_frequency.txt","w")
output_rank = open("rank.txt","w")
output_frequency = open("frequency.txt","w")
wordAndCount = dict()

for word in input_file :
	input_list.append(word.split("\n").pop(0))
unique_words = Set(input_list)

for unique_word in unique_words :
	wordAndCount[unique_word] = input_list.count(unique_word)
wordsSortedBasedonCount = sorted(wordAndCount.items(), key=operator.itemgetter(1), reverse = True)
count = 0
rank = 1
words_with_count_below_4 = 0
len_of_unique_words = len(unique_words)

for word in wordsSortedBasedonCount : 
	probability = float("{0:.8f}".format(float(word[1])/len(input_list)))
	if count < 25 :
		output_file.write(word[0] + "\t \t \t" + str(word[1]) + "\t" + str(rank) + "\t" + str(probability) + "\t \t" + str(rank * probability) +  "\n")
		count += 1
	elif count >= 25 and count < 50  :
		if word[0][:1] == 'm':
			output_file.write(word[0] + "\t \t \t" + str(word[1]) + "\t" + str(rank) + "\t" + str(probability) + "\t \t" + str(rank * probability) + "\n")
			count += 1
	all_words.write(word[0] + "\t \t \t" + str(word[1]) + "\t" + str(rank) + "\t" + str(probability) + "\t \t" + str(rank * probability) + "\n")
	output_log_rank.write(str(math.log(rank)) +"\n")
	output_log_frequency.write(str(math.log(word[1])) +"\n")
	output_rank.write(str(rank) + "\n")
	output_frequency.write(str(word[1]) +"\n")
	if word[1] <= 4 :
		words_with_count_below_4 += 1
	rank += 1

output_file.write("Total number of words" + str(len(input_list)) + "\n")
output_file.write("Total number of unique words" + str(len_of_unique_words))
all_words.write("\n" + "Total Number of words with count < 4:" + str(words_with_count_below_4) + "\n")

input_file.close()
output_file.close()
all_words.close()
