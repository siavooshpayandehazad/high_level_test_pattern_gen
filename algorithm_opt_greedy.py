import Logger
import sys, os
import copy
import itertools
import time
import package

sys.stdout = Logger.Logger()
generated_files_folder = "generated_files"

if os.path.exists("generated_files"):
	file_list = [file for file in os.listdir("generated_files")]
	for file in file_list:
		os.remove("generated_files"+'/'+file)
else:
    os.mkdir("generated_files")



def find_most_signifacant(function_dict, function_id_1, function_id_2, list_of_used_patterns, list_of_excluded_patterns, current_covered, debug, verbose):
	list_of_ones_in_ands = {}
	or_op = "00000000"
	not_covered = format(int("11111111", 2) ^ int(str(current_covered), 2), 'b').zfill(8)
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

if "--help" in sys.argv[1:] or len(sys.argv[1:]) == 0:
	print "---------------------------------------------------------------------------"
	print "\n     Copyright (C) 2017 Siavoosh Payandeh Azad, Stephen Oyeniran \n"
	print "This program optimizes test patterns generation between different functions"
	print "program arguments:"
	print "-i [file name]: spcifies the path to the input file" 
	print "-ot [file name]: spcifies the path to the generated table file" 
	print "-op [file name]: spcifies the path to the generated patterns file" 
	print "-v: makes it more verbose" 
	print "-debug: enables debug printing"
	print "---------------------------------------------------------------------------"
	sys.exit()

if "-i" in sys.argv[1:]:
	input_file_name= sys.argv[sys.argv.index('-i') + 1]

if "-v" in sys.argv[1:]:
	verbose = True
else:
	verbose = False

if "-debug" in sys.argv[1:]:
	debug = True
else:
	debug = False

if "-ot" in sys.argv[1:]:
	output_table_file_name= generated_files_folder + "/" + sys.argv[sys.argv.index('-ot') + 1]
else:
	output_table_file_name= generated_files_folder + "/" + "table.txt"
	
if "-op" in sys.argv[1:]:
	output_patterns_file_name= generated_files_folder + "/" + sys.argv[sys.argv.index('-op') + 1]
else:
	output_patterns_file_name= generated_files_folder + "/" + "patterns.txt"

start_time = time.time()
function_dict = {}
line_counter = 0
with open(input_file_name) as f:
	for line in f:
		if line != "":
			line_counter += 1
			list_of_functions =  line.split(" ")
			list_of_functions[len(list_of_functions)-1] = list_of_functions[len(list_of_functions)-1][:-2]
			function_dict[line_counter] = list_of_functions[1:]
			sorted_keys = sorted(function_dict.keys())

len_of_list = len(function_dict[function_dict.keys()[0]])
number_of_lines = len(function_dict.keys())

table_file = open(output_table_file_name, 'w')
string =  '%10s' %(" ")
for function in range(2, len_of_list):
	string += "\t"+'%8s' %("f_"+str(function-1)) # -1 to march the number of functions for readability
table_file.write(string+"\n")
string = '%10s' %(" ")+ "\t" + "------------"*(len_of_list-2)
table_file.write(string+"\n")

patterns_file = open(output_patterns_file_name, 'w')
test_patterns_file = open(generated_files_folder + "/" +"testpatterns.txt", 'w')

number_of_ones_in_experiments = 0
number_of_zeros_in_experiments = 0

