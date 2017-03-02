
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