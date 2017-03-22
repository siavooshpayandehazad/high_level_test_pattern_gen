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