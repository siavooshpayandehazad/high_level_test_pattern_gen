# Copyright (C) 2017 Siavoosh Payandeh Azad, Stephen Oyeniran

import Logger
import sys
import copy
import itertools
import time
import package

generated_files_folder = "../generated_files"
package.generate_folders(generated_files_folder)
sys.stdout = Logger.Logger(generated_files_folder)



def find_most_signifacant(function_dict, function_id_1, function_id_2, list_of_used_patterns, list_of_excluded_patterns, current_covered, debug, verbose):
	list_of_ones_in_ands = {}
	or_op = "00000000"
	not_covered = format(int("11111111", 2) ^ int(str(current_covered), 2), 'b').zfill(8)		# inverse of the current_covered! to find what has not been covered so far
	if verbose:
		print "\tcurrently covered:", current_covered
		print "\tcurrently not covered:", not_covered
	if debug:
		print "\tfinding the patterns with most uncovered ones!"
		print "\t\tline\top1\t\top2\t\tfunc_1 \t\t func_2\t\txor(1,2)\tand(1,xor)\tor(prev_or,and)"
		print "\t\t"+"------------------------------------------"*3
	for i in sorted(function_dict.keys()):
		if i in list_of_used_patterns:
			if i not in list_of_excluded_patterns:
				xor_op = format(int(function_dict[i][function_id_1], 2) ^ int(function_dict[i][function_id_2], 2), 'b').zfill(8)
				and_op = format(int(function_dict[i][function_id_2], 2) & int(xor_op, 2), 'b').zfill(8)
				new_ones =  format(int(not_covered, 2) & int(and_op, 2), 'b').zfill(8) 
				if new_ones.count("1") in list_of_ones_in_ands.keys():
					list_of_ones_in_ands[new_ones.count("1")].append(i)
				else:
					list_of_ones_in_ands[new_ones.count("1")] = [i]
				or_op = format(int(or_op, 2) | int(and_op, 2), 'b').zfill(8)		
				if debug:		
					print "\t\t"+str(i)+"\t", function_dict[i][0],"\t", function_dict[i][1],"\t", function_dict[i][function_id_1], "\t", function_dict[i][function_id_2], "\t", xor_op, "\t"+str(and_op), "\t"+str(or_op)
	return list_of_ones_in_ands

def check_if_sufficient(function_dict, function_id_1, function_id_2, list_patterns, debug, verbose):
	or_op = "00000000"
	if debug:
		print "\t--------------------"
		print "\tchecking if sufficient number of ones reached!"
		print "\t\tline\top1\t\top2\t\tfunc_1 \t\t func_2\t\txor(1,2)\tand(1,xor)\tor(prev_or,and)"
		print "\t\t"+"------------------------------------------"*3
	for i in list_patterns:
		xor_op = format(int(function_dict[i][function_id_1], 2) ^ int(function_dict[i][function_id_2], 2), 'b').zfill(8)
		and_op = format(int(function_dict[i][function_id_2], 2) & int(xor_op, 2), 'b').zfill(8)
		or_op = format(int(or_op, 2) | int(and_op, 2), 'b').zfill(8)
		if debug:
			print "\t\t"+str(i)+"\t", function_dict[i][0],"\t", function_dict[i][1],"\t", function_dict[i][function_id_1], "\t", function_dict[i][function_id_2], "\t", xor_op, "\t"+str(and_op), "\t"+str(or_op)
	if or_op == "11111111":
		if verbose:
			print "\tbingo! all ones!"
		return or_op
	else:
		if debug and verbose:
			print "\tdidnt reach all ones!"
		return or_op

input_file_name, verbose, debug, output_table_file_name, output_patterns_file_name, scanning_table_file_name, redundant_function_reduction = package.parse_program_arg(sys.argv, generated_files_folder)

start_time = time.time()

function_dict = copy.deepcopy(package.parse_input_pattern_file(input_file_name))
len_of_list = len(function_dict[function_dict.keys()[0]])
number_of_lines = len(function_dict.keys())

try:
	table_file = open(output_table_file_name, 'w')
	scanning_table_file = open(scanning_table_file_name, 'w')
	test_patterns_file = open(output_patterns_file_name, 'w')
