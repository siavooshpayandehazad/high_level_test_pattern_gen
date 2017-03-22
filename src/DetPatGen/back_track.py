from ALU import *
import numpy
from package import *
import sys
import copy

list_of_patterns = [(0, 0), (0, 1), (1, 0), (1, 1), (1, 2), (1, 3), (1, 7), (1, 15), (1, 31), (1, 63), (1, 127), 
					(2, 0), (3, 0), (4, 0), (7, 0), (8, 0), (15, 0), (16, 0), (31, 0), (32, 0), (63, 0), (64, 0), 
					(127, 0), (128, 0), (128, 1), (1, 255), (2, 2), (2, 254), (4, 4), (8, 8), (16, 16), (32, 32), 
					(64, 64), (128, 128), (128, 129), (0, 3), (0, 5), (0, 9), (0, 17), (0, 33), (0, 65), (0, 129), 
					(2, 1), (4, 1), (8, 1), (16, 1), (32, 1), (64, 1), (0, 2), (0, 4), (0, 8), (0, 16), (0, 32), 
					(0, 64), (0, 128), (2, 4), (3, 4), (4, 2), (4, 8), (7, 8), (8, 4), (8, 16), (15, 16), (16, 8), 
					(16, 32), (31, 32), (32, 16), (32, 64), (63, 64), (64, 32), (64, 128), (127, 128), (128, 64), 
					(3, 2), (7, 4), (15, 8), (31, 16), (63, 32), (127, 64), (255, 0), (255, 128), (1, 4), (1, 8), 
					(1, 16), (1, 32), (1, 64), (1, 128), (1, 129), (5, 0), (9, 0), (17, 0), (33, 0), (65, 0), (129, 0)]

"description:"
print "in this program, we check all the test patterns in initial list of patterns against each other and "
print "will calculate f(P1) and f(P2) for all the functions in ALU..."
print "we say pattern P1 dominates pattern P2 if for all f in the ALU functions, f(P1) < f(P2)"
print "---------------------------------------"
print "starting with ", len(list_of_patterns), "patterns:"
print list_of_patterns
print "---------------------------------------"
pattern_list = copy.deepcopy(list_of_patterns)
for test_pattern_1 in list_of_patterns:
	if test_pattern_1 in pattern_list:
		for test_pattern_2 in pattern_list:
			if test_pattern_1 != test_pattern_2:
				p1_dominates_p2 = True
				for key1 in list_of_operations: 
					func1 = alu(test_pattern_1[0], test_pattern_1[1], op_dic[key1], 0)%256	
					func2 = alu(test_pattern_2[0], test_pattern_2[1], op_dic[key1], 0)%256
					#print numpy.binary_repr(func1, 8)[-8: ], numpy.binary_repr(func2, 8)[-8: ]
					if func1 < func2:
						p1_dominates_p2 = False
				if p1_dominates_p2:
					print "\tpattern: ", test_pattern_1, "\tdominates pattern: ", test_pattern_2, "\tremoving pattern ", test_pattern_2, "from the list of patterns!"
					pattern_list.remove(test_pattern_2)
print "-----------------------------------------"
print "number of remaining patterns: ", len(pattern_list)
print "final list of patterns:", pattern_list