#!/usr/bin/python3 -B

COUNTER_STOP = 1000

def die(msg):
	print(msg)
	1/0 # FOR THE STACK TRACE

class Frame:
	def __init__(self, input):
		self.spot = 0
		self.vars = [0, input]
		self.counter = 0

class Algorhithm:
	def __init__(self, cmds):
		self.cmds = cmds

	@staticmethod
	def parse(text):
		lines = text.strip("\n").split("\n")
		cmd = list()
		for line in lines:
			splat = line.split(" ")
			if splat[0] == "ifgo":
				cmd.append(IfgoCommand(int(splat[1]), int(splat[2])))
			elif splat[0] == "set":
				cmd.append(SetCommand(int(splat[1]), splat[2]))
			else:
				die("wot?")
		return Algorhithm(cmd)

	def call(self, input):
		frame = Frame(input)
		while frame.spot < len(self.cmds) and frame.spot >= 0 and frame.counter < COUNTER_STOP:
			tmpspot = frame.spot
			self.cmds[frame.spot].call(frame)
			frame.counter += 1
		return frame.vars[0]

	def toString(self):
		return '\n'.join([x.toString() for x in self.cmds])

class IfgoCommand:
	def __init__(self, condition, line):
		self.condition = condition
		self.line = line

	def call(self, frame):
		if frame.vars[self.condition]:
			frame.spot = self.line
		else:
			frame.spot += 1

	def toString(self):
		return "ifgo " + str(self.condition) + " " + str(self.line)

class SetCommand:
	def __init__(self, var, func):
		self.var = var
		self.func = func

	def call(self, frame):
		try:
			vars = frame.vars.copy()
			x = eval(self.func)
		except:
			print("SetCommand::call(): invalid func:", self.func)
		while len(frame.vars)-1 < self.var:
			frame.vars.append(0)
		frame.vars[self.var] = x
		frame.spot += 1

	def toString(self):
		return "set " + str(self.var) + " " + self.func

"""
operators = [
	(lambda x: x[0] + x[1], "(int,int)", "int"),
	(lambda x: x[0] + x[1], "(float,float)", "float"),
	(lambda x: x[0] + x[1], "(int,float)", "float"),
	(lambda x: x[0] + x[1], "(float,int)", "float"),
	(lambda x: x[0] + x[1], "(str,str)", "str"),
	(lambda x: x[0] + x[1], "(str,str)", "str"),
	(lambda x: (x, x+1), "int", "(int,int)"),
]
"""
