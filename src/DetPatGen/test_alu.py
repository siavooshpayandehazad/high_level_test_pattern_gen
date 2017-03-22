from ALU import *
import numpy
from package import *
import sys
import copy
from back_track import back_track

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

for key1 in k1_list:
	print "checking function:", key1
	op_temp_dic = {
					"mov" 	:	"00000000" ,
					"add" 	:	"00000000" ,
					"sub" 	:	"00000000" ,
					"cmp" 	:	"00000000" ,
					"and" 	:	"00000000" ,
					"or" 	:	"00000000" ,
					"xor" 	:	"00000000" ,
					"not" 	:	"00000000" ,
					"shl" 	:	"00000000" ,
					"shr" 	:	"00000000" ,
					"asr" 	:	"00000000" ,
					"inc" 	:	"00000000" ,
					"dec" 	:	"00000000" ,
					"rlc" 	:	"00000000" ,
					"rrc" 	:	"00000000" ,
					"nop" 	:	"00000000" 
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
							print "\tselecting pattern:", (op1, op2)
							patterns_taken.append((op1, op2))
					if op_temp_dic[key2] == "11111111":
						k2_list.remove(key2)
						#print "function ", key2, "is covered!"		
	del op_temp_dic
	print "function:", key1, "fully examined!"
	print "number of patterns take so far:", len(patterns_taken)
	print "----------------------------------------"*3

#print len(patterns_taken)
#print patterns_taken
back_track(patterns_taken)

