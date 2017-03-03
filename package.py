import sys, os
# in this dictionary we describe untestable points between related functions!

# use the function number in the table file!
# "10000000" means that only the most significant bit is provable to be testable
# "01111111" the most significant bit is not testable
related_functions = { "10_11" : "10000000",  	# SHR, ASR
					  "11_10" : "10000000",		# ASR, SHR
					  "12_13" : "11111110",		# INC, DEC
					  "13_12" : "11111110",		# DEC, INC
					  "4_11"  : "01111111",		# CMP, ASR
					  "11_4"  : "01111111",		# ASR, CMP
					  "2_7"   : "11111110",		# ADD, XOR
					  "7_2"   : "11111110",		# XOR, ADD
					  "3_7"   : "11111110",		# SUB, XOR
					  "7_3"   : "11111110",		# XOR, SUB
					  "3_2"   : "11111110",		# SUB, ADD
					  "2_3"   : "11111110",		# ADD, SUB
					  "6_2"   : "11111110",		# OR, ADD
					  "6_3"   : "11111110",		# OR, SUB
					  "6_11"  : "01111111",		# OR, ASR
					  # "6_12"  : "01111111",	# OR, INC ?? 
					  "11_14"  : "01111111",	# ASR, RLC
					  "11_15"  : "01111111",	# ASR, RRC
					  "14_11"  : "01111111",	# ASR, RLC
					  "15_11"  : "01111111",	# ASR, RRC
					  "11_5"  : "01111111",		# ASR, ANd
}

def generate_folders(generated_files_folder):
	if os.path.exists(generated_files_folder):
		file_list = [file for file in os.listdir(generated_files_folder)]
		for file in file_list:
			os.remove(generated_files_folder+'/'+file)
	else:
	    os.mkdir(generated_files_folder)

def make_table_header(table_file, len_of_list):
	string =  '%10s' %(" ")
	for function in range(2, len_of_list):
		string += "\t"+'%8s' %("f_"+str(function-1)) # -1 to march the number of functions for readability
	table_file.write(string+"\n")
	string = '%10s' %(" ")+ "\t" + "------------"*(len_of_list-2)
	table_file.write(string+"\n")
	return None

def find_most_signifacant_scanning(function_dict, function_id_1, current_covered, debug, verbose):
	list_of_ones_in_ands = {}

	not_covered = format(int("11111111", 2) ^ int(str(current_covered), 2), 'b').zfill(8)		# inverse of the current_covered! to find what has not been covered so far
	if verbose:
		print "\tcurrently covered:", current_covered
		print "\tcurrently not covered:", not_covered
	for i in sorted(function_dict.keys()):
		new_ones =  format(int(not_covered, 2) & int(function_dict[i][function_id_1], 2), 'b').zfill(8) 
		if new_ones.count("1") in list_of_ones_in_ands.keys():
			list_of_ones_in_ands[new_ones.count("1")].append(i)
		else:
			list_of_ones_in_ands[new_ones.count("1")] = [i]
	return list_of_ones_in_ands

def print_results(final_set_of_patterns, final_unsed_patterns):
	print "------------------------------------------"*3
	print "|"+"                                         "*3+" |"
	print "|"+"                                         "+"                RESULTS                  "+"                                         "+" |"
	print "|"+"                                         "*3+" |"
	print "------------------------------------------"*3
	print "final list of patterns used in the experiment:"
	print "number of patterns used:", len(final_set_of_patterns)
	print sorted(final_set_of_patterns)

	#print "------------------------------------------"*3
	#print "final list of patterns NOT used in the experiment:"
	#print "number of patterns NOT used:", len(final_unsed_patterns)
	#print sorted(final_unsed_patterns)

def print_fault_coverage(number_of_lines, number_of_ones_in_experiments, number_of_zeros_in_experiments):
	print "------------------------------------------"*3
	print "|"+"                                         "+"             FAULT COVERAGE              "+"                                         "+" |"
	print "------------------------------------------"*3
	print "number of patterns:", number_of_lines
	print "number of faults covered:", number_of_ones_in_experiments
	print "number of faults not covered:" , number_of_zeros_in_experiments
	print "NOTE: fault coverage =  (number of faults covered)/(number of faults covered + number of faults not covered)"
	print "fault coverage :", "{:1.2f}".format(100*float(number_of_ones_in_experiments)/(number_of_ones_in_experiments+number_of_zeros_in_experiments)),"%"


def parse_program_arg(arguments, generated_files_folder):
	if "--help" in arguments[1:] or len(arguments[1:]) == 0:
		print "---------------------------------------------------------------------------"
		print "\n     Copyright (C) 2017 Siavoosh Payandeh Azad, Stephen Oyeniran \n"
		print "This program optimizes test patterns generation between different functions"
		print "program arguments:"
		print "-i [file name]: spcifies the path to the input file" 
		print "-ot [file name]: spcifies the path to the generated table file" 
		print "-ost [file name]: spcifies the path to the generated table file for scanning test" 
		print "-op [file name]: spcifies the path to the generated patterns file" 
		print "-v: makes it more verbose" 
		print "-debug: enables debug printing"
		print "---------------------------------------------------------------------------"
		sys.exit()

	if "-i" in arguments[1:]:
		input_file_name= arguments[arguments.index('-i') + 1]

	if "-v" in arguments[1:]:
		verbose = True
	else:
		verbose = False

	if "-debug" in arguments[1:]:
		debug = True
	else:
		debug = False

	if "-ot" in arguments[1:]:
		output_table_file_name= generated_files_folder + "/" + arguments[arguments.index('-ot') + 1]
	else:
		output_table_file_name= generated_files_folder + "/" + "table.txt"
		
	if "-op" in arguments[1:]:
		output_patterns_file_name= generated_files_folder + "/" + arguments[arguments.index('-op') + 1]
	else:
		output_patterns_file_name= generated_files_folder + "/" + "patterns.txt"

	if "-ost" in arguments[1:]:
		scanning_table_file_name= generated_files_folder + "/" + arguments[arguments.index('-ost') + 1]
	else:
		scanning_table_file_name= generated_files_folder + "/" + "scanning_table.txt"

	return input_file_name, verbose, debug, output_table_file_name, output_patterns_file_name, scanning_table_file_name