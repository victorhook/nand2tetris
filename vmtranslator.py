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

		self.files = self.open()
		self.text= self.trim_text()
		

	def open(self):
		file = "StackTest.vm"
		#file = input("What file do you want to translate? ")
		self.file_name = file

		try:
			if os.path.exists(file):
					# If input is a file
				if os.path.isfile(file):
					return [open(file).readlines()]

				else:
					# If input is a directory
					all_files = []
					for each_list in os.walk(file):
						for each_file in each_list[2]:
							if each_file.endswith(".vm"):
								all_files.append(open(file + "/" + each_file).readlines())
					return all_files

			else:
				raise FileNotFoundError("File not found.")

		except FileNotFoundError:
			print("File can't be opened. Check if it exists")
			sys.exit()

	def trim_text(self):

		new_file = []
		for each in self.files:

			for line in each:
				line = line.replace(" ", "")
				if "//" in line:
					index = line.find("//")
					line = line[:index]
				line = line.strip()
				if line:
					new_file.append(line)

		return new_file


	def has_more_commands(self):
		if self.text:
			return True
		return False

	def advance(self):
		self.command = self.text[0]

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

	def i(self, cmd):
		# Finds the value of i in the command
		# Is only called when cmd has a 2nd argument.
		index = self.command.find(cmd) + len(cmd)
		return self.command[index:]

class CodeWriter:

	def __init__(self, input_file):
		self.input_file = input_file
		self.constructor()


	def constructor(self):
		self.file = self.input_file.split(".")[0] + ".asm"


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


	def write_push_pop(self, arg1, arg2, i):
		# Using the backend code tables to grab the correct translation of
		# the Push or Pop commands.

		instruction = backend.Code.push_pop[arg1].replace("i", i)

		if arg2 == "constant":
			instruction = backend.Code.push_pop[arg2].replace("i", i)

		else:
			instruction = instruction.replace("segment", backend.Code.second_arguments[arg2])

			if arg2 == "temp" or arg2 == "pointer":
				instruction = instruction.replace("D+M", "D+A")

		return instruction


	def close(self, instructions):
		# Save all the code as a string 

		with open(self.file, "w") as f:
			f.write(instructions)

		if os.path.exists(self.file):
			print("File {} was saved correctly.".format(self.file))



parser = Parser()
code = CodeWriter(parser.file_name)
parser.translated_text = ""

while True:

	if parser.has_more_commands():
		parser.advance()
	else:
		break

	# Checks the command type, to know which arguments are needed.
	cmd_type = parser.command_type()
	if not cmd_type:
		print("Couldn't set command type.")
		sys.exit()

	# Parses the arguments that are required for later code.
	if cmd_type != "C_RETURN":
		arg1 = parser.arg1(cmd_type)
		
	if cmd_type == "C_PUSH" or cmd_type == "C_POP" or cmd_type == "C_FUNCTION" or cmd_type == "C_CALL":
		arg2 = parser.arg2()
		i = parser.i(arg2)


	# Returns the asm code.
	if cmd_type == "C_ARITHMETIC":
		instruction = code.write_arithmetic(arg1)

	elif cmd_type == "C_PUSH" or cmd_type == "C_POP":
		instruction = code.write_push_pop(arg1, arg2, i)

	# Appends the instruction to the total code (list). Then pops the command
	# to continue the loop.
	instruction = "//" +  parser.command + "\n" + instruction + "\n//-------\n"
	parser.translated_text += instruction
	parser.text.pop(0)

code.close(parser.translated_text)
	

