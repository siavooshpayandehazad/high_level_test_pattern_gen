# Copyright (C) 2017 Siavoosh Payandeh Azad, Stephen Oyeniran

import Logger
import sys
import copy
import time
import package

generated_files_folder = "../generated_files"

package.generate_folders(generated_files_folder)
sys.stdout = Logger.Logger(generated_files_folder)

if "-sp" in sys.argv[1:]:
	saf_output_patterns_file_name= generated_files_folder + "/" +"SAF"+ sys.argv[sys.argv.index('-sp') + 1]
else:
	saf_output_patterns_file_name= generated_files_folder + "/" + "SAFpatterns.txt"

input_file_name, verbose, debug, output_table_file_name, output_patterns_file_name, scanning_table_file_name, redundant_function_reduction= package.parse_program_arg(sys.argv, generated_files_folder)

start_time = time.time()

function_dict = copy.deepcopy(package.parse_input_pattern_file(input_file_name))
len_of_list = len(function_dict[function_dict.keys()[0]])
number_of_lines = len(function_dict.keys())

table_file = open(output_table_file_name, 'w')
scanning_table_file = open(scanning_table_file_name, 'w')

package.make_table_header(table_file, len_of_list)
package.make_table_header(scanning_table_file, len_of_list)
 
saf_test_patterns_file = open(saf_output_patterns_file_name, 'w')
test_patterns_file = open(output_patterns_file_name, 'w')

