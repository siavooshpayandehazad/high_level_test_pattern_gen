# high level test pattern gen
welcome! 

---------
The following is the project's folder structure:

* generated_files: exclusively used for storing generated files by algorithm_2.py and algorithm_opt_greedy.py. every time you run the tool, files which are previously stored in this folder would be deleted!
* patterns: input files used by the tool
* script_outputs: exclusively used for storing generated files by script.py. every time you run the tool, files which are previously stored in this folder would be deleted!

* The project basically contains 2 high-level test pattern generation algorithms. (algotithm_2.py and algorithim_opt_greedy.py). 

* The project has two options for execution. You can either execute the algorithms individually with options to see the fault coverage either when redundant faults are included or removed(-rfr removes redundant fault and the default option doesn't). Optionally, you can run script.py which execute the alorithims for every possible patterns in the patterns file. For each execution, the fault coverage, test lenght and time are computed and graphs are generated accordingly
