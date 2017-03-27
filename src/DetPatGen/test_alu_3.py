from ALU import *
import numpy
from package import *
import sys
import copy

max_number_of_ones = 0
selected_patterns = []

# these are the final results of the program:
# selected_patterns = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 8), (0, 9), 
# 					 (0, 16), (0, 17), (0, 32), (0, 33), (0, 64), (0, 65), (0, 128), 
# 					 (0, 129), (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 7), (1, 8), 
# 					 (1, 15), (1, 16), (1, 31), (1, 32), (1, 63), (1, 64), (1, 127), 
# 					 (1, 128), (1, 255), (2, 0), (2, 1), (2, 2), (2, 4), (3, 0), 
# 					 (3, 2), (3, 4), (4, 0), (4, 1), (4, 2), (4, 4), (4, 8), (5, 0), 
# 					 (7, 0), (7, 4), (7, 8), (8, 0), (8, 1), (8, 4), (8, 8), (8, 16), 
# 					 (9, 0), (15, 0), (15, 8), (15, 16), (16, 0), (16, 1), (16, 8), 
# 					 (16, 16), (16, 32), (17, 0), (31, 0), (31, 16), (31, 32), (32, 0), 
# 					 (32, 1), (32, 16), (32, 32), (32, 64), (33, 0), (63, 0), (63, 32), 
# 					 (63, 64), (64, 0), (64, 1), (64, 32), (64, 64), (64, 128), (65, 0), 
# 					 (127, 0), (127, 64), (127, 128), (128, 0), (128, 1), (128, 64), 
# 					 (128, 128), (129, 0), (255, 0), (255, 128)]
# 
# max_number_of_ones = report_table(selected_patterns, False)

print "starting with", len(selected_patterns), "patterns with ", max_number_of_ones, "ones!"
counter = 128*256
for op_1 in range(129, 256):
	for op_2 in range(0, 256):
		counter += 1
		pattern = [(op_1, op_2)]
		if pattern[0] not in selected_patterns:
			number_of_ones = report_table(selected_patterns+pattern, False)
			if number_of_ones > max_number_of_ones:
				print "found better solution with ", len(selected_patterns+pattern),"patterns with", number_of_ones, "ones! patterns counted:", counter
				print selected_patterns+pattern
				#report_table(selected_patterns+pattern, False)
				max_number_of_ones = number_of_ones
				best_pattern = pattern
				selected_patterns.append(best_pattern[0])
		#print counter
		if (counter+1)/1000 > counter/1000:
				print "patterns counted:", counter+1, "\t"+str((float(counter)/(256*256))*100)+"% of search space covered!"
		if max_number_of_ones  == 1622:
			break
	if max_number_of_ones  == 1622:
		break
print "selected patterns:", selected_patterns
print "------------------------"*3
print selected_patterns
report_table(selected_patterns, True)