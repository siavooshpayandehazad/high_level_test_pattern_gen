library IEEE;
use IEEE.std_logic_1164.all;
--use IEEE.std_logic_arith.all;
--use IEEE.std_logic_unsigned.all;

--------------------------------------------------------------------------------
--!@file: tp_lib.vhd
--!@brief: library of tp
--
--!@author: Tobias Koal(TK)
--!@date: 13-10-02
--------------------------------------------------------------------------------
--! library description of the test processor!
package lib is

	constant WIDTH : natural := 16;

	constant PRG_WIDTH : natural := 104;                  -- Bits im Instruktionswort
	constant OPC_WIDTH : natural := 8;                   -- Bits zur Speicherung des Opcodes
	constant OPR_WIDTH : natural := 6;                   -- Bits zur Speicherung einer Registernummer
	constant OFU_WIDTH : natural := OPC_WIDTH + 3*OPR_WIDTH;
	
	constant SOPC1  : natural := PRG_WIDTH-1;
	constant EOPC1  : natural := PRG_WIDTH-OPC_WIDTH;
	constant SSRC1_1: natural := EOPC1-1;
	constant ESRC1_1: natural := EOPC1-OPR_WIDTH;
	constant SSRC1_2: natural := ESRC1_1-1;
	constant ESRC1_2: natural := ESRC1_1-OPR_WIDTH;
	constant SDST1  : natural := ESRC1_2-1;
	constant EDST1  : natural := ESRC1_2-OPR_WIDTH;
	
	constant SOPC2  : natural := SOPC1  -OFU_WIDTH;
	constant EOPC2  : natural := EOPC1  -OFU_WIDTH;
	constant SSRC2_1: natural := SSRC1_1-OFU_WIDTH;
	constant ESRC2_1: natural := ESRC1_1-OFU_WIDTH;
	constant SSRC2_2: natural := SSRC1_2-OFU_WIDTH;
	constant ESRC2_2: natural := ESRC1_2-OFU_WIDTH;
	constant SDST2  : natural := SDST1  -OFU_WIDTH;
	constant EDST2  : natural := EDST1  -OFU_WIDTH;
	
	constant SOPC3  : natural := SOPC1  -2*OFU_WIDTH;
	constant EOPC3  : natural := EOPC1  -2*OFU_WIDTH;
	constant SSRC3_1: natural := SSRC1_1-2*OFU_WIDTH;
	constant ESRC3_1: natural := ESRC1_1-2*OFU_WIDTH;
	constant SSRC3_2: natural := SSRC1_2-2*OFU_WIDTH;
	constant ESRC3_2: natural := ESRC1_2-2*OFU_WIDTH;
	constant SDST3  : natural := SDST1  -2*OFU_WIDTH;
	constant EDST3  : natural := EDST1  -2*OFU_WIDTH;
	
	constant SOPC4  : natural := SOPC1  -3*OFU_WIDTH;
	constant EOPC4  : natural := EOPC1  -3*OFU_WIDTH;
	constant SSRC4_1: natural := SSRC1_1-3*OFU_WIDTH;
	constant ESRC4_1: natural := ESRC1_1-3*OFU_WIDTH;
	constant SSRC4_2: natural := SSRC1_2-3*OFU_WIDTH;
	constant ESRC4_2: natural := ESRC1_2-3*OFU_WIDTH;
	constant SDST4  : natural := SDST1  -3*OFU_WIDTH;
	constant EDST4  : natural := EDST1  -3*OFU_WIDTH;
	
	
	subtype data_width is std_logic_vector(WIDTH - 1 downto 0);
	subtype prog_addr_width is std_logic_vector(15 downto 0);
	subtype dmem_addr_width is std_logic_vector(15 downto 0);
	subtype instruction_width is std_logic_vector(PRG_WIDTH - 1 downto 0);
	subtype opcode_width is std_logic_vector(OPC_WIDTH - 1 downto 0);
	subtype reg_select is std_logic_vector(OPR_WIDTH - 1 downto 0);
	
	constant ZERO_VECTOR : std_logic_vector(WIDTH - 1 downto 0) := (others => '0');
	constant ONE_VECTOR  : std_logic_vector(WIDTH - 1 downto 0) := (others => '1');
	constant NOP_VECTOR  : instruction_width := (others => '0');

	constant C_ALU : std_logic_vector(3 downto 0) := "1100";
  -- C_ALU & "0000" noch frei
	constant I_CML : opcode_width := C_ALU & "0001";
	constant I_INC : opcode_width := C_ALU & "0010";
	constant I_DEC : opcode_width := C_ALU & "0011";
	constant I_ADD : opcode_width := C_ALU & "0100";
	constant I_ADC : opcode_width := C_ALU & "0101";
	constant I_SUB : opcode_width := C_ALU & "0110";
	constant I_SBB : opcode_width := C_ALU & "0111";	
	constant I_AND : opcode_width := C_ALU & "1000";
	constant I_OR  : opcode_width := C_ALU & "1001";
	constant I_XOR : opcode_width := C_ALU & "1010";
	constant I_CMP : opcode_width := C_ALU & "1011";
	constant I_SHR : opcode_width := C_ALU & "1100";
	constant I_SHL : opcode_width := C_ALU & "1101";
	constant I_RRC : opcode_width := C_ALU & "1110";
	constant I_RLC : opcode_width := C_ALU & "1111";

	constant C_JMP_R : std_logic_vector(3 downto 0) := "0001";
	-- C_JMP_R & "0000" noch frei
	constant I_JZ   : opcode_width := C_JMP_R & "0001";
	constant I_JNZ  : opcode_width := C_JMP_R & "0010";
	constant I_CALL : opcode_width := C_JMP_R & "0011";			
	constant I_JMP  : opcode_width := C_JMP_R & "0100";
	constant I_JMPT : opcode_width := C_JMP_R & "0101";
	constant I_JMPF : opcode_width := C_JMP_R & "0110";
	constant I_JS   : opcode_width := C_JMP_R & "0111";
	constant I_JNS  : opcode_width := C_JMP_R & "1000";
	constant I_JC   : opcode_width := C_JMP_R & "1001";
	-- C_JMP_R & "1010" noch frei
	constant I_JNC  : opcode_width := C_JMP_R & "1011";
	constant I_JO   : opcode_width := C_JMP_R & "1100";
	constant I_JNO  : opcode_width := C_JMP_R & "1101";
	
	constant I_JZ_C   : std_logic_vector(3 downto 0) := "0010";
	constant I_JNZ_C  : std_logic_vector(3 downto 0) := "0011";
	constant I_JS_C   : std_logic_vector(3 downto 0) := "0100";
	constant I_JNS_C  : std_logic_vector(3 downto 0) := "0101";
	constant I_JC_C   : std_logic_vector(3 downto 0) := "0110";
	constant I_JNC_C  : std_logic_vector(3 downto 0) := "0111";
	constant I_JO_C   : std_logic_vector(3 downto 0) := "1000";
	constant I_JNO_C  : std_logic_vector(3 downto 0) := "1001";
	constant I_JMPT_C : std_logic_vector(3 downto 0) := "1010";
	constant I_JMPF_C : std_logic_vector(3 downto 0) := "1011";
	
	constant C_MEM : std_logic_vector(3 downto 0) := "0000";
	constant I_NOP  : opcode_width := C_MEM & "0000";
	constant I_LD0  : opcode_width := C_MEM & "0001";
	constant I_LD1  : opcode_width := C_MEM & "0010";
	constant I_ST0  : opcode_width := C_MEM & "0011";
	constant I_ST1  : opcode_width := C_MEM & "0100";
	
  constant I_CHK_L_0 : opcode_width := C_MEM & "0101";
	constant I_CHK_R_0 : opcode_width := C_MEM & "0110";
	constant I_CHK_R_1 : opcode_width := C_MEM & "1001";
	constant I_CHK_L_1 : opcode_width := C_MEM & "1010";
		
  constant I_HALT    : opcode_width := C_MEM & "0111";
  constant I_LD_FS : opcode_width := C_MEM & "1000";
  
  -- "1101" noch frei
  constant I_JMP_C : std_logic_vector(3 downto 0) := "1110";
  constant I_LDC : std_logic_vector(3 downto 0) := "1111";


  type faulty_rps_register  is array (9 downto 0) of std_logic_vector(63 downto 0);

  
  type fs_regs_select is array(3 downto 0) of std_logic_vector(3 downto 0);
  type fs_bits_select is array(3 downto 0) of std_logic_vector(5 downto 0);


-- AP --
  constant AP_WIDTH : natural := 8;
  constant AP_ADDR_WIDTH : natural := 11;
  subtype AP_data_width is std_logic_vector(AP_WIDTH-1 downto 0);
  subtype AP_mem_addr_width is std_logic_vector(AP_ADDR_WIDTH-1 downto 0);
  subtype AP_instruction_width is std_logic_vector(7 downto 0);
  subtype AP_reg_select is std_logic_vector(1 downto 0);


end package lib;

--! package body of lib
package body lib is

end package body;

