from ALU import *
import numpy
from package import *
import sys
import copy
import gc

max_number_of_ones = 0
last_round_most_number_of_ones  = 0
selected_patterns = []

selected_patterns = [(172, 55), (83, 201), (150, 242), (105, 14), (53, 77), 
					 (200, 177), (127, 126), (0, 1), (2, 30), (32, 32), (15, 0), 
					 (63, 0), (128, 128), (255, 128), (7, 0)] # 99.57% coverage
last_round_most_number_of_ones = report_table(selected_patterns, False)
max_number_of_ones = last_round_most_number_of_ones

while True:
	counter = 0
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
					print "found better solution", temp_list," with", number_of_ones, "ones! patterns counted:", counter
					#report_table(selected_patterns+pattern, False)
					max_number_of_ones = number_of_ones
					best_pattern = pattern
				del temp_list, number_of_ones
			#print op_1,op_2
			del pattern

	if last_round_most_number_of_ones < max_number_of_ones: 
		print "adding pattern", best_pattern, "to list of selected patterns!"
		selected_patterns.append(best_pattern[0])
		last_round_most_number_of_ones = max_number_of_ones
	else:
		break
	print "selected patterns:", selected_patterns
	print "------------------------"*3
print selected_patterns
report_table(selected_patterns, True)