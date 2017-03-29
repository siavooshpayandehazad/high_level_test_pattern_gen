LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.STD_LOGIC_ARITH.ALL;
USE IEEE.STD_LOGIC_UNSIGNED.ALL;
USE WORK.LIB.ALL;

ENTITY AP_Alu IS
  PORT(
    clock         : IN std_logic;
    rst           : IN std_logic;    
		OP_A          : IN AP_data_width;
		OP_B          : IN AP_data_width;
		ALU_OP        : IN std_logic_vector(3 downto 0);
		
		RESULT        : OUT AP_data_width;
		carry_out     : OUT std_logic;
		zero_out      : OUT std_logic;
		sign_out      : OUT std_logic;
		overflow_out  : OUT std_logic
  );
END AP_Alu;

ARCHITECTURE behave OF AP_Alu IS
  signal carry, zero, sign, overflow : std_logic;
  signal carry_new, zero_new, sign_new, overflow_new : std_logic;
  
BEGIN
  
  alu_process : process(OP_A, OP_B, ALU_OP)
    variable RESULT_INTERN : AP_data_width;
    variable RESULT_TEMP : std_logic_vector(AP_WIDTH downto 0);
  begin
    RESULT_INTERN := (others => '0');
    carry_new <= carry;
    zero_new <= zero;
    sign_new <= sign;
    overflow_new <= overflow;
    
    case ALU_OP is
      when "0000" => -- mov
        RESULT_INTERN := OP_B;
      when "0001" => -- add
        RESULT_TEMP := ('0' & OP_A) + OP_B;
        carry_new <= RESULT_TEMP(AP_WIDTH);
        sign_new <= RESULT_TEMP(AP_WIDTH-1);
        overflow_new <= (not(OP_A(AP_WIDTH-1) XOR OP_B(AP_WIDTH-1))) 
                AND (OP_A(AP_WIDTH-1) XOR RESULT_TEMP(AP_WIDTH-1));  
        
        if RESULT_TEMP(AP_WIDTH - 1 downto 0) = "00000000" then
			    zero_new <= '1';
		    else
			    zero_new <= '0'; 
		    end if;
        
        RESULT_INTERN := RESULT_TEMP(AP_WIDTH-1 downto 0);
      when "0010" | "0011" => -- sub, cmp
        RESULT_TEMP := ('0' & OP_A) - OP_B; 
        carry_new <= RESULT_TEMP(AP_WIDTH);
        sign_new <= RESULT_TEMP(AP_WIDTH-1);
        overflow_new <= (OP_A(AP_WIDTH-1) XOR OP_B(AP_WIDTH-1)) 
                AND (OP_A(AP_WIDTH-1) XOR RESULT_TEMP(AP_WIDTH-1));
        
        if RESULT_TEMP(AP_WIDTH - 1 downto 0) = "00000000" then
			    zero_new <= '1';
		    else
			    zero_new <= '0';
		    end if;
		    
		    if ALU_OP = "0010" then
		      RESULT_INTERN := RESULT_TEMP(AP_WIDTH-1 downto 0);
		    else
		      RESULT_INTERN := OP_A; -- bei Alu-Ops ist RF_en immer gesetzt
		    end if;
      when "0100" => -- and
        RESULT_INTERN := OP_A AND OP_B;
      when "0101" => -- or
        RESULT_INTERN := OP_A OR OP_B;
      when "0110" => -- xor
        RESULT_INTERN := OP_A XOR OP_B;
      when "0111" => -- not
        RESULT_INTERN := NOT OP_B;
      when "1000" => -- shl
        RESULT_INTERN := OP_A(AP_WIDTH-2 downto 0) & carry;
        carry_new <= OP_A(AP_WIDTH-1);
      when "1001" => -- shr
        RESULT_INTERN := carry & OP_A(AP_WIDTH-1 downto 1);
        carry_new <= OP_A(0);
      when "1010" => -- asr
        RESULT_INTERN := OP_A(AP_WIDTH-1) & OP_A(AP_WIDTH-1 downto 1);
        carry_new <= OP_A(0);
      when "1011" => -- inc
        RESULT_TEMP := ('0' & OP_A) + 1;
        carry_new <= RESULT_TEMP(AP_WIDTH);
        sign_new <= RESULT_TEMP(AP_WIDTH-1);
        overflow_new <= (not(OP_A(AP_WIDTH-1) XOR OP_B(AP_WIDTH-1))) 
                AND (OP_A(AP_WIDTH-1) XOR RESULT_TEMP(AP_WIDTH-1));  
        
        if RESULT_TEMP(AP_WIDTH - 1 downto 0) = "00000000" then
			    zero_new <= '1';
		    else
			    zero_new <= '0';
		    end if;
        
        RESULT_INTERN := RESULT_TEMP(AP_WIDTH-1 downto 0);        
      when "1100" => -- dec   
        RESULT_TEMP := ('0' & OP_A) - 1; 
        carry_new <= RESULT_TEMP(AP_WIDTH);
        sign_new <= RESULT_TEMP(AP_WIDTH-1);
        overflow_new <= (OP_A(AP_WIDTH-1) XOR OP_B(AP_WIDTH-1)) 
                AND (OP_A(AP_WIDTH-1) XOR RESULT_TEMP(AP_WIDTH-1));
        
        if RESULT_TEMP(AP_WIDTH - 1 downto 0) = "00000000" then
			    zero_new <= '1';
		    else
			    zero_new <= '0';
		    end if;
		    
		    RESULT_INTERN := RESULT_TEMP(AP_WIDTH-1 downto 0);      
      when "1101" => 
        carry_new <= '1';
        RESULT_INTERN := OP_A;  
      when "1110" => 
        carry_new <= '0';
        RESULT_INTERN := OP_A;
     -- when "1111" =>
      
      when others =>
        
    end case;
    RESULT <= RESULT_INTERN;
  end process;
  
  flag_process : process(clock, rst)
  begin
    if (rst = '1') then
      carry <= '0';
      zero <= '0';
      sign <= '0';
      overflow <= '0';
    elsif (clock'event and clock = '1') then
      carry <= carry_new;
      zero <= zero_new;
      sign <= sign_new;
      overflow <= overflow_new;
    end if;
  end process;
  
  carry_out <= carry;
  zero_out <= zero;
  sign_out <= sign;
  overflow_out <= overflow;
  
  
END behave;  