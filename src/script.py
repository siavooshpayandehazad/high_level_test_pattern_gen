# Copyright (C) 2017 Siavoosh Payandeh Azad, Stephen Oyeniran

import os
from shutil import copyfile
import matplotlib.pyplot as plt
import re, copy

# This script goes through the files in patterns folder and runs them with both 
# algorithms and with and without redundant function reduction!
# The results would be copied to script_outputs folder and comparison graphs would also
# be saved in the same folder!

input_file_path = "../patterns"
generated_files_folder = "../generated_files"
script_folder = "../script_outputs"

tmp_file_list = [tmp_file for tmp_file in os.listdir(input_file_path+"/")]
file_list =[]
for file in tmp_file_list:
	if ".txt" in file:
		file_list.append(file)

print "--------------------------"*3
print "This script runs both algorithms for all the patterns in \"patterns\" folder and saves the results"
print "in \"script_outputs\" folder!"
print "list of files to be processed:", file_list
print "--------------------------"*3

FC = 0
time = 0
num_of_patterns = 0


if os.path.exists(script_folder):
	files = [file for file in os.listdir(script_folder)]
	for file in files:
		os.remove(script_folder+"/"+file)
else:
	os.mkdir(script_folder)

results_alg = {}
for algorithm in ["algorithm_2", "algorithm_opt_greedy"]:
	for rfr in [False, True]:
		for file in file_list:
			
			end_of_file_name = ("_opt" if "opt" in algorithm else "") + ("_rfr" if rfr else "")+"_"+file
			table_file = "table" + end_of_file_name
			pattern_file = "pattern" + end_of_file_name
			ost_file = "ost" + end_of_file_name
			SAF_file = "SAF" + end_of_file_name
			
			command = "python "+algorithm+".py"+" -i "+str(input_file_path+"/"+file) +" -ot "+ table_file+" -op "+ pattern_file+" -ost "+ost_file
			file_name = file
			if "opt" in algorithm:
				file_name = "opt_"+file_name
			if rfr:
				command += " -rfr"
				file_name = "rfr_"+file_name
			os.system(command)

			with open("../generated_files/Console.log") as f:
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
			
			# copying files from generated files folder to script output folder
			#TODO: after fixing SAF for the opt version, this list should be updated!
			for file_to_copy in [table_file, pattern_file, ost_file]: 
				copyfile(generated_files_folder+"/"+file_to_copy, script_folder+"/"+file_to_copy)
	
			if algorithm == "algorithm_2":
				copyfile(generated_files_folder+"/"+"SAFpatterns.txt", script_folder+"/"+SAF_file)

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

	# the data in the lists should be sorted first!
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

	# plotting the data!
	plt.plot(x, y_opt_rfr, ".-r", label="opt, rfr")
	plt.plot(x, y_rfr, "--b",  label="no opt, rfr") 
	plt.plot(x, y_opt, ".-g", label="opt, no rfr") 
	plt.plot(x, y, "--c", label="no opt, no rfr")

	# here we mark the maximum values of each 
	plt.plot((0, x[y_opt_rfr.index(max(y_opt_rfr))]), (max(y_opt_rfr), max(y_opt_rfr)), 'y--')
	plt.plot((0, x[y_rfr.index(max(y_rfr))]), (max(y_rfr), max(y_rfr)), 'y--')
	plt.plot((0, x[y_opt.index(max(y_opt))]), (max(y_opt), max(y_opt)), 'y--')
	plt.plot((0, x[y.index(max(y))]), (max(y), max(y)), 'y--')

	# adding lables!
	plt.xlabel("Search Space(number of initial patterns)")
	if plot == "time taken":
		plt.ylabel(plot+"(s)")
	else:
		plt.ylabel(plot)

	# adding legend!
	if plot == "time taken":
		plt.legend(fontsize = 10, loc='upper left')
	else:
		plt.legend(fontsize = 10, loc='lower right')

	figure_name = script_folder+"/"
	split_plot_name = plot.split()
	for j in split_plot_name:
		if split_plot_name.index(j)!= len(split_plot_name)-1:
			figure_name += j + "_"
		else:
			figure_name += j +".jpg"
	plt.savefig(figure_name)
	plt.close()
