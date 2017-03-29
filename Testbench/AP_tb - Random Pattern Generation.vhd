-- TestBench Template 

  LIBRARY ieee;
  library std;
  USE ieee.std_logic_1164.ALL;
  USE ieee.numeric_std.ALL;
  USE ieee.std_logic_textio.all; 
  USE ieee.math_real.ALL;
  USE std.textio.ALL;
  USE work.my_package.ALL;

  ENTITY testbench IS
  END testbench;

  ARCHITECTURE behavior OF testbench IS 

  -- Component Declaration
          COMPONENT AP_Alu IS
          PORT(
               clock           : IN std_logic;
               rst             : IN std_logic;
                    OP_A          : IN std_logic_vector(7 downto 0);
                    OP_B          : IN std_logic_vector(7 downto 0);
        RESULT    : OUT std_logic_vector(7 downto 0);
                    ALU_OP        : IN std_logic_vector(3 downto 0)
                  );
          END COMPONENT;

          SIGNAL clock          :  std_logic:= '0';
          SIGNAL rst            :  std_logic := '1';
          SIGNAL OP_A           :  std_logic_vector(7 downto 0) := "00000000";
          SIGNAL OP_B           :  std_logic_vector(7 downto 0) := "00000000";
          SIGNAL RESULT         :  std_logic_vector(7 downto 0) := "00000000";
          SIGNAL ALU_OP         :  std_logic_vector(3 downto 0) := "0000";
          --SIGNAL ALU_OP1        :  std_logic_vector(3 downto 0) := "0000";
  --SIGNAL num_bin1       : std_logic_vector (7 downto 0);
  --SIGNAL num_bin2       : std_logic_vector (7 downto 0);
  --variable num_1        : std_logic_vector (7 downto 0);
  --variable num_2        : std_logic_vector (7 downto 0);
       
        --SIGNAL Header1  : string(1 to 3) := "OPC";
          SIGNAL Header2  : string(1 to 4) := "OP_A";
          SIGNAL Header3  : string(1 to 4) := "OP_B";
          SIGNAL Header4  : string(1 to 6) := "RESULT";
          CONSTANT clk_period : time := 10 ns;
          
-- procedure my_proc is    trying to create procedure for header
--begin
--end procedure my_proc;
  BEGIN

  -- Component Instantiation
          uut: AP_Alu PORT MAP(
                  clock => clock,
                  rst=> rst,
                        OP_A=> OP_A,
                        OP_B=> OP_B,
                        ALU_OP=> ALU_OP,
      RESULT=> RESULT
          );


  --  Test Bench Statements
    --clock <= not clock after 50 ns;
     rst <= '0' after 1 ns;

clk_process:
  process
    begin
        clock <= '0';
        wait for clk_period/2;  --for 0.5 ns signal is '0'.
        clock <= '1';
        wait for clk_period/2;  --for next 0.5 ns signal is '1'.
   end process;
--NOLABEL:
--    process
--    
--    variable Header1 : string(1 to 3) := "OPC";
--    variable seed1 :positive ;  -- seed of value for random generator
--    variable seed2 :positive ;  -- seed of value for random generator
--    variable rand_num : integer;  
--    variable rand_num1 : integer; 
--    variable rand : real ;  -- random real number value in range of 0 to 1
--    variable rand1 : real ;  -- random real number value in range of 0 to 1
--    variable range_of_random : real := 1000.0; -- range of random value to be created
--    
----    begin  
----       uniform (seed1,seed2,rand);    -- generate random number
----       uniform (seed1,seed2,rand1);
----       rand_num := integer (rand * range_of_random);  -- rescale to 0 to 1000 and convert to integer
----       rand_num1 := integer (rand1 * range_of_random);  -- rescale to 0 to 1000 and convert to integer
----       num_bin1 <= std_logic_vector ( to_unsigned (rand_num,8));
----       num_bin2 <= std_logic_vector ( to_unsigned (rand_num1,8));
--       wait for 2 ns;
--      wait;
--   end process;

MONITOR:
    --process (num_bin1, num_bin2) 
  process     
  variable line_v     : line;
  variable line_num     : line;
  file   input_file : text; -- open read_mode is "input.txt";   --declare input file
  file     out_file   : text open write_mode is "sim_generated_file/out.txt";
  variable a, b     : string(1 to 8);
  
  variable char : character:='0';
  variable num_1      : std_logic_vector (7 downto 0); -- num_1 and num_2 are declared as variable 
  variable num_2      : std_logic_vector (7 downto 0);
  variable I : integer range 0 to 4;
  variable count_value : integer := 0;

   
  begin
  --wait for 10 ns;
  while (count_value < 16) loop
  --file     out_file   : text open write_mode is "out.txt";
  file_open(input_file, "sim_input/input.txt", read_mode);
   --while not endfile(input_file) loop
  f: loop 
    readline(input_file, line_num);
    read(line_num, a);
    read(line_num, b);
    for idx in 1 to 8 loop
           char := a(idx);
       if(char = '0') then
                  num_1(8-idx) := '0';
                else
                  num_1(8-idx) := '1';
                  end if;
      end loop;

    for id in 1 to 8 loop
           char := b(id);
       if(char = '0') then
                  num_2(8-id) := '0';
                else
                  num_2(8-id) := '1';
                  end if;
      end loop;
      
       OP_A <= num_1;
     OP_B <= num_2;
    ALU_OP <= std_logic_vector(to_unsigned(count_value, 4));
    wait for 1 ns;
       --OP_A1 := num_1;
       --OP_B1 := num_2;
       
      write(line_v, to_bstring(ALU_OP)& " " & to_bstring(OP_A)& " " & to_bstring(OP_B)& " " & to_bstring(RESULT));
      writeline(out_file, line_v);
    wait for 4 ns;
    --wait;
    exit f when endfile(input_file);
   end loop; -- end inner while loop
write(line_v, string'(""));
   writeline(out_file, line_v);
   wait for 1 ns;
   file_close(input_file);
   
   count_value := count_value + 1;
   --report "The value of count_value is " & integer'image(count_value);
   --wait;
   --wait for 1 ns;

   --file_close(out_file);
  end loop ; -- end outer while loop
    --wait;
     file_close(out_file);
   wait;
   end process;
   
  END;