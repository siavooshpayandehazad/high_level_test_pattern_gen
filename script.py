import os
from shutil import copyfile
import matplotlib.pyplot as plt
import re, copy

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

list_of_plots = ["fault coverage", "time taken","number of patterns"]
for plot in list_of_plots:
	index = list_of_plots.index(plot)
	x = []
	y_opt_rfr = []
	y_opt = []
	y_rfr = []
	y = []
	for file in sorted(results_alg.keys()):
		number = re.findall('\d+', file)
		x.append(int(number[0]))
		if "opt_" in file and "rfr_" in file:
			y_opt_rfr.append(float(results_alg[file][index]))
		if "opt_" not in file and "rfr_" in file:
			y_rfr.append(float(results_alg[file][index]))
		if "opt_" in file and "rfr_" not in file:
			y_opt.append(float(results_alg[file][index]))
		if "opt_" not in file and "rfr_" not in file:
			y.append(float(results_alg[file][index]))

	temp_y_opt_rfr = []
	temp_y_rfr = []
	temp_y_opt = []
	temp_y = []
	for item in sorted(x):
		temp_y_opt_rfr.append(y_opt_rfr[x.index(item)])
		temp_y_rfr.append(y_rfr[x.index(item)])
		temp_y_opt.append(y_opt[x.index(item)])
		temp_y.append(y[x.index(item)])

	x = copy.deepcopy(sorted(x))
	y_opt_rfr = copy.deepcopy(temp_y_opt_rfr)
	y_rfr = copy.deepcopy(temp_y_rfr)
	y_opt = copy.deepcopy(temp_y_opt)
	y = copy.deepcopy(temp_y)
	plt.plot(x, y_opt_rfr, ".-r", label="opt, rfr")
	plt.plot(x, y_rfr, "--b",  label="no opt, rfr") 
	plt.plot(x, y_opt, ".-g", label="opt, no rfr") 
	plt.plot(x, y, "--c", label="no opt, no rfr")
	plt.ylabel(plot)
	plt.legend(fontsize = 10, loc='lower right')
	plt.show()

