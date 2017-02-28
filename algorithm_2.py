import Logger
import sys
import copy

sys.stdout = Logger.Logger()

if "--help" in sys.argv[1:] or len(sys.argv[1:]) == 0:
	print "---------------------------------------------------------------------------"
	print "\n     Copyright (C) 2017 Siavoosh Payandeh Azad, Stephen Oyeniran \n"
	print "This program optimizes test patterns generation between different functions"
	print "program arguments:"
	print "-i [file name]: spcifies the path to the input file" 
	#print "-ot [file name]: spcifies the path to the generated table file" 
	#print "-op [file name]: spcifies the path to the generated patterns file" 
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

if "-ot" in sys.argv[1:]:
	output_table_file_name= generated_files_folder + "/" + sys.argv[sys.argv.index('-ot') + 1]

if "-op" in sys.argv[1:]:
	output_patterns_file_name= generated_files_folder + "/" + sys.argv[sys.argv.index('-op') + 1]"""
	

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


deletion_dic = {}
used_dic = {}

for func_id_1 in range(2, len_of_list):
	
	list_of_used_patterns =  range(1, number_of_lines+1)
	list_of_necessary_patterns = []
	for func_id_2 in range(2, len_of_list):		
		if func_id_1 != func_id_2:
			
			list_of_pattens_to_delete = []
			print "---------------------------------------------------------------------------------------"
			print "---------------------------------------------------------------------------------------"
			print "function_1: ", func_id_1, "function_2:", func_id_2
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

			print "final list of patterns:", list_of_necessary_patterns
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