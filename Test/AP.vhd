LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.STD_LOGIC_UNSIGNED.ALL;
USE IEEE.STD_LOGIC_ARITH.ALL;
USE WORK.LIB.ALL;

ENTITY AP IS
  PORT(
    clock      : IN std_logic;
    rst        : IN std_logic;
    
    -- AP Memory/Arbiter
    MemDataIn  : IN AP_data_width;
    MemDataOut: OUT AP_data_width;
    MemAddr    : OUT AP_mem_addr_width;
    wrMem      : OUT std_logic;
    startArb   : OUT std_logic;
    arbMode    : OUT std_logic;
    arbReady   : IN  std_logic;
    
    
    -- Fault State Memory
    FSdataIn  : IN AP_data_width;
    FSdataOut : OUT AP_data_width;
    FSwrite   : OUT std_logic;
    FSaddr    : OUT std_logic_vector (6 downto 0);
    SlotNr    : OUT std_logic_vector (1 downto 0);
    slot      : IN std_logic;
    lRP       : IN std_logic;
    rRP       : IN std_logic;
    resetFS   : OUT std_logic;
    
    -- PuT
    PuTHalt          : IN std_logic;
		PuTContinue      : OUT std_logic;
		PuTReset         : OUT std_logic
       
  );
END AP;

ARCHITECTURE behave OF AP IS

-- COMPONENTS ---------
  COMPONENT AP_regFile IS
  PORT(
    clock      : IN std_logic;
    rst        : IN std_logic;
    enable     : IN std_logic;
    wrAddr     : IN AP_reg_select;
    wrData    	: IN AP_data_width;
   	rp1Addr    : IN AP_reg_select;
	  rp2Addr  	 : IN AP_reg_select;
	  rp1Data    : OUT AP_data_width;
	  rp2Data    : OUT AP_data_width
	         
  );
  END COMPONENT;
  
  COMPONENT AP_reg_generic IS
  GENERIC (reg_width  : natural := 8);
  PORT(
    clock      : IN std_logic;
    rst        : IN std_logic;
    enable     : IN std_logic;
    input      : IN std_logic_vector (reg_width-1 downto 0);
    output     : OUT std_logic_vector (reg_width-1 downto 0)  
  );
  END COMPONENT;
  
  COMPONENT AP_Alu IS
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
END COMPONENT;
  
-- SIGNALS ------------ 
  signal RF_wrAddr, RF_Addr1, RF_Addr2 : AP_reg_select;
  signal RF_en, IR_en, FSaddr_en, SlotNr_en, MBR_en, MAR_H_en, MAR_L_en, PC_en, rstTimer, incTimer  : std_logic;
  signal carry, overflow, sign, zero : std_logic;
  signal RF_in, RF_out1, RF_out2, IR_out, Alu_in1, Alu_in2, Alu_out : AP_data_width;
  signal MAR_L_out, MAR_L_in, MBR_out, MBR_in : AP_data_width;
  signal MAR_H_out, MAR_H_in : std_logic_vector(AP_ADDR_WIDTH - AP_WIDTH - 1 downto 0);
  signal Alu_opc : std_logic_vector(3 downto 0);
  signal timer : std_logic_vector(3 downto 0);
  signal FSaddr_in : std_logic_vector(6 downto 0);
  signal SlotNr_in, SlotNr_out : std_logic_vector(1 downto 0);
  signal PC_out, PC_in : AP_mem_addr_width;
  signal instCh_in, instCh_out : std_logic_vector(0 downto 0);
  signal instCh_en : std_logic;
  
