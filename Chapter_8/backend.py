command_table = {
	"function": "C_FUNCTION",
	"return": "C_RETURN",
	"call": "C_CALL",
	"push": "C_PUSH",
	"pop": "C_POP",
	"if-goto": "C_IF",
	"goto": "C_GOTO",
	"label": "C_LABEL",
	"add": "C_ARITHMETIC",
	"sub": "C_ARITHMETIC",
	"neg": "C_ARITHMETIC",
	"eq": "C_ARITHMETIC",
	"gt": "C_ARITHMETIC",
	"lt": "C_ARITHMETIC",
	"and": "C_ARITHMETIC",
	"or": "C_ARITHMETIC",
	"not": "C_ARITHMETIC",
}

segment_table = {
	"argument": "ARG",
	"local": "LCL",
	"this": "THIS",
	"that": "THAT",
	"pointer": "pointer",
	"temp": "5",
	"static": "16",
	"constant": "constant"
}

arithmetic_table = {
	"add": "@SP\nAM=M-1\nD=M\nA=A-1\nM=D+M\n",
	"sub": "@SP\nAM=M-1\nD=M\nA=A-1\nM=M-D\n",
	"neg": "@SP\nA=M-1\nM=-M\n",
	"and": "@SP\nAM=M-1\nD=M\nA=A-1\nM=D&M\n",
	"or": "@SP\nAM=M-1\nD=M\nA=A-1\nM=D|M\n",
	"not": "@SP\nA=M-1\nM=!M\n",
}

def comparator(file):
	file_name = file.file_name.split(".vm")[0]
	command = file.current_command[0]
	i = str(file.arithmetic_counter[command])
	file.arithmetic_counter[command] += 1

	if_true = file_name + "." + command + ".true." + i
	end = file_name + "." + command + ".end." + i

	if command == "lt":
		jump = "JLT"
	elif command == "gt":
		jump = "JGT"
	else:
		jump = "JEQ"

	instruction = f"@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\n@{if_true}\nD;{jump}\nD=0\n@{end}\n0;JMP\n"
	instruction += f"({if_true})\nD=-1\n({end})\n@SP\nA=M-1\nM=D\n" 

	return instruction

#	instruction = f"@SP\nAM=M-1\nA=A-1\nD=M\nA=A+1\nD=D-M\n@%s\nD;%s\nD=0\n@%s\n0;JMP\n" % (if_true, jump, end)
#	instruction += f"(%s)\nD=-1\n(%s)\n@SP\nA=M-1\nM=D\n" % (if_true, end)