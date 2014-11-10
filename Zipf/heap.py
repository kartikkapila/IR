from sets import Set
import math
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

input_file.close()
output_file.close()
input_file = open("total_words_vs_unique_words.txt","r")
output_file_xi = open("log_xi.txt","w")
output_file_yi = open("log_yi.txt","w")
output_answer = open("answer.txt","w")
input_list = []
x = []
y = []
x_avg = 0
y_avg = 0
sum_x = 0
sum_y = 0
sum_of_xi_square = 0
sum_of_yi_square = 0
sum_of_product_of_xi_yi = 0
b = 0
m = 0
k = 0
for word in input_file :
	words = word.split(" ")
	x.append(words.pop(0))
	y.append(words.pop(0).split("\n").pop(0))

n = len(x)
for xi,yi in zip(x,y) :
	log_xi = math.log(int(xi))
	output_file_xi.write(str(log_xi) + "\n")
	log_yi = math.log(int(yi))
	output_file_yi.write(str(log_yi) + "\n")
	sum_x += log_xi
	sum_of_xi_square += log_xi * log_xi
	sum_y += log_yi
	sum_of_yi_square += log_yi * log_yi
	sum_of_product_of_xi_yi += log_xi * log_yi
x_avg = float(sum_x) / n 
y_avg = float(sum_y) / n
b = float((y_avg * sum_of_xi_square) - (x_avg * sum_of_product_of_xi_yi)) / (sum_of_xi_square - (n * x_avg * x_avg))
m = float(sum_of_product_of_xi_yi - (n * x_avg * y_avg)) / (sum_of_xi_square - (n * x_avg * x_avg))
k = math.exp(b)
output_answer.write(str(k) + "\n" + str(m))
