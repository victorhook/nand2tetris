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

	first = "@SP\nM=M-1\nA=M-1\nD=M\nA=A+1\nD=D-M\n"
	second = "@cond_true_i\nD;condition\nD=0\n@end_i\n0;JMP\n"
	third = "(cond_true_i)\nD=-1\n(end_i)\n@SP\nA=M-1\nM=D"
	eq_gt_lt = first + second + third


	arithmetic = {
	"add": "@SP\nAM=M-1\nD=M\nA=A-1\nM=D+M",
	"sub": "@SP\nM=M-1\nA=M-1\nD=M\nA=A+1\nD=D-M\nA=A-1\nM=D",
	"neg": "@SP\nA=M-1\nM=-M",
	"eq": eq_gt_lt,
	"gt": eq_gt_lt,
	"lt": eq_gt_lt,
	"and": "@SP\nAM=M-1\nD=M\nA=A-1\nM=D&M",
	"or": "@SP\nAM=M-1\nD=M\nA=A-1\nM=D|M",
	"not": "@SP\nA=M-1\nM=!M",
	"comp_counter": 0
	}

	push_pop = {
	"push": "@i\nD=A\n@segment\nA=D+M\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1",
	"pop": "@i\nD=A\n@segment\nD=D+M\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D",
	"constant": "@i\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1"
	}

	second_arguments = {
	"argument": "ARG",
	"local": "LCL",
	"static": "16",
	"this": "THIS",
	"that": "THAT",
	"pointer": "3",
	"temp": "5"
	}

