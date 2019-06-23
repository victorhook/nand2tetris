import os
import backend
import sys

"""
R0 = SP
R1 = LCL
R2 = ARG
R3 = THIS
R4 = THAT
R5-12 = temp
R13-15 = free
pointer => R3 + i
"""

class Parser:

	def __init__(self):

		# Initialization of the object, opens file/dir and trims it.
		# White space is removed, comments are removed.
		# An error is raised and program stops if file/dir can't be opened.

		self.files, self.file_names = self.open()
		# Self.text is a list containing each files, seperated as lists.
		self.text = self.trim_text()
		self.functions = {}
		self.return_address = {}


	def open(self):
		file = "BasicLoop.vm"
		#file = input("What file do you want to translate? ")
		self.file_name = file
		all_files = []
		file_names = []
		try:
			if os.path.exists(file):
					# If input is a file
				if os.path.isfile(file):
					all_files.append(open(file).readlines())
					name, ext = os.path.splitext(file)
					file_names.append(name)

				else:
					# If input is a directory
					all_files = []
					file_names = []
					for each_list in os.walk(file):
						for each_file in each_list[2]:
							name, ext = os.path.splitext(each_file)
							if ext == ".vm":
								all_files.append(open(file + "/" + each_file).readlines())
								file_names.append(name)
				return all_files, file_names

			else:
				raise FileNotFoundError("File not found.")

		except FileNotFoundError:
			print("\nFile can't be opened. Check if it exists")
			sys.exit()

	def trim_text(self):

		
		container = []
		for each in self.files:
			new_file = []
			for line in each:
				line = line.replace(" ", "")
				if "//" in line:
					index = line.find("//")
					line = line[:index]
				line = line.strip()
				if line:
					new_file.append(line)

			container.append(new_file)

		new_file = {}
		for index, name in enumerate(self.file_names):
			new_file[name] = container[index]

		# Return a dictionary with each key being the file names with
		# their corresponding text as values.
		return new_file


	def has_more_commands(self, file):
		if self.text[file]:
			return True
		return False

	def advance(self, file):
		self.command = self.text[file][0]

	def command_type(self):
		# Returns the type of command it is
		for command in backend.commands.keys():
			for each in backend.commands[command]:
				if each in self.command:
					return command


	def arg1(self, cmd_type):
		# Returns the first argument of the command
		for command in backend.commands[cmd_type]:
			if command in self.command:
				return command


	def arg2(self):
		# Returns the second argument of command.
		# Only called if cmd_type == push, pop, function or call
		for index, command in enumerate(backend.second_argument):
			if command in self.command:
				return backend.second_argument[index]

	def func(self, cmd):
		# Returns the function name as 'func'
		# Returns n arguments as 'args' - NOTE: Function name can't contain integers!
		func = cmd.split("function")[1]
		for index, letter in enumerate(cmd):
			if letter.isdigit():
				index = index

		nargs = cmd[index:]
		funcname = func.split(nargs)[0]
		return funcname, nargs


	def i(self, cmd):
		# Finds the value of i in the command
		# Is only called when cmd has a 2nd argument.
		index = self.command.find(cmd) + len(cmd)
		return self.command[index:]


	def call(self, cmd):
		# Returns the function name as 'func'
		# Returns n arguments as 'args' - NOTE: Function name can't contain integers!
		name = cmd.split("call")[1]
		for index, letter in enumerate(cmd):
			if letter.isdigit():
				nargs = cmd[index]

		funcname = name.split(nargs)[0]
		return funcname, nargs