deletion_dic = {}
used_dic = {}
number_of_ones_in_experiments = 0
number_of_zeros_in_experiments = 0
final_set_of_patterns = []
for func_id_1 in range(2, len_of_list):
	string =  '%10s' %("f_"+str(func_id_1-1)+"|") # -1 to march the number of functions for readability
	scanning_string =  '%10s' %("f_"+str(func_id_1-1)+"|") # -1 to march the number of functions for readability
 	list_of_used_patterns =  range(1, number_of_lines+1)
	list_of_necessary_patterns = []
	scanning_test_f1 = "00000000"
	for func_id_2 in range(2, len_of_list):	
		scanning_test_f1_f2 = "00000000"
		if func_id_1 != func_id_2:
			
			list_of_pattens_to_delete = []
			if verbose:
				print "---------------------------------------------------------------------------------------"
				print "---------------------------------------------------------------------------------------"
				print "function_1: ", func_id_1-1, "function_2:", func_id_2-1
				print "line\top1\t\top2\t\tfunc_1 \t\t func_2\t\txor(1,2)\tand(1,xor)\tor(prev_or,and)"
				print "---------------------------------------------------------------------------------------"
				print "starting with list: ", list_of_necessary_patterns

			or_op = "00000000"
			for i in list_of_necessary_patterns:
				xor_op = format(int(function_dict[i][func_id_1], 2) ^ int(function_dict[i][func_id_2], 2), 'b').zfill(8)
				and_op = format(int(function_dict[i][func_id_2], 2) & int(xor_op, 2), 'b').zfill(8)	
				or_op = format(int(or_op, 2) | int(and_op, 2), 'b').zfill(8)
				if verbose:
					print str(i)+"\t", function_dict[i][0],"\t", function_dict[i][1],"\t", function_dict[i][func_id_1], "\t", function_dict[i][func_id_2], "\t", xor_op, "\t"+str(and_op), "\t"+str(or_op)
			#print list_of_used_patterns
			for i in list_of_used_patterns:
				if i not in list_of_necessary_patterns:
					xor_op = format(int(function_dict[i][func_id_1], 2) ^ int(function_dict[i][func_id_2], 2), 'b').zfill(8)
					and_op = format(int(function_dict[i][func_id_2], 2) & int(xor_op, 2), 'b').zfill(8)
					prev_or = or_op
					or_op = format(int(or_op, 2) | int(and_op, 2), 'b').zfill(8)
					if prev_or == or_op or or_op == "00000000":
						if i not in list_of_necessary_patterns:
							list_of_pattens_to_delete.append(i)
							#print "adding pattern:", i, "to unused list"
					else:
						if or_op != "00000000":
							if i not in list_of_necessary_patterns:				
								list_of_necessary_patterns.append(i)
								if verbose:
									print str(i)+"\t", function_dict[i][0],"\t", function_dict[i][1],"\t", function_dict[i][func_id_1], "\t", function_dict[i][func_id_2], "\t", xor_op, "\t"+str(and_op), "\t"+str(or_op) , "\t\tadding pattern ", i, "to final pattern list!"
						if or_op == "11111111":
							if verbose:
								print  "INFO::  reached all ones!"
							break
			if or_op != "11111111":
				if verbose:
					print  "INFO::  Didn't find a solution!"

			string += "\t"+str(or_op)
			
			number_of_ones_in_experiments  += or_op.count("1")
			if redundant_function_reduction and (str(func_id_1-1)+"_"+str(func_id_2-1) in package.related_functions.keys()):
				#print "here", func_id_1-1, func_id_2-1, or_op, package.related_functions[str(func_id_1-1)+"_"+str(func_id_2-1)]
				number_of_zeros_in_experiments  += or_op.count("0") - package.related_functions[str(func_id_1-1)+"_"+str(func_id_2-1)].count("0")
			elif or_op != "00000000":
				number_of_zeros_in_experiments  += or_op.count("0")
			if verbose:
				print "------------------------------"

			for scan_pattern in list_of_necessary_patterns:
				scanning_test_f1_f2 = format(int(scanning_test_f1_f2, 2) | int(function_dict[scan_pattern][func_id_1], 2), 'b').zfill(8)
			

			if verbose:
				print "final list of patterns:", list_of_necessary_patterns
			for final_pattern in list_of_necessary_patterns:
				if final_pattern not in final_set_of_patterns:
					final_set_of_patterns.append(final_pattern)

			#print "final list of unused patterns:", list_of_pattens_to_delete
			deletion_dic['{0:03}'.format(func_id_1)+"_"+'{0:03}'.format(func_id_2)] = copy.deepcopy(list_of_pattens_to_delete)
			used_dic['{0:03}'.format(func_id_1)+"_"+'{0:03}'.format(func_id_2)] = copy.deepcopy(list_of_necessary_patterns)
			# if len(list_of_pattens_to_delete)>0 and len(list_of_necessary_patterns)>0: 
			# 	for item in list_of_pattens_to_delete:
			# 		if item < max(list_of_necessary_patterns):
			# 			if item in list_of_used_patterns:
			# 				if item not in list_of_necessary_patterns:
			# 					list_of_used_patterns.remove(item) 
			# 					#print "removed pattern no:", item

		else:
			string += "\t"+"xxxxxxxx"

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
			if scanning_dict[max_coverable_scanning][0] not in list_of_necessary_patterns:
				if verbose:
					print "adding pattern", scanning_dict[max_coverable_scanning][0], "to the list of solutions for scanning test!"
				list_of_necessary_patterns.append(scanning_dict[max_coverable_scanning][0])
				scanning_test_f1 = format(int(scanning_test_f1, 2) | int(function_dict[scanning_dict[max_coverable_scanning][0]][func_id_1], 2), 'b').zfill(8)
			if verbose:
				print "All ones!"
		elif max_coverable_scanning == 0:
			if verbose:
				print "scanning test can not be improved!"
		else:
			while max_coverable_scanning != 0:
				if scanning_dict[max_coverable_scanning][0] not in list_of_necessary_patterns:
					if verbose:
						print "adding pattern", scanning_dict[max_coverable_scanning][0], "to the list of solutions!"
					list_of_necessary_patterns.append(scanning_dict[max_coverable_scanning][0])
					scanning_test_f1 = format(int(scanning_test_f1, 2) | int(function_dict[scanning_dict[max_coverable_scanning][0]][func_id_1], 2), 'b').zfill(8)
					scanning_dict = package.find_most_signifacant_scanning(function_dict, func_id_1, scanning_test_f1, debug, verbose)
					max_coverable_scanning = max(scanning_dict.keys())
					if scanning_test_f1.count("0") == max_coverable_scanning:
						if scanning_dict[max_coverable_scanning][0] not in list_of_necessary_patterns:
							if verbose:
								print "adding pattern", scanning_dict[max_coverable_scanning][0], "to the list of solutions scanning test!"
							list_of_necessary_patterns.append(scanning_dict[max_coverable_scanning][0])
							scanning_test_f1 = format(int(scanning_test_f1, 2) | int(function_dict[scanning_dict[max_coverable_scanning][0]][func_id_1], 2), 'b').zfill(8)
						if verbose:
							print "All ones!"
						break

	scanning_string += "\t"+str(scanning_test_f1)
	scanning_table_file.write(scanning_string+"\n")					
	table_file.write(string+"\n")
	
	# Print patterns and functions.. This will be used to prepare test patterns for SAF testing in turbo tester
	# This should only be used for VLIW experiment. Modification will be needed for other processors
	if verbose:
		print "-----------------------------------------------------"
		print "function_1: ",func_id_1

	opcode = "{0:04b}".format((func_id_1-2))
	# test_patterns_file.write("function_1: "+str(func_id_1)+ " "+str(opcode)+"\n")
	for j in list_of_necessary_patterns:
		# test_patterns_file.write(str(j)+"\t"+function_dict[j][0]+"\t"+function_dict[j][1]+"\n")
		saf_test_patterns_file.write(function_dict[j][0]+function_dict[j][1]+opcode+"\n")
	# test_patterns_file.write("\n")

# final set of patterns	
for k in final_set_of_patterns:
	test_patterns_file.write(function_dict[k][0]+function_dict[k][1]+"\n")

table_file.close()
scanning_table_file.close()
test_patterns_file.close()
saf_test_patterns_file.close()
stop_time = time.time()

package.report_usefull_patterns_per_round(used_dic, len_of_list)

final_unsed_patterns = []
for item in range(1, number_of_lines+1):
	if item not in final_set_of_patterns:
		final_unsed_patterns.append(item)

package.print_results(final_set_of_patterns, final_unsed_patterns, verbose)
package.print_fault_coverage(number_of_lines, number_of_ones_in_experiments, number_of_zeros_in_experiments)

print "------------------------------------------"*3
print "program took ", str(stop_time-start_time), "seconds"