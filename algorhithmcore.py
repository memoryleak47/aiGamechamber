#!/usr/bin/python3 -B

COUNTER_STOP = 1000

def die(msg):
	print(msg)
	1/0 # FOR THE STACK TRACE

class Frame:
	def __init__(self, args):
		self.spot = 0
		self.vars = [0] + args
		self.counter = 0

class Algorhithm:
	def __init__(self, cmds):
		self.cmds = cmds

	@staticmethod
	def parse(text):
		lines = text.split("\n")
		cmd = list()
		for line in lines:
			splat = line.split(" ")
			if splat[0] == "ifgo":
				cmd.append(IfgoCommand(splat[1], splat[2]))
			elif splat[0] == "set":
				cmd.append(SetCommand(splat[1], OperatorPointer(splat[2], splat[3])))
			else:
				die("wot?")
		return cmd

	def call(self, args):
		frame = Frame(args)
		while frame.spot < len(self.cmds)-1 and frame.counter < COUNTER_STOP:
			cmds[frame.spot].call(frame)
			frame.counter += 1
		return frame.vars[0]

	def toString(self):
		return '\n'.join([x.toString() for x in self.cmds])

class IfgoCommand:
	def __init__(self, condition, line):
		self.condition = condition
		self.line = line

	def call(self, frame):
		if True == frame.vars[self.condition]:
			frame.spot = self.line

	def toString(self):
		return "ifgo " + condition + " " + line

class SetCommand:
	def __init__(self, var, operatorPointer):
		self.var = var
		self.operatorPointer = operatorPointer

	def call(self, frame):
		frame.vars[self.var] = self.operatorPointer.call(frame)
		frame.spot += 1

	def toString(self):
		return "set " + self.var + " " + self.operatorPointer.id + " " + self.operatorPointer.var

class OperatorPointer:
	def __init__(self, id, var):
		self.id = id
		self.var = var

	def call(self, frame):
		return operators[self.id](frame.vars[var])

operators = [
	(lambda x: x[0] + x[1], "(int,int)", "int"),
	(lambda x: x[0] + x[1], "(float,float)", "float"),
	(lambda x: x[0] + x[1], "(int,float)", "float"),
	(lambda x: x[0] + x[1], "(float,int)", "float"),
	(lambda x: x[0] + x[1], "(str,str)", "str"),
	(lambda x: x[0] + x[1], "(str,str)", "str"),
	(lambda x: (x, x+1), "int", "(int,int)"),
]