class CodeWriter:

	def __init__(self, input_file):
		self.input_file = input_file
		self.constructor()


	def constructor(self):
		self.file = self.input_file.split(".")[0] + ".asm"

	def init(self):
		# Writes the initialization of the file.
		pass

	def write_arithmetic(self, arg1):
		# 
		instruction = backend.Code.arithmetic[arg1]
		i = backend.Code.arithmetic["comp_counter"]

		if arg1 == "lt" or arg1 == "gt" or arg1 == "eq":
			instruction = instruction.replace("_i", str(i))

			if arg1 == "lt":
				instruction = instruction.replace("condition", "JLT")

			elif arg1 == "gt":
				instruction = instruction.replace("condition", "JGT")

			elif arg1 == "eq":
				instruction = instruction.replace("condition", "JEQ")

		backend.Code.arithmetic["comp_counter"] += 1

		return instruction


	def write_push_pop(self, arg1, arg2, i, file):
		# Using the backend code tables to grab the correct translation of
		# the Push or Pop commands.

		instruction = backend.Code.push_pop[arg1].replace("i", i)

		if arg2 == "constant":
			instruction = backend.Code.push_pop[arg2].replace("i", i)

		elif arg2 == "static":
			variable = file + "." + i
			instruction = backend.Code.push_pop[arg2][arg1].replace("variable", variable)

		else:
			instruction = instruction.replace("segment", backend.Code.second_arguments[arg2])

			if arg2 == "temp" or arg2 == "pointer":
				instruction = instruction.replace("D+M", "D+A")

		return instruction

	def label(self, cmd):
		return "(%s)" % (cmd.split("label")[1])

	def goto(self, cmd):
		addr = cmd.split("goto")[1]
		instruction = "@%s\n0;JMP" % (addr)
		return instruction

	def if_goto(self, cmd):
		addr = cmd.split("if-goto")[1]
		instruction = "@SP\nAM=M-1\nD=M\n@%s\nD;JNE" % (addr)
		return instruction

	def write_call(self, funcname, nargs, file):
		# Defines two functions that sets the arguments and
		# sets the stack according to the nargs.

		def set_args(nargs):
			# Sets n arguments from the stack to the argument segment.
			# RAM[ARG] + n = RAM[SP] + n 		 * n times
			instruction = ""
			for index, arg in enumerate(range(nargs)[::-1]):
				set_args = "@%s\nD=A\n@argument\nD=D+M\n@R13\nM=D\n@SP\nD=M\n@%s\nA=D-A\n@R13\nA=M\nM=D\n" % (index, arg)
				instruction += set_args
			return instruction

		def set_stack(funcname, nargs, file, return_address):
			# return address
			return_address = "@SP\nA=M\nM=M\n"

			# Save segments
			push_lcl = "@local\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
			push_arg = "@argument\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
			push_this = "@this\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
			push_that = "@that\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"

			# ARG = SP-5-nargs
			reposition_arg = "@SP\nD=M\n@5\nD=D-A\n@%s\nD=D-A\n@argument\nM=D\n" % nargs

			# LCL = SP
			lcl = "@SP\nD=M\n@local\nM=D\n"

			# goto functionName
			goto_func = "@%s\n0;JMP" % funcname

			# Declare a label
			"(%s$ret.%s)" % (file, return_address)

			instruction = return_address + push_lcl + push_arg + push_this + push_that
			instruction += reposition_arg + lcl + goto_func
			return instruction

		return_number = parser.return_address[file]
		nargs = int(nargs)

		# Combines the returns to return a single string instruction
		set_arguments = set_args(nargs)
		set_stack = set_stack(funcname, nargs, file, return_number)
		instruction = set_arguments + set_stack

		return instruction


	def write_return(self):
		# end frame = LCL
		end_frame = "@LCL\nD=M\n@temp\nM=D\n"

		# return address = *(end_frame - 5)
		return_address = "@temp\nD=M\n@5\nA=D-A\nD=M\n@temp\nM=D\n"

		# *ARG = pop()
		return_value = "@SP\nA=M-1\nD=M\n@argument\nA=M\nM=D\n"

		# Reposition SP of the caller
		sp_reset = "@argument\nD=M+1\n@SP\nM=D\n"

		# Restores segments
		that = "@local\nA=M-1\nM=D\nD=M\n@that\nM=D\n"
		this = "@local\nD=M\n@2\nA=D-A\nM=D\n@this\nM=D\n"
		arg = "@local\nD=M\n@3\nA=D-A\nM=D\n@argument\nM=D\n"
		lcl = "@local\nD=M\n@4\nA=D-A\nM=D\n@local\nM=D\n"

		# goto return address
		goto_return = "@temp\n0;JMP"

		instruction = end_frame + return_address + return_value + sp_reset
		instruction += that + this + that + arg + lcl + goto_return
		return instruction	

	def write_function(self, funcname, nargs, file):
		# Insert label as (Function Name)
		# Sets n ram memories on the local segments to 0.
		# RAM[LCL] + n = 0		* n times

		instruction = "(%s.%s)\n" % (file, funcname)
		for arg in range(int(nargs)):
			set_vars = "@%s\nD=A\n@local\nA=D+M\nM=0\n" % arg
			instruction += set_vars

		return instruction

	def close(self, instructions):
		# Save all the code as a string 

		with open(self.file, "w") as f:
			f.write(instructions)

		if os.path.exists(self.file):
			print("\nFile {} was saved correctly in filepath:".format(self.file))
			print(os.getcwd() + self.file)


parser = Parser()
code = CodeWriter(parser.file_name)
parser.translated_text = ""
files_translated = 0

for file in parser.text.keys():
	parser.return_address[file] = 0
	while True:
		if parser.has_more_commands(file):
			parser.advance(file)
			cmd = parser.command
		else:
			break

		cmd_type = parser.command_type()
		
		# Get corresponding arguments
		if cmd_type != "C_RETURN":
			arg1 = parser.arg1(cmd_type)

		if cmd_type == "C_PUSH" or cmd_type == "C_POP":
			arg2 = parser.arg2()
			i = parser.i(arg2)

		elif cmd_type == "C_FUNCTION":
			funcname, nargs = parser.func(cmd)

		elif cmd_type == "C_CALL":
			funcname, nargs = parser.call(cmd)


		# Return the asm code 
		if cmd_type == "C_ARITHMETIC":
			instruction = code.write_arithmetic(arg1)

		elif cmd_type == "C_LABEL":
			instruction = code.label(cmd)

		elif cmd_type == "C_GOTO":
			instruction = code.goto(cmd)

		elif cmd_type == "C_IF":
			instruction = code.if_goto(cmd)

		elif cmd_type == "C_PUSH" or cmd_type == "C_POP":
			instruction = code.write_push_pop(arg1, arg2, i, file)

		elif cmd_type == "C_FUNCTION":
			instruction = code.write_function(funcname, nargs, file)

		elif cmd_type == "C_CALL":
			instruction = code.write_call(funcname, nargs, file)

		elif cmd_type == "C_RETURN":
			instruction = code.write_return()

		instruction = "// " + parser.command + "\n" + instruction + "\n\n"
		parser.translated_text += instruction
		parser.text[file].pop(0)
	
code.close(parser.translated_text)
print(parser.translated_text)
