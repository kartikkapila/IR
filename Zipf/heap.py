from sets import Set
input_file = open("output.txt","r")
input_list = []
for word in input_file :
        input_list.append(word.split("\n").pop(0))
output_file = open("total_words_vs_unique_words.txt","w")
unique_words = Set()
unique_words_count = 0
words_processed = 0
for word in input_list :
	words_processed += 1
	if word not in unique_words :
		unique_words.add(word)
		unique_words_count += 1
		output_file.write(str(words_processed) + " " + str(unique_words_count) + "\n")
	else :
		output_file.write(str(words_processed) + " " + str(unique_words_count) + "\n")

	