except IOError:
    print "Could not open input pattern file, test pattern file, conformity or scanning table file!"
    sys.exit()

package.make_table_header(table_file, len_of_list)
package.make_table_header(scanning_table_file, len_of_list)

number_of_ones_in_experiments = 0
number_of_zeros_in_experiments = 0
used_dic = {}
final_set_of_patterns = []

for func_id_1 in range(2, len_of_list):
	scanning_test_f1 = "00000000"
	string =  '%10s' %("f_"+str(func_id_1-1)+"|") # -1 to march the number of functions for readability
	scanning_string =  '%10s' %("f_"+str(func_id_1-1)+"|") # -1 to march the number of functions for readability
	scanning_test_f1 = "00000000"
	for func_id_2 in range(2, len_of_list):		
		if func_id_1 != func_id_2:
			scanning_test_f1_f2 = "00000000"
			list_of_used_patterns =  range(1, number_of_lines+1)
			if verbose:
				print "------------------------------------------"*3
				print "function 1: ", func_id_1-1, "function 2:", func_id_2-1
				print "------------------------------------------"*3
			
			counter = 0
			list_of_excluded_patterns = copy.deepcopy(final_set_of_patterns)
			break_the_loop = False
			best_solution = []
			best_value = 0

			sufficient =  check_if_sufficient(function_dict, func_id_1, func_id_2, list_of_excluded_patterns, debug, verbose)

			while(counter < number_of_lines):
				list_of_ones_in_ands = find_most_signifacant(function_dict, func_id_1, func_id_2, list_of_used_patterns, list_of_excluded_patterns, sufficient, debug, verbose)
			 	if len(list_of_ones_in_ands.keys())>0:
			 		if verbose:
					 	print "\tmax number of ones:", max(list_of_ones_in_ands.keys())
				 	
				 	if max(list_of_ones_in_ands.keys()) == 0: 
				 		break
				 	list_of_best_patterns = list_of_ones_in_ands[max(list_of_ones_in_ands.keys())]
				 	if verbose:
					 	print "\tbest patterns in this round:", list_of_best_patterns
					for item in list_of_best_patterns:
						if type(item) == int: 
							item = [item]
						if verbose:
							print "\t----------------------"
							print "\ttrying combination: ", list_of_excluded_patterns+list(item)
						
						sufficient =  check_if_sufficient(function_dict, func_id_1, func_id_2, list_of_excluded_patterns+list(item), debug, verbose)
						if sufficient.count("1") == len(sufficient):
						 	best_solution = copy.deepcopy(list_of_excluded_patterns+list(item))
						 	if verbose:
							 	print "\twe got it!"
						 	break_the_loop = True
						 	break
						else:
							if verbose:
								print "\tnew number of ones :", sufficient.count("1"), "\t\tprevious value:", best_value
							if sufficient.count("1") > best_value:
								if verbose:
									print "\tfound a better solution!"
						 		list_of_excluded_patterns += list(item)
						 		best_solution = copy.deepcopy(list_of_excluded_patterns)
						 		best_value = sufficient.count("1")
						 		
						 		break
						if break_the_loop:
							break
					if break_the_loop:
							break 		
					counter += 1
				else:
					break
				if verbose:
					print "\t------------------------------------------------------------------"
			if verbose:
				print "best conformity solution for func ", func_id_1-1, " and func ", func_id_2-1, ": ", sufficient, best_solution

			

			if verbose:
				print "------------------------------"

			for final_pattern in best_solution:
				if final_pattern not in final_set_of_patterns:
					final_set_of_patterns.append(final_pattern)
			 
				
			string += "\t"+str(sufficient)

			for scan_pattern in best_solution:
				scanning_test_f1_f2 = format(int(scanning_test_f1_f2, 2) | int(function_dict[scan_pattern][func_id_1], 2), 'b').zfill(8)
 
			if redundant_function_reduction and (str(func_id_1-1)+"_"+str(func_id_2-1) in package.related_functions.keys()):
				#print "here", func_id_1-1, func_id_2-1, sufficient, package.related_functions[str(func_id_1-1)+"_"+str(func_id_2-1)]
				number_of_zeros_in_experiments  += sufficient.count("0") - package.related_functions[str(func_id_1-1)+"_"+str(func_id_2-1)].count("0")
			elif sufficient != "00000000":
				number_of_zeros_in_experiments  += sufficient.count("0")
			number_of_ones_in_experiments  += sufficient.count("1")
			
			used_dic['{0:03}'.format(func_id_1)+"_"+'{0:03}'.format(func_id_2)] = copy.deepcopy(final_set_of_patterns)
		else:
			scanning_test_f1_f2 = "00000000"
			string += "\t"+"xxxxxxxx"

	#print "SCANNING RESULT for function", func_id_1, ": ", scanning_test
		scanning_test_f1 =  format(int(scanning_test_f1, 2) | int(scanning_test_f1_f2, 2), 'b').zfill(8)
		scanning_string += "\t"+str(scanning_test_f1_f2)

	#-------------------------------------------------------------------------------
	#	This part fixes the scanning test results for the current function pair
	#-------------------------------------------------------------------------------
	
	if scanning_test_f1.count("1") != len(scanning_test_f1):
		scanning_dict = package.find_most_signifacant_scanning(function_dict, func_id_1, scanning_test_f1, debug, verbose)
		max_coverable_scanning = max(scanning_dict.keys())
		if verbose:
			print "number of missing ones:", scanning_test_f1.count("0")
			print "max ones that can be covered:", max_coverable_scanning
		if scanning_test_f1.count("0") == max_coverable_scanning:
			if scanning_dict[max_coverable_scanning][0] not in best_solution:
				if verbose:
					print "adding pattern", scanning_dict[max_coverable_scanning][0], "to the list of solutions for scanning test!"
				best_solution.append(scanning_dict[max_coverable_scanning][0])
				scanning_test_f1 = format(int(scanning_test_f1, 2) | int(function_dict[scanning_dict[max_coverable_scanning][0]][func_id_1], 2), 'b').zfill(8)
			if verbose:
				print "All ones!"
		elif max_coverable_scanning == 0:
			if verbose:
				print "scanning test can not be improved!"
		else:
			while max_coverable_scanning != 0:
				if scanning_dict[max_coverable_scanning][0] not in best_solution:
					if verbose:
						print "adding pattern", scanning_dict[max_coverable_scanning][0], "to the list of solutions!"
					best_solution.append(scanning_dict[max_coverable_scanning][0])
					scanning_test_f1 = format(int(scanning_test_f1, 2) | int(function_dict[scanning_dict[max_coverable_scanning][0]][func_id_1], 2), 'b').zfill(8)
					scanning_dict = package.find_most_signifacant_scanning(function_dict, func_id_1, scanning_test_f1, debug, verbose)
					max_coverable_scanning = max(scanning_dict.keys())
					if scanning_test_f1.count("0") == max_coverable_scanning:
						if scanning_dict[max_coverable_scanning][0] not in best_solution:
							if verbose:
								print "adding pattern", scanning_dict[max_coverable_scanning][0], "to the list of solutions scanning test!"
							best_solution.append(scanning_dict[max_coverable_scanning][0])
							scanning_test_f1 = format(int(scanning_test_f1, 2) | int(function_dict[scanning_dict[max_coverable_scanning][0]][func_id_1], 2), 'b').zfill(8)
						if verbose:
							print "All ones!"
						break

	scanning_string += "\t"+str(scanning_test_f1)
	scanning_table_file.write(scanning_string+"\n")					
	table_file.write(string+"\n")

 

stop_time = time.time()

final_unsed_patterns = []
for item in range(1, number_of_lines+1):
	if item not in final_set_of_patterns:
		final_unsed_patterns.append(item)

for item in sorted(final_set_of_patterns):
	test_patterns_file.write(str(function_dict[item][0])+""+str(function_dict[item][1])+"\n")

# reports!
package.report_usefull_patterns_per_round(used_dic, len_of_list)
package.print_results(final_set_of_patterns, final_unsed_patterns, verbose)
package.print_fault_coverage(number_of_lines, number_of_ones_in_experiments, number_of_zeros_in_experiments)

print "------------------------------------------"*3
print "program took ", str(stop_time-start_time), "seconds"

# closing all files
table_file.close()
scanning_table_file.close()
test_patterns_file.close()
