vlib work

#Include files and compile them
vcom "Test/lib.vhd"
vcom "Test/my_package.vhd"
vcom "Test/AP_Alu.vhd"
vcom "Testbench/AP_tb - Random Pattern Generation.vhd"

# Start simulation
vsim work.testbench 

# Draw waves 

# Run simulation
run 2000000 ns

quit
