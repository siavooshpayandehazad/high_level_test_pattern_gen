import numpy

def alu( op1, op2, alu_op, c_in):
	if 	 alu_op == "0000": 	# mov
		result = op2
	elif alu_op == "0001": 	# add
		result = op1 + op2
	elif alu_op == "0010": 	# sub
		result = op1 - op2
	elif alu_op == "0011": 	# cmp
		result = op1
	elif alu_op == "0100": 	# and 
		result = numpy.bitwise_and(op1, op2)
	elif alu_op == "0101": 	# or
		result = numpy.bitwise_or(op1, op2)
	elif alu_op == "0110": 	# xor
		result = numpy.bitwise_xor(op1, op2)
	elif alu_op == "0111": 	# not 
		result = numpy.invert(op2)
	elif alu_op == "1000": 	# shl 
		result = numpy.left_shift(op1,1)
	elif alu_op == "1001": 	# shr 
		result = numpy.right_shift(op1,1)
	elif alu_op == "1010": 	# asr 
		result = numpy.bitwise_or(numpy.bitwise_and(op1, 128), numpy.right_shift(op1,1))
	elif alu_op == "1011": 	# inc 
		result = op1 + 1 
	elif alu_op == "1100": 	# dec
		result = op1 - 1 
	elif alu_op == "1101": 	# rlc
		result = numpy.bitwise_or(128*c_in, numpy.right_shift(op1,1))
	elif alu_op == "1110": 	# rrc 
		result = numpy.bitwise_or(c_in, numpy.left_shift(op1,1))
	elif alu_op == "1111": 	# nop 
		result = 0
	return result 