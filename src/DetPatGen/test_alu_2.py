from ALU import *
import numpy
from package import *
import sys
import copy

max_number_of_ones = 0
last_round_most_number_of_ones  = 0
selected_patterns = []

selected_patterns = [(172, 55), (83, 201), (150, 242), (105, 14), (53, 77), (200, 177)]
last_round_most_number_of_ones = report_table(selected_patterns, False)
max_number_of_ones = last_round_most_number_of_ones

while True:
	counter = 0
	for op_1 in range(0, 256):
		for op_2 in range(0, 256):
			counter += 1
			pattern = [(op_1, op_2)]
			if pattern[0] not in selected_patterns:
				number_of_ones = report_table(selected_patterns+pattern, False)
				if number_of_ones > max_number_of_ones:
					print "found better solution", selected_patterns+pattern," with", number_of_ones, "ones! patterns counted:", counter
					report_table(selected_patterns+pattern, False)
					max_number_of_ones = number_of_ones
					best_pattern = pattern
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