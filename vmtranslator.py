import os
import backend
import sys
"""
RAM ADDRESSES		Usage
0-15				Virtual register
16-255				Static variables
256-2047			Stack
2048-16483			Heap
16384-24575			Memory mapped I/O

"""


class Parser:

	def __init__(self):

		# Initialization of the object, opens file/dir and trims it.
		# White space is removed, comments are removed.
		# An error is raised and program stops if file/dir can't be opened.

		self.files = self.open()
		self.text= self.trim_text()
		

	def open(self):
		#file = "test"
		file = input("What file do you want to translate? ")
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
		return backend.Code.arithmetic[arg1]


	def write_push_pop(self, arg1, arg2, i):
		if arg2 == "constant":
			assembly = backend.Code.push_pop[arg1].replace("i", "{}".format(i)).replace("@segment\nD=D+M\n", "")

		else:
			assembly = backend.Code.push_pop[arg1]
			assembly = assembly.replace("i", "{}".format(i)).replace("segment", "{}".format(backend.Code.second_arguments[arg2]))
		
		return assembly


	def close(self, instructions):
		# Save all the code as a string 
		save = ""

		for ins in instructions:
			ins = parser.command + "\n" + ins + "\n//-------\n\n"
			save += ins

		with open(self.file, "w") as f:
			f.write(save)

		if os.path.exists(self.file):
			print("File {} was saved correctly.".format(self.file))



parser = Parser()
code = CodeWriter(parser.file_name)
parser.translated_text = []

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
	parser.translated_text.append(instruction)
	parser.text.pop(0)

code.close(parser.translated_text)
	

