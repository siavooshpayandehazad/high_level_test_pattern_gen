from ALU import *
import numpy
from package import *
import sys

carry = 0
for key in list_of_operations:
	for op1 in range(0, 256):
		for op2 in range(0, 256):
			#for carry in [0, 1]:
			func = alu(op1, op2, op_dic[key], carry)	
			binary = numpy.binary_repr(func, 8)
			op_1_bin =  numpy.binary_repr(op1, 8)
			op_2_bin =  numpy.binary_repr(op2, 8)
			if len(binary)>8:
				carry_out = int(binary[0])
			else:
				carry_out = 0
			print '%5s' %key, '%10s'%op_1_bin, '%10s'%op_2_bin, '%2s'%carry, "\t\t",'%10s'%binary[-8: len(binary)], '%2s'%carry_out
