import os

from CodeWriter import CodeWriter
from File import File
from Parser import Parser


if __name__ == "__main__":

	parser = Parser(r"C:\Users\vicke\Programmering\nand2tetris\projects\08\FunctionCalls\NestedCall")

	finished_text = ""

	for file in parser.parsed_files:
		for command in file.commands:
			if len(command) >= 2:
				if command[1].lower() == "sys.init":
					finished_text = CodeWriter.init(file, command)
					file.current_command = file.commands[0]	

	for file in parser.parsed_files:
		while True:
			if parser.has_more_commands(file):
				parser.advance(file)
			else:
				break
			cmd_type = parser.command_type(file)
			if cmd_type == "C_PUSH":
				instruction = CodeWriter.write_push(file)

			elif cmd_type == "C_POP":
				instruction = CodeWriter.write_pop(file)

			elif cmd_type == "C_FUNCTION":
				file.last_function = file.current_command[1]
				instruction = CodeWriter.write_function(file)

			elif cmd_type == "C_CALL":
				instruction = CodeWriter.write_call(file)

			elif cmd_type == "C_RETURN":
				instruction = CodeWriter.write_return(file)

			elif cmd_type == "C_IF":
				instruction = CodeWriter.write_if(file)

			elif cmd_type == "C_GOTO":
				instruction = CodeWriter.write_goto(file)

			elif cmd_type == "C_LABEL":
				instruction = CodeWriter.write_label(file)

			elif cmd_type == "C_ARITHMETIC":
				instruction = CodeWriter.write_arithmetic(file)

			finished_text += "//" + " ".join(file.current_command) + "\n" +  instruction
			file.commands.pop(0)

	with open(parser.save_path, "w") as f:
		f.write(finished_text)
		print("File has been translated.")
		print("The script is saved at: %s" % parser.save_path)



