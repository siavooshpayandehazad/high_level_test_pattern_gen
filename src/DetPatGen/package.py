from ALU import *


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


def report_function_res(opt_patterns):
	file = open('pattern_set.txt', 'w')
	print "----------------------------------------------------"*3
	print "printing function results:"
	string = '%8s' %"OP1"+ " " + '%8s' %"OP2"
	for func in list_of_operations:
		string += " " +'%8s' %str(func) 
	print string
	print "---"*55

	for pattern in opt_patterns:
		string = "0000 " + numpy.binary_repr(pattern[0],8) + " " +numpy.binary_repr(pattern[1],8)+ " "
		for func in list_of_operations:
			string +=   numpy.binary_repr(alu(pattern[0], pattern[1], op_dic[func], 0), 8)[-8:]+ " "
		#print string
		file.write(string[:-1]+"\n")
	file.close()

def report_table(opt_patterns, print_to_console):
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
	return number_of_ones