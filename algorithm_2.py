import Logger
import sys, os
import copy
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

if "--help" in sys.argv[1:] or len(sys.argv[1:]) == 0:
	print "---------------------------------------------------------------------------"
	print "\n     Copyright (C) 2017 Siavoosh Payandeh Azad, Stephen Oyeniran \n"
	print "This program optimizes test patterns generation between different functions"
	print "program arguments:"
	print "-i [file name]: specifies the path to the input file" 
	print "-ot [file name]: spcifies the path to the generated table file" 
	print "-op [file name]: specifies the path to the generated patterns file" 
	print "-sp [file name]: specifies the path to the generated SAFpatterns file" 
	#print "-v: makes it more verbose" 
	#print "-debug: enables debug printing"
	print "---------------------------------------------------------------------------"
	sys.exit()

if "-i" in sys.argv[1:]:
	input_file_name= sys.argv[sys.argv.index('-i') + 1]

"""if "-v" in sys.argv[1:]:
	verbose = True
else:
	verbose = False

if "-debug" in sys.argv[1:]:
	debug = True
else:
	debug = False
"""

if "-ot" in sys.argv[1:]:
	output_table_file_name= generated_files_folder + "/" + sys.argv[sys.argv.index('-ot') + 1]
else:
	output_table_file_name= generated_files_folder + "/" + "table.txt"

if "-sp" in sys.argv[1:]:
	saf_output_patterns_file_name= generated_files_folder + "/" +"SAF"+ sys.argv[sys.argv.index('-sp') + 1]
else:
	saf_output_patterns_file_name= generated_files_folder + "/" + "SAFpatterns.txt"
if "-op" in sys.argv[1:]:
	output_patterns_file_name= generated_files_folder + "/" + sys.argv[sys.argv.index('-op') + 1]
else:
	output_patterns_file_name= generated_files_folder + "/" + "final_patterns.txt"

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

saf_test_patterns_file = open(saf_output_patterns_file_name, 'w')
test_patterns_file = open(output_patterns_file_name, 'w')

deletion_dic = {}
used_dic = {}
number_of_ones_in_experiments = 0
number_of_zeros_in_experiments = 0
final_set_of_patterns = []
for func_id_1 in range(2, len_of_list):
	string =  '%10s' %("f_"+str(func_id_1-1)+"|") # -1 to march the number of functions for readability
	list_of_used_patterns =  range(1, number_of_lines+1)
	list_of_necessary_patterns = []
	for func_id_2 in range(2, len_of_list):		
		if func_id_1 != func_id_2:
			
			list_of_pattens_to_delete = []
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
								print str(i)+"\t", function_dict[i][0],"\t", function_dict[i][1],"\t", function_dict[i][func_id_1], "\t", function_dict[i][func_id_2], "\t", xor_op, "\t"+str(and_op), "\t"+str(or_op) , "\t\tadding pattern ", i, "to final pattern list!"
						if or_op == "11111111":
							print  "INFO::  reached all ones!"
							break
			if or_op != "11111111":
				print  "INFO::  Didn't find a solution!"

			string += "\t"+str(or_op)

			number_of_ones_in_experiments  += or_op.count("1")
			if str(func_id_1-1)+"_"+str(func_id_2-1) in package.related_functions.keys():
				#print "here", func_id_1-1, func_id_2-1, or_op, package.related_functions[str(func_id_1-1)+"_"+str(func_id_2-1)]
				number_of_zeros_in_experiments  += or_op.count("0") - package.related_functions[str(func_id_1-1)+"_"+str(func_id_2-1)].count("0")
			elif or_op != "00000000":
				number_of_zeros_in_experiments  += or_op.count("0")
			print "final list of patterns:", list_of_necessary_patterns
			for final_pattern in list_of_necessary_patterns:
				if final_pattern not in final_set_of_patterns:
					final_set_of_patterns.append(final_pattern)
			
			#print "final list of unused patterns:", list_of_pattens_to_delete
			deletion_dic['{0:03}'.format(func_id_1)+"_"+'{0:03}'.format(func_id_2)] = copy.deepcopy(list_of_pattens_to_delete)
			used_dic['{0:03}'.format(func_id_1)+"_"+'{0:03}'.format(func_id_2)] = copy.deepcopy(list_of_necessary_patterns)
			if len(list_of_pattens_to_delete)>0 and len(list_of_necessary_patterns)>0: 
				for item in list_of_pattens_to_delete:
					if item < max(list_of_necessary_patterns):
						if item in list_of_used_patterns:
							if item not in list_of_necessary_patterns:
								list_of_used_patterns.remove(item) 
								#print "removed pattern no:", item
		else:
			string += "\t"+"xxxxxxxx"
	table_file.write(string+"\n")
	# Print patterns and functions.. This will be used to prepare test patterns for SAF testing in turbo tester
	# This should only be used for VLIW experiment. Modification will be needed for other processors
	print "-----------------------------------------------------"
	print "function_1: ",func_id_1
	pat =[]
	opcode = "{0:04b}".format((func_id_1-2))
	#test_patterns_file.write("function_1: "+str(func_id_1)+ " "+str(opcode)+"\n")
	for j in list_of_necessary_patterns:
		#test_patterns_file.write(str(j)+"\t"+function_dict[j][0]+"\t"+function_dict[j][1]+"\n")
		saf_test_patterns_file.write(function_dict[j][0]+function_dict[j][1]+opcode+"\n")
	#test_patterns_file.write("\n")

# final set of patterns	
for k in final_set_of_patterns:
	test_patterns_file.write(function_dict[k][0]+function_dict[k][1]+"\n")

test_patterns_file.close()
saf_test_patterns_file.close()
stop_time = time.time()


print "final list of patterns:", list_of_used_patterns

print "-----------------------------------------------------"
print "list of possible removals for each pair of functions:"
print "function pair", "\t", "\t", '%100s' % "usefull patterns"
print "-------------", "\t", "\t", '%100s' % "----------------"
counter = 1
for item in sorted(deletion_dic.keys()):
	print '%10s' %item, "\t",'%100s' %used_dic[item]
	counter += 1
	if counter == len_of_list-2:
		print "------------------------------------------------------------"*2
		counter = 1


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
print "|"+"                                         "+"             FAULT COVERAGE              "+"                                         "+" |"
print "------------------------------------------"*3
print "number of faults covered:", number_of_ones_in_experiments
print "number of faults not covered:" , number_of_zeros_in_experiments
print "NOTE: fault coverage =  (number of faults covered)/(number of faults covered + number of faults not covered)"
print "fault coverage :", "{:1.2f}".format(100*float(number_of_ones_in_experiments)/(number_of_ones_in_experiments+number_of_zeros_in_experiments)),"%"
print "------------------------------------------"*3
print "program took ", str(stop_time-start_time), "seconds"