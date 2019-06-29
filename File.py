class File:

	def __init__(self, file_name, commands):

		self.file_name = file_name
		self.commands = commands
		self.return_counter = 0
		self.arithmetic_counter = {"add":0, "sub":0, "neg":0, "eq":0, "gt":0, "lt":0, "eq":0, "and":0, "not":0, "or":0}
		self.current_command = ""
		self.last_function = ""

	def __repr__(self):
		return self.file_name