import os

from backend import command_table
from File import File

class Parser:

	def __init__(self, file):

		self.parsed_files = self.parse_file(file)

	def parse_file(self, input_file):

		if os.path.exists(input_file):

			if os.path.isdir(input_file):
				stripped_files = []
				self.save_path = os.path.abspath(input_file)
		
				for each_file in os.listdir(input_file):
					file_name = os.path.basename(each_file)
					abs_path = self.save_path + "\\" + file_name
					_, ext = os.path.splitext(each_file)

					if ext == ".vm":
						with open(abs_path) as f:
							commands = self.strip_file(f.readlines())
						stripped_file = File(file_name, commands)
						stripped_files.append(stripped_file)

				self.save_path = os.path.join(self.save_path, os.path.basename(self.save_path)) + ".asm"

			else:
				file_name = os.path.basename(input_file)
				abs_path = os.path.abspath(input_file)
				self.save_path = abs_path.replace(".vm", ".asm")
				_, ext = os.path.splitext(input_file)

				if ext == ".vm":
					with open(abs_path) as f:
						commands = self.strip_file(f.readlines())
					stripped_files = [File(file_name, commands)]

		else:
			print("Couldn't find file.")
			quit()

		return stripped_files


	def strip_file(self, file):
		cmd_container = []

		for line in file:
			if "//" in line:
				vm_cmd = line.split("//")[0].split(" ")
			else:
				vm_cmd = line.split(" ")

			vm_cmd = [each_cmd.strip() for each_cmd in vm_cmd if each_cmd.strip()]

			if vm_cmd:
				cmd_container.append((vm_cmd))

		return cmd_container


	def has_more_commands(self, file):

		if file.commands:
			return True
		return False

	def advance(self, file):
		file.current_command = file.commands[0]

	def command_type(self, file):

		arg1 = file.current_command[0]

		for command_key in command_table.keys():
			if arg1 == command_key:
				return command_table[arg1]