final_set_of_patterns = []
for func_id_1 in range(2, len_of_list):
	string =  '%10s' %("f_"+str(func_id_1-1)+"|") # -1 to march the number of functions for readability
	for func_id_2 in range(2, len_of_list):		
		if func_id_1 != func_id_2:
			list_of_used_patterns =  range(1, number_of_lines+1)
			if verbose:
				print "------------------------------------------"*3
				print "function 1: ", func_id_1, "function 2:", func_id_2
				print "------------------------------------------"*3
			
			counter = 0
			list_of_excluded_patterns = []
			break_the_loop = False
			best_solution = []
			best_value = 0
			sufficient =  "00000000"
			while(counter < number_of_lines):
				list_of_ones_in_ands = find_most_signifacant(function_dict, func_id_1, func_id_2, list_of_used_patterns, list_of_excluded_patterns, sufficient, debug, verbose)
			 	#print list_of_ones_in_ands
			 	if len(list_of_ones_in_ands.keys())>0:
			 		if verbose:
					 	print "\tmax number of ones:", max(list_of_ones_in_ands.keys())
				 	
				 	if max(list_of_ones_in_ands.keys()) == 0: 
				 		break
				 	#old_found_patterns = copy.deepcopy(best_solution)
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
				print "best_solution for func ", func_id_1, " and func ", func_id_2, ": ", sufficient, best_solution
			for final_pattern in best_solution:
				if final_pattern not in final_set_of_patterns:
					final_set_of_patterns.append(final_pattern)
			patterns_file.write("--------------------------------\n")
			patterns_file.write("Pattern No\t"+'%8s'%("f_"+str(func_id_1))+"    "+"f_"+str(func_id_2)+"\n")
			patterns_file.write("---------\n")
		
			for item in best_solution:
				patterns_file.write('%10s' %str(item)+"\t"+str(function_dict[item][0])+"    "+str(function_dict[item][1])+"\n")
				
			string += "\t"+str(sufficient)

			if str(func_id_1-1)+"_"+str(func_id_2-1) in package.related_functions.keys():
				#print "here", func_id_1-1, func_id_2-1, sufficient, package.related_functions[str(func_id_1-1)+"_"+str(func_id_2-1)]
				number_of_zeros_in_experiments  += sufficient.count("0") - package.related_functions[str(func_id_1-1)+"_"+str(func_id_2-1)].count("0")
			elif sufficient != "00000000":
				number_of_zeros_in_experiments  += sufficient.count("0")
			number_of_ones_in_experiments  += sufficient.count("1")
			
		else:
			string += "\t"+"xxxxxxxx"
	table_file.write(string+"\n")
stop_time = time.time()

table_file.close()
patterns_file.close()
final_unsed_patterns = []
for item in range(1, number_of_lines+1):
	if item not in final_set_of_patterns:
		final_unsed_patterns.append(item)
print "------------------------------------------"*3
print "|"+"                                         "*3+" |"
print "|"+"                                         "+"                RESULTS                  "+"                                         "+" |"
print "|"+"                                         "*3+" |"
print "------------------------------------------"*3
print "final list of patterns used in the experiment:"
print "number of patterns used:", len(final_set_of_patterns)
print sorted(final_set_of_patterns)
print "------------------------------------------"*3
print "final list of patterns NOT used in the experiment:"
print "number of patterns NOT used:", len(final_unsed_patterns)
print sorted(final_unsed_patterns)

print "------------------------------------------"*3
print "------------------------------------------"*3
if verbose:
	print "final list of patterns"
for item in sorted(final_set_of_patterns):
		test_patterns_file.write(str(function_dict[item][0])+""+str(function_dict[item][1])+"\n")
		if verbose:
			print str(function_dict[item][0])+"    "+str(function_dict[item][1])
		

print "------------------------------------------"*3
print "|"+"                                         "+"             FAULT COVERAGE              "+"                                         "+" |"
print "------------------------------------------"*3
print "number of patterns:", number_of_lines
print "number of faults covered:", number_of_ones_in_experiments
print "number of faults not covered:" , number_of_zeros_in_experiments
print "NOTE: fault coverage =  (number of faults covered)/(number of faults covered + number of faults not covered)"
print "fault coverage :", "{:1.2f}".format(100*float(number_of_ones_in_experiments)/(number_of_ones_in_experiments+number_of_zeros_in_experiments)),"%"
print "------------------------------------------"*3
print "program took ", str(stop_time-start_time), "seconds"

test_patterns_file.close()
