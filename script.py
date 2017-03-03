import os
from shutil import copyfile

input_file_path = "patterns/"
file_list = [file for file in os.listdir(input_file_path)]
FC = 0
time = 0
num_of_patterns = 0

script_folder = "script_outputs/"
if os.path.exists(script_folder):
	files = [file for file in os.listdir(script_folder)]
	for file in files:
		os.remove(script_folder+file)
else:
	os.mkdir(script_folder)



results_alg = {}
for algorithm in ["algorithm_2", "algorithm_opt_greedy"]:
	for rfr in [False, True]:
		for file in file_list:
			

			table_file = "table"+("_opt" if "opt" in algorithm else "")+ ("_rfr" if rfr else "")+"_"+file
			pattern_file = "pattern"+("_opt" if "opt" in algorithm else "")+ ("_rfr" if rfr else "")+"_"+file
			ost_file = "ost"+("_opt" if "opt" in algorithm else "")+ ("_rfr" if rfr else "")+"_"+file
			
			command = "python "+algorithm+".py"+" -i "+str(input_file_path+file) +" -ot "+ table_file+" -op "+ pattern_file+" -ost "+ost_file
			file_name = file
			if "opt" in algorithm:
				file_name = "opt_"+file_name
			if rfr:
				command += " -rfr"
				file_name = "rfr_"+file_name
			os.system(command)
			with open("Console.log") as f:
				FC = 0
				time = 0
				num_of_patterns = 0
				for line in f:
					if line != "":
						if "fault coverage " in line and "%" in line:
							FC =  line.split()[3]
						if "seconds" in line:
							time = line.split()[2]
						if "number of patterns used:" in line:
							num_of_patterns = line.split()[4]
				results_alg[file_name] = [FC, time, num_of_patterns]
				
			copyfile("generated_files/"+table_file, script_folder+table_file)
			copyfile("generated_files/"+pattern_file, script_folder+pattern_file)
			copyfile("generated_files/"+ost_file, script_folder+ost_file)


print "---------------------------"
print "algorithms results:"  
print '%20s' %"file name", "\t", "fault coverage", "\t", '%20s' %"time taken", "\t", '%18s' %"number of patterns", "\t", '%5s' %"rfr ",  "\t", '%5s' %"opt "
print '%20s' %"---------", "\t", "--------------", "\t", '%20s' %"----------", "\t", '%18s' %"------------------", "\t", '%5s' %"-----", "\t", '%5s' %"-----"
for file in sorted(results_alg.keys()):
	rfr = False
	opt = False
	file_name = file
	pointer = 0
	if "opt_" in file:
		opt = True
		pointer += 4
	if "rfr_" in file:
		rfr = True
		pointer += 4
	file_name = file[pointer:]

	print '%20s' %file_name, "\t", '%14s' %results_alg[file][0], "\t", '%20s' %results_alg[file][1], "\t",'%18s' %results_alg[file][2], "\t",'%5s' %rfr , "\t",'%5s' %opt 
