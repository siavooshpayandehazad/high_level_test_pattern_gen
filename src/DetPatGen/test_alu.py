from ALU import *
import numpy
from package import *
import sys
import copy

print "----------------------------------"
print "description:"
print "\tThis program utilizes a high level description of an ALU to generate test patterns"
print "\there are the functions supported by ALU:"
print "\t\t",
for item in list_of_operations:
	print item,
print 
print "----------------------------------"
#print '%7s' %"func1",'%7s' %"func2", '%10s'%"op1", '%10s'%"op2",  "\t\t",'%10s'%"F1",'%10s'%"F2", '%15s'%"XOR(F1,F2)", '%15s'%"AND(XOR,F2)"
#print "-----------------"*6
carry = 0
full_list_of_ops = copy.deepcopy(list_of_operations)
k1_list = copy.deepcopy(list_of_operations)
patterns_taken = []
test_length = 0

for key1 in k1_list:
	current_patterns_taken = []
	print "checking function:", key1
	op_temp_dic = {
					"mov" 	:	"00000000" , "add" 	:	"00000000" ,
					"sub" 	:	"00000000" , "cmp" 	:	"00000000" ,
					"and" 	:	"00000000" , "or" 	:	"00000000" ,
					"xor" 	:	"00000000" , "not" 	:	"00000000" ,
					"shl" 	:	"00000000" , "shr" 	:	"00000000" ,
					"asr" 	:	"00000000" , "inc" 	:	"00000000" ,
					"dec" 	:	"00000000" , "rlc" 	:	"00000000" ,
					"rrc" 	:	"00000000" , "nop" 	:	"00000000" 
					}
	k2_list = copy.deepcopy(list_of_operations)
	for op1 in range(0, 256):
		for op2 in range(0, 256):
			for key2 in k2_list:
				if key1 != key2:
					#for carry in [0, 1]:
					op_1_bin =  numpy.binary_repr(op1, 8)
					op_2_bin =  numpy.binary_repr(op2, 8)
					func1 = alu(op1, op2, op_dic[key1], carry)	
					func2 = alu(op1, op2, op_dic[key2], carry)	

					carry_out1 = 0
					carry_out2 = 0
					if len(numpy.binary_repr(func1, 8))>8:
						carry_out1 = int(numpy.binary_repr(func1, 8)[0])
					if len(numpy.binary_repr(func2, 8))>8:
						carry_out2 = int(numpy.binary_repr(func2, 8)[0])
					binary1 = numpy.binary_repr(func1, 8)[-8: ]
					binary2 = numpy.binary_repr(func2, 8)[-8: ]
					
					xor_value = numpy.binary_repr(numpy.bitwise_xor(int(binary1, 2), int(binary2, 2)), 8) [-8: ]
					and_value = numpy.binary_repr(numpy.bitwise_and(int(xor_value, 2), int(binary2, 2)), 8) [-8: ]

					temp_or = numpy.binary_repr(numpy.bitwise_or(int(op_temp_dic[key2],2), int(and_value,2)), 8) 
					if int(op_temp_dic[key2],2) < int(temp_or, 2):
						#print '%7s' %key1,'%7s' %key2, '%10s'%op_1_bin, '%10s'%op_2_bin,  "\t\t",'%10s'%binary1,'%10s'%binary2, '%15s'%xor_value, '%15s'%and_value, '%15s'%op_temp_dic[key2]
						op_temp_dic[key2] = temp_or
						
						if (op1, op2) not in patterns_taken:
							patterns_taken.append((op1, op2))
						if (op1, op2) not in current_patterns_taken:
							print "\tselecting pattern for current function:", (op1, op2)
							current_patterns_taken.append((op1, op2))

					if op_temp_dic[key2] == "11111111":
						k2_list.remove(key2)
						#print "function ", key2, "is covered!"		
	del op_temp_dic
	test_length += len(current_patterns_taken)
	print "function:", key1, "fully examined!"
	print "number of patterns for the current function:", len(current_patterns_taken)
	print "number of patterns take so far:", len(patterns_taken)
	print "----------------------------------------"*3

 
print "test length:", test_length
report_table(patterns_taken, True)

print "-------------------------------------------------"
final_pattern_list = []
old_number_of_ones = 0
for pattern in patterns_taken:
	number_of_ones = report_table(final_pattern_list+[pattern], False)
	if number_of_ones > old_number_of_ones:
		print "selecting pattern", pattern, "number of ones improved to:", number_of_ones 
		final_pattern_list.append(pattern)
		old_number_of_ones = number_of_ones
	else:
		print "not picking pattern:", pattern
print "-------------------------------------------------"
print "number of patterns:", len(final_pattern_list)

report_function_res(final_pattern_list)
print "final list:", final_pattern_list
report_table(final_pattern_list, True)

print "-------------------------------------------------"

total_test_length = 0
for key1 in list_of_operations:
	func_pattern = []
	#print "finding test length for function", key1
	for key2 in list_of_operations:
		if key1 != key2:
			temp_or = "00000000"
			test_length  = 0
			for pattern in final_pattern_list:
				
				func1 = alu(pattern[0], pattern[1], op_dic[key1], 0)	
				func2 = alu(pattern[0], pattern[1], op_dic[key2], 0)	
				binary1 = numpy.binary_repr(func1, 8)[-8: ]
				binary2 = numpy.binary_repr(func2, 8)[-8: ]
				
				xor_value = numpy.binary_repr(numpy.bitwise_xor(int(binary1, 2), int(binary2, 2)), 8) [-8: ]
				and_value = numpy.binary_repr(numpy.bitwise_and(int(xor_value, 2), int(binary2, 2)), 8) [-8: ]
				new_or =  numpy.bitwise_or(int(temp_or,2), int(and_value,2))
				if int(temp_or,2) < new_or:
					#print key1, key2, numpy.binary_repr(pattern[0],8), numpy.binary_repr(pattern[1],8), binary1, binary2, xor_value, and_value, numpy.binary_repr(new_or)
					temp_or = numpy.binary_repr(new_or) [-8: ]
					if pattern not in func_pattern:
						
						func_pattern.append(pattern)
					#print "\tpattern taken:", numpy.binary_repr(pattern[0],8), numpy.binary_repr(pattern[1],8)
				if temp_or == "11111111": 
					break
			#print "-------------"
	print "test length for function", key1, "is:", len(func_pattern) 
	#print func_pattern
	total_test_length +=  len(func_pattern) 
print "-------------------------------------------"
print "total test length:",total_test_length