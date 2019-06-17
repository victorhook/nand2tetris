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
m="popconstant17"
cmd_type = "C_PUSH"
for command in commands[cmd_type]:
	print(command)
	if command in m:
		print(command)