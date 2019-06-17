commands = {
	"C_ARITHMETIC": ["add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"],
	"C_PUSH": ["push"],
	"C_POP": ["pop"],
	"C_LABEL": ["label"],
	"C_GOTO": ["goto"],
	"C_IF": ["if"],
	"C_FUNCTION": ["function"],
	"C_RETURN": ["return"],
	"C_CALL": ["call"]
}

second_argument = ["argument", "local", "static", "constant", "this", "that", "pointer", "temp"]

class Code:

	
	eq1 = "@R13\nM=-1\n@R14\nM=0"
	eq2 = "\n@SP\nM=M-1\nA=M\nD=M\nA=A-1\nD=D-M\n@EQ\nD;JEQ\n@!EQ\n0;JMP"
	eq3 = "\n(EQ)\n@R13\nD=M\n@END\n0;JMP"
	eq4 = "\n(!EQ)\n@R14\nD=M\n(END)\n@SP\nA=M-1\nM=D"
	eq = eq1 + eq2 + eq3 + eq4
	gt = eq.replace("EQ", "GT")
	lt = eq.replace("EQ", "LT")
	

	arithmetic = {
	"add": "@SP\nM=M-1\nA=M\nD=M\nA=A-1\nM=D+M",
	"sub": "@SP\nM=M-1\nA=M-1\nD=M\nA=A+1\nD=D-M\nA=A-1\nM=D",
	"neg": "@SP\nA=M\nM=-M",
	"eq": eq,
	"gt": gt,
	"lt": lt,
	"and": "@SP\nAM=M-1\nD=M\nA=A-1\nM=D&M",
	"or": "@SP\nAM=M-1\nD=M\nA=A-1\nD=D|M",
	"not": "@SP\nA=M-1\nM=!M"
	}

	push_pop = {
	"push": "@i\nD=A\n@segment\nD=D+M\n@SP\nA=M\nM=D\n@SP\nM=M+1",
	"pop": "@i\nD=A\n@segment\nD=D+M\n@R13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@R13\nA=M\nM=D"
	}

	second_arguments = {
	"argument": "ARG",
	"local": "LCL",
	"static": "static",
	"this": "THIS",
	"that": "THAT",
	"pointer": "3",
	"temp": "5"
	}