BEGIN 
  SlotNr <= SlotNr_out;


  control: process(IR_out, timer, PC_out, RF_out1, RF_out2, Alu_out, 
                    MemDataIN, MBR_out, MAR_L_out, MAR_H_out, FSdataIn, 
                    arbReady, carry, zero, sign, overflow, PuTHalt, SlotNr_out)
    variable jmpCond : std_logic := '0';
  begin
    -- default-values
    IR_en <= '0';
    PC_en <= '0';
    RF_en <= '0';
    MBR_en <= '0';
    MAR_H_en <= '0';
    MAR_L_en <= '0';
    FSaddr_en <= '0';
    FSwrite <= '0';
    wrMem <= '0';
    rstTimer <= '0';
    startArb <= '0';
    arbMode <= '0';
    incTimer <= '1';
    PuTContinue <= '0';
    PuTReset <= '0';
    SlotNr_en <= '0';
    instCh_en <= '0';
    resetFS <= '0';
        
    
    PC_in <= PC_out;
    MemAddr <= PC_out;
    Alu_opc <= (others => '0');
    RF_Addr1 <= IR_out(3 downto 2);
    RF_Addr2 <= IR_out(1 downto 0);
    RF_wrAddr <= IR_out(3 downto 2);
    Alu_in1 <= RF_out1;
    Alu_in2 <= RF_out2;
    RF_in <= Alu_out;
    MBR_in <= MemDataIN;
    MAR_H_in <= RF_out1(AP_ADDR_WIDTH - AP_WIDTH - 1 downto 0);
    MAR_L_in <= RF_out1;    
    MemDataOut <= MBR_out;
    FSaddr_in <= RF_out1(6 downto 0);
    FSdataOut <= RF_out1;
    SlotNr_in <= Alu_out(1 downto 0);
    instCh_in <= IR_out(0 downto 0); 
    
    if(timer = "0000") then
    -- fetch
      MemAddr <= PC_out;
      IR_en <= '1';
      PC_en <= '1';
      PC_in <= PC_out + 1;
    else
      if(IR_out(7) = '0') then
      -- AluOp with 2 Operands
        Alu_opc <= IR_out(7 downto 4);
        RF_Addr1 <= IR_out(3 downto 2);
        RF_Addr2 <= IR_out(1 downto 0);
        RF_wrAddr <= IR_out(3 downto 2);
        Alu_in1 <= RF_out1;
        Alu_in2 <= RF_out2;
        RF_in <= Alu_out;
        RF_en <= '1';
        rstTimer <= '1';
    
      elsif(IR_out(7 downto 5) = "101") then
      -- AluOp with 1 Operand
        Alu_opc <= IR_out(5 downto 2);
        RF_Addr1 <= IR_out(1 downto 0);
        RF_wrAddr <= IR_out(1 downto 0);
        Alu_in1 <= RF_out1;
        RF_in <= Alu_out;
        RF_en <= '1';
        rstTimer <= '1';
      elsif(IR_out(7 downto 5) /= "111") then
      -- Ops with 1 Operand
        RF_Addr1 <= IR_out(1 downto 0);
        RF_wrAddr <= IR_out(1 downto 0);
        case IR_out(7 downto 2) is
          
          when "100000" =>
          -- load
            if(timer = "0001") then
              MemAddr <= MAR_H_out & MAR_L_out;
              MBR_en <= '1';
              MBR_in <= MemDataIN;
            elsif(timer = "0010") then
              RF_in <= MBR_out;
              RF_en <= '1';
              rstTimer <= '1';
            end if;
          
          when "100001" =>
          -- store
            if(timer = "0001") then
              MBR_in <= RF_out1;
              MBR_en <= '1';
            elsif(timer = "0010") then           
              wrMem <= '1';           
              MemAddr <= MAR_H_out & MAR_L_out;
              rstTimer <= '1';
            end if;
          
          when "100010" =>
          -- ldc
            if(timer = "0001") then
              PC_en <= '1';
              PC_in <= PC_out + 1;
              MBR_in <= MemDataIN;
              MBR_en <= '1';
            elsif(timer = "0010") then
              RF_in <= MBR_out;
              RF_en <= '1';
              rstTimer <= '1';            
            end if; 
            
          when "100011" =>
          -- setMarL 
            MAR_L_in <= RF_out1;
            MAR_L_en <= '1';
            rstTimer <= '1';        
          when "100100" =>
          -- setMarH
            MAR_H_in <= RF_out1(AP_ADDR_WIDTH - AP_WIDTH - 1 downto 0); 
            MAR_H_en <= '1';
            rstTimer <= '1';          
          when "100101" | "100110" =>
          -- incMar | decMar  
            if(timer = "0001") then
              Alu_in1 <= MAR_L_out;
              Alu_in2 <= "000000" & IR_out(1 downto 0);
              if(IR_out(7 downto 2) = "100101") then
                 Alu_opc <= "0001"; -- add
              else
                 Alu_opc <= "0010"; -- sub
              end if;
              MAR_L_in <= Alu_out;
              MAR_L_en <= '1';             
            elsif(timer = "0010") then
              if(carry = '1') then
                Alu_in1(AP_WIDTH - 1 downto AP_ADDR_WIDTH - AP_WIDTH) <= (others => '0');
                Alu_in1(AP_ADDR_WIDTH - AP_WIDTH - 1 downto 0) <= MAR_H_out;                
                if(IR_out(7 downto 2) = "100101") then
                  Alu_opc <= "1011"; -- inc
                else
                  Alu_opc <= "1100"; -- dec
                end if;
                MAR_H_in <= Alu_out(AP_ADDR_WIDTH - AP_WIDTH - 1 downto 0);
                MAR_H_en <= '1';
              end if;             
              rstTimer <= '1';            
            end if;
          
          when "110000" =>
          -- setFSaddr
            FSaddr_en <= '1';
            FSaddr_in <= RF_out1(6 downto 0);
            rstTimer <= '1';
          when "110001" =>
          -- readFS
            RF_in <= FSdataIn;
            RF_en <= '1';
            rstTimer <= '1';  
          when "110010" =>
          -- writeFS
            FSdataOut <= RF_out1;
            FSwrite <= '1';
            rstTimer <= '1';                 
          when others =>
            rstTimer <= '1'; 
        end case;  
      elsif(IR_out(7 downto 5) = "111") then
      -- no Operands
        if(IR_out(4) = '0') then
          -- jumps 
            if(timer = "0001") then
             
              case IR_out(4 downto 0) is
                when "00000" =>
                  jmpCond := '1';
                when "00001" =>
                  jmpCond := carry;
                when "00010" =>
                  jmpCond := not carry;
                when "00011" =>
                  jmpCond := sign;
                when "00100" =>
                  jmpCond := not sign;
                when "00101" =>
                  jmpCond := overflow;
                when "00110" =>
                  jmpCond := not overflow;
                when "00111" =>
                  jmpCond := zero;
                when "01000" =>
                  jmpCond := not zero;
                  
                when "01001" => 
                  jmpCond := slot;
                when "01010" =>
                  if(SlotNr_out = "11") then
                    jmpCond := '0';
                  else 
                    jmpCond := '1';   
                  end if;
                when "01011" =>
                  jmpCond := not lRP;
                when "01100" =>
                  jmpCond := not rRP;                                                                                         
                when "01111" =>
                  jmpCond := not PuTHalt;
                when others =>
                  jmpCond := '0';
                end case; 
              
              PC_en <= '1';
              PC_in <= PC_out + 1; 
                  
              if(jmpCond = '1') then   
                MBR_in <= MemDataIN;
                MBR_en <= '1';
              end if;  
                                               
            elsif(timer = "0010") then
              if(jmpCond = '0') then
                PC_en <= '1';
                PC_in <= PC_out + 1;
                rstTimer <= '1';
              else
                PC_in(AP_ADDR_WIDTH-1 downto AP_WIDTH) 
                      <= MBR_out(AP_ADDR_WIDTH - AP_WIDTH - 1 downto 0);  
                PC_en <= '1';
                
                MBR_in <= MemDataIN;
                MBR_en <= '1';
              end if;
            elsif(timer = "0011") then
                PC_in(AP_WIDTH-1 downto 0) <= MBR_out;            
                PC_en <= '1';
                MemAddr <= MAR_H_out & MAR_L_out; -- im PC könnte in diesem Takt eine zu hohe Adresse stehen (falls der adressierbare Bereich größer ist als der Speicher) 
                rstTimer <= '1'; 
            end if;
        else -- IR_out(4) /= '0'  -> no Operand, no jump
          case IR_out(4 downto 0) is      
            when "10000" | "10001" =>
            -- fetchInstr | storeInstr.
              
              arbMode <= IR_out(0);
              incTimer <= '0';
              if(timer = "0001") then
                MemAddr <= MAR_H_out & MAR_L_out; 
                startArb <=  not IR_out(0) or instCh_out(0);   
                incTimer <= '1';
              elsif(arbReady = '1') then
                rstTimer <= '1';
              end if;
              
            when "10010" =>
            -- continuePuT
              PuTContinue <= '1';
              rstTimer <= '1';
            when "10011" =>
            -- resetPuT
              PuTReset <= '1';
              rstTimer <= '1';
              
            when "10100" =>
            -- resetFS
              resetFS <= '1';
              rstTimer <= '1';              
              
            when "10101" =>
            -- setMar
              if(timer = "0001") then
                MBR_in <= MemDataIN;
                MBR_en <= '1';
                
                PC_en <= '1';
                PC_in <= PC_out + 1;
              elsif(timer = "0010") then 
                MAR_H_in <= MBR_out(AP_ADDR_WIDTH - AP_WIDTH - 1 downto 0);
                MAR_H_en <= '1';
                
                MBR_in <= MemDataIN;
                MBR_en <= '1';
                
                PC_en <= '1';
                PC_in <= PC_out + 1;
              elsif(timer = "0011") then
                MAR_L_in <= MBR_out;
                MAR_L_en <= '1'; 
                rstTimer <= '1'; 
              end if;             
                        
            when "11000" | "11001" =>
            -- rstInstChanged | setInstChanged  
               instCh_in <= IR_out(0 downto 0);
               instCh_en <= '1';
               rstTimer <= '1';  
               
            when "11010" =>
            -- rstSlotNr  
              SlotNr_in <= "00";
              SlotNr_en <= '1';    
              rstTimer <= '1';
              
            when "11011" | "11100" =>
            -- incSlotNr | decSlotNr
              Alu_in1 <= "000000" & SlotNr_out;
              Alu_opc <= IR_out(3 downto 0);
              SlotNr_in <= Alu_out(1 downto 0);
              SlotNr_en <= '1';
              rstTimer <= '1';
                          
            when others =>
              rstTimer <= '1'; 
          end case;
        end if;
      
              
      end if;
    end if;
  end process;
  
  timer_process: process(clock, rst)
  begin
    if (rst = '1') then
      timer <= (others => '0');
    elsif (clock'event and clock = '1') then
      if(rstTimer = '1') then
        timer <= (others => '0');
      elsif(incTimer = '1') then
        timer <= timer + 1;
      end if;
    end if;   
  end process;
   
  PC: AP_reg_generic
  GENERIC MAP (reg_width => AP_ADDR_WIDTH)
  PORT MAP (
    clock => clock,
    rst => rst,
    enable => PC_en,
    input => PC_in,
    output => PC_out
    
  ); 
  
  IR: AP_reg_generic
  GENERIC MAP (reg_width => AP_WIDTH)
  PORT MAP (
    clock => clock,
    rst => rst,
    enable => IR_en,
    input => MemDataIN,
    output => IR_out
    
  );
  
  MBR: AP_reg_generic
  GENERIC MAP (reg_width => AP_WIDTH)
  PORT MAP (
    clock => clock,
    rst => rst,
    enable => MBR_en,
    input => MBR_in,
    output => MBR_out
    
  ); 
  
  MAR_H: AP_reg_generic
  GENERIC MAP (reg_width => AP_ADDR_WIDTH - AP_WIDTH)
  PORT MAP (
    clock => clock,
    rst => rst,
    enable => MAR_H_en,
    input => MAR_H_in,
    output => MAR_H_out
    
  ); 
  
  MAR_L: AP_reg_generic
  GENERIC MAP (reg_width => AP_WIDTH)
  PORT MAP (
    clock => clock,
    rst => rst,
    enable => MAR_L_en,
    input => MAR_L_in,
    output => MAR_L_out
    
  ); 
  
  FS_addr: AP_reg_generic
  GENERIC MAP (reg_width => 7)
  PORT MAP (
    clock => clock,
    rst => rst,
    enable => FSaddr_en,
    input => FSaddr_in,
    output => FSaddr
    
  );
  
  SlotNr_reg: AP_reg_generic
  GENERIC MAP (reg_width => 2)
  PORT MAP (
    clock => clock,
    rst => rst,
    enable => SlotNr_en,
    input => SlotNr_in,
    output => SlotNr_out
    
  );
  
  regFile: AP_regFile
  PORT MAP (
    clock => clock,
    rst => rst,
    enable => RF_en,
    wrAddr => RF_wrAddr,
    wrData => RF_in,
    rp1Addr => RF_Addr1,
    rp2Addr => RF_Addr2,
    rp1Data => RF_out1,
    rp2Data => RF_out2
    
  );
  
  ALU: AP_Alu
  PORT MAP (
    clock => clock,
    rst => rst,
    OP_A => Alu_in1,
    OP_B => Alu_in2,
    ALU_OP => Alu_opc,    
    RESULT  => Alu_out,
    carry_out => carry,
    zero_out => zero,
    sign_out => sign,
    overflow_out => overflow
    
  );
      
  InstChanged: AP_reg_generic
  GENERIC MAP (reg_width => 1)
  PORT MAP (
    clock => clock,
    rst => rst,
    enable => instCh_en,
    input => instCh_in,
    output => instCh_out
    
  );
  
END behave;