from ALU import *
import numpy
from package import *
import sys
import copy
import gc

max_number_of_ones = 0
last_round_most_number_of_ones  = 0
selected_patterns = [(172, 55), (83, 201), (150, 242), (105, 14)]
last_round_most_number_of_ones = report_table(selected_patterns, False)
max_number_of_ones = last_round_most_number_of_ones

while True:
	counter = 0
	this_rounds_good_solutions = []
	for op_1 in range(0, 256):
		for op_2 in range(0, 256):
			if (counter+1)/1000 > counter/1000:
				print "patterns counted:", counter+1, "\t"+str((float(counter)/(256*256))*100)+"% of search space covered!"
			counter += 1
			pattern = [(op_1, op_2)]
			if pattern[0] not in selected_patterns:
				temp_list = selected_patterns+pattern
				number_of_ones = report_table(temp_list, False)
				if number_of_ones > max_number_of_ones:
					#report_table(selected_patterns+pattern, False)
					this_rounds_good_solutions = [pattern[0]]
					max_number_of_ones = number_of_ones
					print "found better solution", temp_list," with", number_of_ones, "ones! patterns counted:", counter, "list of good solutions:", this_rounds_good_solutions 
				elif number_of_ones == max_number_of_ones:
					this_rounds_good_solutions.append(pattern[0])
					print "found good solution", temp_list," with", number_of_ones, "ones! patterns counted:", counter, "list of good solutions:", this_rounds_good_solutions
				del temp_list, number_of_ones
			#print op_1,op_2
			del pattern

	if last_round_most_number_of_ones < max_number_of_ones: 
		ones = 0
		for p in this_rounds_good_solutions:
			pattern_ones = report_table([p], False)
			if ones < pattern_ones:
				ones = pattern_ones
				best_pattern = [p]
		print "adding pattern", best_pattern, "to list of selected patterns!"
		selected_patterns.append(best_pattern[0])
		last_round_most_number_of_ones = max_number_of_ones
	else:
		break
	print "selected patterns:", selected_patterns
	print "------------------------"*3
print selected_patterns
report_table(selected_patterns, True)