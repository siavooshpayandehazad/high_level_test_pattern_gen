from ALU import *
import numpy
from package import *
import sys
import copy

max_number_of_ones = 0
selected_patterns = []


counter = 0
counter_digits = 0
for op_1 in range(0, 256):
	for op_2 in range(0, 256):
		counter += 1
		pattern = [(op_1, op_2)]
		if pattern[0] not in selected_patterns:
			number_of_ones = report_table(selected_patterns+pattern, False)
			if number_of_ones > max_number_of_ones:
				print "found better solution with ", len(selected_patterns+pattern),"patterns with", number_of_ones, "ones! patterns counted:", counter
				report_table(selected_patterns+pattern, False)
				max_number_of_ones = number_of_ones
				best_pattern = pattern
				selected_patterns.append(best_pattern[0])
		#print counter
		if counter/1000>counter_digits:
			counter_digits = counter/1000
			print counter_digits
		if max_number_of_ones  == 1622:
			break
	if max_number_of_ones  == 1622:
		break
print "selected patterns:", selected_patterns
print "------------------------"*3
print selected_patterns
report_table(selected_patterns, True)