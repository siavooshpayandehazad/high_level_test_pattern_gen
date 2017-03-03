import os

input_file_path = "patterns/"
file_list = [file for file in os.listdir(input_file_path)]
FC = 0
time = 0
num_of_patterns = 0

results_alg_2 = {}
results_alg_opt = {}

for rfr in [False, True]:
	for file in file_list:
		file_name = file
		command = "python algorithm_2.py"+" -i "+str(input_file_path+file) 
		if rfr:
			command += " -rfr"
			file_name = "rfr_"+file
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
			results_alg_2[file_name] = [FC, time, num_of_patterns]

for rfr in [False, True]:
	
	for file in file_list:
		file_name = file
		command = "python algorithm_opt_greedy.py"+" -i "+str(input_file_path+file)
		if rfr:
			file_name = "rfr_"+file
			command += " -rfr"
		print command
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
			results_alg_opt[file_name] = [FC, time, num_of_patterns]


print "---------------------------"
print "algorithm 2 results:"  
print '%20s' %"file name", "\t", "fault coverage", "\t", '%20s' %"time taken", "\t", '%18s' %"number of patterns", "\t", '%5s' %"rfr "
print '%20s' %"---------", "\t", "--------------", "\t", '%20s' %"----------", "\t", '%18s' %"------------------", "\t", '%5s' %"-----"
for file in sorted(results_alg_2.keys()):
	rfr = False
	file_name = file
	if "rfr_" in file:
		rfr = True
		file_name = file[4:]
	print '%20s' %file_name, "\t", '%14s' %results_alg_2[file][0], "\t", '%20s' %results_alg_2[file][1], "\t",'%18s' %results_alg_2[file][2], "\t",'%5s' %rfr 
print "---------------------------"
print "algorithm opt greedy results:" 
print '%20s' %"file name", "\t", "fault coverage", "\t", '%20s' %"time taken", "\t", '%18s' %"number of patterns",  "\t", '%5s' %"rfr "
print '%20s' %"---------", "\t", "--------------", "\t", '%20s' %"----------", "\t", '%18s' %"------------------", "\t", '%5s' %"-----"
for file in sorted(results_alg_opt.keys()):
	rfr = False
	file_name = file
	if "rfr_" in file:
		rfr = True
		file_name = file[4:]
	print '%20s' %file_name, "\t", '%14s' %results_alg_opt[file][0], "\t", '%20s' %results_alg_opt[file][1], "\t", '%18s' %results_alg_opt[file][2], "\t",'%5s' %rfr 
