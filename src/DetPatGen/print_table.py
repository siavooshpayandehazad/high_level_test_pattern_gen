from ALU import *
from package import report_function_res

op_dic = {
	"mov" 	:	"0000" ,
	"add" 	:	"0001" ,
	"sub" 	:	"0010" ,
	"cmp" 	:	"0011" ,
	"and" 	:	"0100" ,
	"or" 	:	"0101" ,
	"xor" 	:	"0110" ,
	"not" 	:	"0111" ,
	"shl" 	:	"1000" ,
	"shr" 	:	"1001" ,
	"asr" 	:	"1010" ,
	"inc" 	:	"1011" ,
	"dec" 	:	"1100" ,
	"rlc" 	:	"1101" ,
	"rrc" 	:	"1110" ,
	"nop" 	:	"1111" ,
}

# this list is used only to keep order of the op-codes... since dictionaries dont keep the keys in order!
list_of_operations = ["mov","add","sub","cmp","and","or" ,"xor","not" ,"shl","shr","asr","inc","dec","rlc","rrc","nop"]


opt_patterns = [(172, 55), (83, 201), (202, 174), (53, 80), 
				 (128, 133), (105, 105), (31, 31), (215, 244), 
				 (255, 224), (0, 2), (16, 16), (64, 64), 
				 (127, 0), (2, 0), (8, 8), (32, 32),
				 (15, 0), (63, 0)]
print_to_console = True

report_function_res(opt_patterns)

if print_to_console:
	print "----------------------------------------------------"*3
	print "reporting corss function table:"
	print  "\t",
	for func in list_of_operations:
		print '%8s' %str(func),
	print
number_of_ones = 0
for func1 in list_of_operations:
	string = str(func1)+"\t"
	for func2 in list_of_operations:
		if func1 != func2:
			or_val = "00000000"
			for pattern in opt_patterns:
				res_1 = alu(pattern[0], pattern[1], op_dic[func1], 0)	
				res_2 = alu(pattern[0], pattern[1], op_dic[func2], 0)	
				binary1 = numpy.binary_repr(res_1, 8)[-8: ]
				binary2 = numpy.binary_repr(res_2, 8)[-8: ]
				xor_value = numpy.binary_repr(numpy.bitwise_xor(int(binary1, 2), int(binary2, 2)), 8) [-8: ]
				and_value = numpy.binary_repr(numpy.bitwise_and(int(xor_value, 2), int(binary2, 2)), 8) [-8: ]
				or_val = numpy.binary_repr(numpy.bitwise_or(int(and_value, 2), int(or_val, 2)), 8) [-8: ]
			string += or_val+" "
			number_of_ones += or_val.count("1")
		else:
			string  += "XXXXXXXX"+" "
	if print_to_console:
		print string
if print_to_console:
	print "number of ones in the table:", number_of_ones

print "-------------------------------------------"
final_pattern_list = opt_patterns
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


print "-------------------------------------------"
print "checking the variation in ones in outputs of functions"
for pattern in opt_patterns:
	bit_8 = 0
	bit_7 = 0
	bit_6 = 0
	bit_5 = 0
	bit_4 = 0
	bit_3 = 0
	bit_2 = 0
	bit_1 = 0
	for function in list_of_operations:
		func1 = alu(pattern[0], pattern[1], op_dic[function], 0)
		binary1 = numpy.binary_repr(func1, 8)[-8: ]
		bit_8 += int(binary1[0])
		bit_7 += int(binary1[1])
		bit_6 += int(binary1[2])
		bit_5 += int(binary1[3])
		bit_4 += int(binary1[4])
		bit_3 += int(binary1[5])
		bit_2 += int(binary1[6])
		bit_1 += int(binary1[7])
	print opt_patterns.index(pattern), "\t",bit_8, "\t",bit_7, "\t",bit_6, "\t",bit_5, "\t",bit_4, "\t",bit_3, "\t",bit_2, "\t",bit_1