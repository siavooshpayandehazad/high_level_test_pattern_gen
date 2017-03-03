import os

input_file_path = "patterns/"
file_list = [file for file in os.listdir(input_file_path)]

results_alg_2 = {}
for file in file_list:
	command = "python algorithm_2.py"+" -i "+str(input_file_path+file) 
	os.system(command)

	with open("Console.log") as f:
		for line in f:
			if line != "":
				if "fault coverage " in line and "%" in line:
					FC =  line.split()[3]
				if "seconds" in line:
					time = line.split()[2]
				if "number of patterns used:" in line:
					num_of_patterns = line.split()[4]
		results_alg_2[file] = [FC, time, num_of_patterns]



results_alg_opt = {}
for file in file_list:
	command = "python algorithm_opt_greedy.py"+" -i "+str(input_file_path+file) 
	os.system(command)

	with open("Console.log") as f:
		for line in f:
			if line != "":
				if "fault coverage " in line and "%" in line:
					FC =  line.split()[3]
				if "seconds" in line:
					time = line.split()[2]
				if "number of patterns used:" in line:
					num_of_patterns = line.split()[4]
		results_alg_opt[file] = [FC, time, num_of_patterns]

print "---------------------------"
print "algorithm 2 results"
print '%20s' %"file name", "\t", "fault coverage", "\t", '%20s' %"time taken", "\t", '%18s' %"number of patterns"
print '%20s' %"---------", "\t", "--------------", "\t", '%20s' %"----------", "\t", '%18s' %"------------------"
for file in sorted(results_alg_2.keys()):
	print '%20s' %file, "\t", '%14s' %results_alg_2[file][0], "\t", '%20s' %results_alg_2[file][1], "\t",'%18s' %results_alg_2[file][2]
print "---------------------------"
print "algorithm opt greedy results"
print '%20s' %"file name", "\t", "fault coverage", "\t", '%20s' %"time taken", "\t", '%18s' %"number of patterns"
print '%20s' %"---------", "\t", "--------------", "\t", '%20s' %"----------", "\t", '%18s' %"------------------"
for file in sorted(results_alg_opt.keys()):
	print '%20s' %file, "\t", '%14s' %results_alg_opt[file][0], "\t", '%20s' %results_alg_opt[file][1], "\t", '%18s' %results_alg_2[file][2]