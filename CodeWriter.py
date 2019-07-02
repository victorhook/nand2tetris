from backend import segment_table, comparator, arithmetic_table
from File import File

class CodeWriter:

	return_counter = 0

	def push(number, segment):

		instruction = "@%s\nD=A\n@%s\nA=D+M\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n" % (number, segment)

		if number == 0:
			instruction = "@%s\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n" % segment

		if segment == "constant":
			instruction = "@%s\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n" % number

		if segment == "pointer":
			instruction = "@%s\nD=A\n@%s\nA=D+A\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n" % ("THIS", number)

		if segment == "THAT":
			instruction = "@THAT\nD=M\n@%s\nA=D+A\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n" % number

		if segment == "write_func":
			instruction = "@%s\nD=A\n@SP\nA=M\nM=0\n@SP\nM=M+1\n" % number

		if segment == "call_func":
			instruction = "@%s\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n" % number

		return instruction

	def pop(number, segment):

		instruction = "@%s\nD=A\n@%s\nD=D+M\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n" % (number, segment)

		if segment == "3" or segment == "5":
			instruction = instruction.replace("D=D+M", "D=D+A") 

		if segment == "THIS" or segment == "THAT":
			instruction = "@%s\nD=M\n@%s\nD=D+A\n@R13\nM=D\n@SP\nA=M-1\nD=M\n@R13\nA=M\nM=D\n@SP\nM=M-1\n" % (segment, number)

		if segment == "pointer":
			instruction = "@%s\nD=A\n@R3\nD=D+A\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n" % number


		return instruction


	def write_push(file):

		if file.current_command[1] == "static":
			i = file.current_command[2]
			segment = file.statics[int(i)]
			instruction = "@%s\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n" % segment

		else:
			segment = segment_table[file.current_command[1]]
			number = file.current_command[2]
			instruction = CodeWriter.push(number, segment)

		return instruction

	def write_pop(file):

		if file.current_command[1] == "static":
			i = file.current_command[2]
			static_name = file.last_function.split(".")[0] + "." + i
			
			if static_name in file.statics:
				segment = static_name
			else:
				segment = static_name
				file.statics.append(static_name)
				file.static_counter += 1

			instruction = "@%s\nD=A\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n" % segment
		

		else:
			segment = segment_table[file.current_command[1]]
			number = file.current_command[2]
			instruction = CodeWriter.pop(number, segment)

		return instruction


	def write_function(file):
		func_name = file.current_command[1]
		nargs = file.current_command[2]
		instruction = "(%s)\n" % func_name		

		for arg in range(int(nargs)):
			instruction += CodeWriter.push(arg, "write_func")

		return instruction

	def write_call(file):		
		nargs = int(file.current_command[2])
		function = file.current_command[1]

		return_label = function.split(".")[0] + "$ret." + str(CodeWriter.return_counter)
		CodeWriter.return_counter += 1
		instruction = "@%s\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n" % return_label	# push ret addr
		instruction += CodeWriter.push("LCL", "call_func")
		instruction += CodeWriter.push("ARG", "call_func")
		instruction += CodeWriter.push("THIS", "call_func")
		instruction += CodeWriter.push("THAT", "call_func")

		nargs += 5
		set_arg = "@SP\nD=M\n@%s\nD=D-A\n@ARG\nM=D\n" % nargs

		instruction += set_arg
		instruction += "@SP\nD=M\n@LCL\nM=D\n"
		instruction += "@%s\n0;JMP\n" % function
		instruction += "(%s)\n" % return_label
		return instruction

	def write_return(file):
		frame = "R13"
		ret = "R14"

		instruction = "@LCL\nD=M\n@%s\nM=D\n" % frame 							# FRAME = LCL
		instruction += "@%s\nD=M\n@5\nA=D-A\nD=M\n@%s\nM=D\n" % (frame, ret)	# return addresss in temp var
		instruction += "@SP\nAM=M-1\nD=M\n@ARG\nA=M\nM=D\n"						# *ARG = pop()
		instruction += "@ARG\nD=M+1\n@SP\nM=D\n"								# SP = ARG*
		instruction += "@%s\nD=M\nA=D-1\nD=M\n@THAT\nM=D\n" % frame				# THAT = *(Frame - 1)
		instruction += "@%s\nD=M\n@2\nA=D-A\nD=M\n@THIS\nM=D\n"	% frame 		# THIS = *(Frame - 2)
		instruction += "@%s\nD=M\n@3\nA=D-A\nD=M\n@ARG\nM=D\n" % frame 			# ARG = *(Frame - 3)
		instruction += "@%s\nD=M\n@4\nA=D-A\nD=M\n@LCL\nM=D\n" % frame 			# LCL = *(Frame - 4)
		instruction += "@%s\nA=M\n0;JMP\n" % ret 								# goto ret

		return instruction
		
	def write_label(file):
		if file.last_function:
			function_name = file.last_function
			label = file.current_command[1]
			label = function_name + "$" + label
		else:
			label = file.current_command[1]

		return "(%s)\n" % label

	def write_arithmetic(file):
		cmd = file.current_command[0]
		if cmd == "eq" or cmd == "lt" or cmd == "gt":
			instruction = comparator(file)
		else:
			instruction = arithmetic_table[cmd]

		return instruction

	def write_if(file):
		if file.last_function:
			function_name = file.last_function
			label = file.current_command[1]
			label = function_name + "$" + label
		else:
			label = file.current_command[1]

		instruction = "@SP\nAM=M-1\nD=M\n@%s\nD;JNE\n" % label
		return instruction

	def write_goto(file):
		if file.last_function:
			function_name = file.last_function
			label = file.current_command[1]
			label = function_name + "$" + label
		else:
			label = file.current_command[1]

		instruction = "@%s\n0;JMP\n" % label
		return instruction

	def init(file, command):
		file.current_command = command
		instruction = "@256\nD=A\n@SP\nM=D\n"
		instruction += CodeWriter.write_call(file)
		return instruction