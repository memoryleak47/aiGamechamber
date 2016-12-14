#!/usr/bin/python3 -B

import random
import sys
import os
sys.path.append(os.path.dirname(sys.path[0]))
import formatter
from player import *
import time

SURRENDERSUCCESS = -800
FAVSUCCESS = 100
MAXFAVS = 20
PARENT_FACTOR = 0.1

def die(string):
	print(string)
	1/0 # FOR THE STACK TRACE!

class FuncTryhard(Player):
	def __init__(self, game, id):
		Player.__init__(self, game, id)
		self.__idea = None
		self.__favs = list()
		self.__ideaStartTime = 0

		self.__updateIdea()

	def act(self):
		return self.__idea.call(self._game.getData())

	def gameOver(self):
		if self.__idea.success <= 0:
			self.__updateIdea()

	def evaluate(self, value):
		self.__idea.evaluate(value)
		print(self.__idea.toString())
		#   if you surrender OR you get bad evals and don't do anything
		if (self.__idea.success <= SURRENDERSUCCESS) or (value <= 0 and self.__isStuck()):
			self.__updateIdea()

	def __updateIdea(self):
		if (self.__idea != None) and (self.__idea not in self.__favs) and (self.__idea.highestSuccess >= FAVSUCCESS):
			self.__addToFavs(self.__idea)
		self.__idea = self.__getNewIdea()
		self.__ideaStartTime = self._game.getTime()

	def __isStuck(self):
		history = self._game.getHistory()[max(self._game.getStartTime(), self.__ideaStartTime):]
		stuckCircle = list()
		for data in reversed(history):
			if len(stuckCircle) > 2 and len(stuckCircle)*2 <= len(history) and data == stuckCircle[0]:
				clen = len(stuckCircle)
				for i in range(len(stuckCircle)):
					if stuckCircle[i] != list(reversed(history))[clen + i]:
						return False
				return True
			stuckCircle.append(data)
		return False

	def __getNewIdea(self):
		if len(self.__favs) == 0 or random.randint(0, 1) == 0:
			self.__ideaStartTime = self._game.getTime()
			return Idea.getRandom(self._game.getDataFormat(), self._game.getActionFormat())
		else:
			highestSuccessSum = 0
			for fav in self.__favs:
				highestSuccessSum += fav.highestSuccess
			tmp = random.random() * highestSuccessSum
			for fav in self.__favs:
				tmp -= fav.highestSuccess
				if tmp <= 0:
					return fav.getMutation()

	def __addToFavs(self, idea):
		if idea not in self.__favs:
			idea.parent = None
			self.__favs.append(idea)
			if len(self.__favs) > MAXFAVS:
				minspot = 0
				for i in range(len(self.__favs)):
					if self.__favs[i].highestSuccess < self.__favs[minspot].highestSuccess:
						minspot = i
				self.__favs.pop(minspot)

# idea

class Idea:
	def __init__(self, func, inputformat, outputformat):
		self.func = func 
		self.inputformat = inputformat
		self.outputformat = outputformat
		self.success = 0
		self.highestSuccess = 0
		self.parent = None

	@staticmethod
	def getRandom(inputformat, outputformat):
		return Idea(getRandomFunc(inputformat, outputformat), inputformat, outputformat)

	def toString(self):
		return "success= " + str(self.success) + "\n" + self.func.toString()

	def call(self, data):
		return self.func.call(data)

	def evaluate(self, value):
		self.success += value
		if self.parent != None:
			self.parent.highestSuccess += value * PARENT_FACTOR
		self.highestSuccess = max(self.success, self.highestSuccess)

	def getMutation(self):
		return Idea(self.func.getMutation(), self.inputformat, self.outputformat)

# func

ERRORDATA="_ERRORDATA_"
PRIMITIVE_TYPES = ['float', 'int', 'bool', 'str']

def getRandomFunc(inputformat, outputformat): # creates a Func, that converts data which matches inputdata to data which matches outputdata
		if "{" in inputformat:
			return InputSwitchFunc.getRandom(inputformat, outputformat)
		if "{" in outputformat:
			return OutputSwitchFunc.getRandom(inputformat, outputformat)
		if outputformat.startswith("("):
			return TupleFunc.getRandom(inputformat, outputformat)
		if outputformat.startswith("["):
			die("no lists yet")
			return ERRORDATA
		if outputformat == "int":
			return EvalFunc(getRandomPrimitiveFuncStr(inputformat, "int"), inputformat, outputformat)
		if outputformat == "float":
			return EvalFunc(getRandomPrimitiveFuncStr(inputformat, "float"), inputformat, outputformat)
		if outputformat == "str":
			return EvalFunc(getRandomPrimitiveFuncStr(inputformat, "str"), inputformat, outputformat)
		if outputformat == "bool":
			return EvalFunc(getRandomPrimitiveFuncStr(inputformat, "bool"), inputformat, outputformat)
		if outputformat.startswith("'") or outputformat.startswith('"'):
			return EvalFunc("'" + outputformat[1:-1] + "'", inputformat, outputformat)
		die("getRandomFunc(). dunno, what todo with outputformat=" + outputformat)

class InputSwitchFunc: # has one func for every inputformat permutation
	def __init__(self, inputformats, funcs):
		self.inputformats = inputformats
		self.funcs = funcs

	def call(self, args):
		for i in range(len(self.inputformats)):
			if formatter.matches(arg, self.inputformats[i]):
				return funcs[i].call(args)
		die("BraceFunc::call(): no format is matched")
		return ERRORDATA

	def getMutation(self):
		funcs = [x.copy() for x in self.funcs]
		i = random.choice(range(len(funcs)))
		funcs[i] = funcs[i].getMutation()
		return InputSwitchFunc(self.inputformats.copy(), funcs)

	def copy(self):
		return InputSwitchFunc(self.inputformats.copy(), [x.copy() for x in self.funcs])

	def toString(self):
		return "InputSwitchFunc(\n" + ["\t" + x.toString() + "\n" for x in self.funcs] + "\n)\n"

	@staticmethod
	def getRandom(inputformat, outputformat):
		inputformats = formatter.getPermutations(inputformat)
		return InputSwitchFunc(inputformats, [getRandomFunc(inputformats[i], outputformat) for i in range(len(inputformats))])

class OutputSwitchFunc: # has one condition and func for every outputformat permutation
	def __init__(self, outputformats, conditions, funcs):
		self.outputformats = outputformats
		self.conditions = conditions
		self.funcs = funcs

	def call(self, args):
		for i in range(len(self.conditions)):
			if self.conditions[i].call(args) == True:
				return self.funcs[i].call(args)
		return self.funcs[-1].call(args)

	def getMutation(self):
		funcs = [x.copy() for x in self.funcs]
		conditions = [x.copy() for x in self.conditions]
		if random.random() > 0.5:
			i = random.choice(range(len(funcs)))
			funcs[i] = funcs[i].getMutation()
		else:
			i = random.choice(range(len(conditions)))
			conditions[i] = conditions[i].getMutation()
		return OutputSwitchFunc(self.outputformats.copy(), conditions, funcs)

	def copy(self):
		return OutputSwitchFunc(self.outputformats.copy(), [x.copy() for x in self.conditions], [x.copy() for x in self.funcs])

	def toString(self):
		return "OutputSwitchFunc(\n" + "\n".join(["\t" + self.conditions[i].toString() + ":\n\t\t" + self.funcs[i].toString() for i in range(len(self.conditions))]) + "\n\t" + self.funcs[-1].toString() + "\n)\n"

	@staticmethod
	def getRandom(inputformat, outputformat):
		outputformats = formatter.getPermutations(outputformat)
		return OutputSwitchFunc(outputformats, [getRandomFunc(inputformat, "bool") for x in range(len(outputformats)-1)], [getRandomFunc(inputformat, x) for x in outputformats])

class TupleFunc:
	def __init__(self, parts):
		self.parts = parts

	def call(self, args):
		t = tuple()
		for part in self.parts:
			t += (part.call(args),) # to make it tuply anyhow
		return t

	def getMutation(self):
		parts = self.parts.copy()
		i = random.choice(range(len(parts)))
		parts[i] = parts[i].getMutation()
		return TupleFunc(parts)

	def copy(self):
		return TupleFunc(self.parts.copy())

	def toString(self):
		return "TupleFunc(" + ", ".join([x.toString() for x in self.parts]) + ")"

	@staticmethod
	def getRandom(inputformat, outputformat):
		parts = list()
		outputformats = formatter.splitSections(outputformat)
		for format in outputformats:
			parts.append(getRandomFunc(inputformat, format))
		return TupleFunc(parts)

class EvalFunc:
	def __init__(self, string, inputformat, outputformat):
		self.string = string
		self.inputformat = inputformat
		self.outputformat = outputformat

	def call(self, args):
		try:
			return eval(self.string)
		except:
			print("EvalFunc::call() failed func=" + self.string + " with args=" + str(args))
			return ERRORDATA

	def getMutation(self):
		return getRandomFunc(self.inputformat, self.outputformat) # TODO correct?

	def copy(self):
		return EvalFunc(self.string, self.inputformat, self.outputformat)

	def toString(self):
		return "EvalFunc(" + self.string + ")"

def getRandomPrimitiveFuncStr(inputformat, outputtype, recursion=0.95):
	operators = getOperators("any", outputtype)
	if len(operators) == 0:
		return getRandomPrimitiveValueStr(outputtype, inputformat)
	outteroperator = random.choice(operators)
	opstring = outteroperator[0]
	opin = outteroperator[1]
	opout = outteroperator[2]

	if random.random() < recursion: # another step
		while "$" in opstring:
			funcstr = getRandomPrimitiveFuncStr(inputformat, opin, recursion/2)
			if funcstr == ERRORDATA:
				return ERRORDATA
			opstring = opstring.replace("$", funcstr, 1)
	else: # insert real values
		while "$" in opstring:
			opstring = opstring.replace("$", getRandomPrimitiveValueStr(opin, inputformat), 1)
	return opstring

def getRandomPrimitiveValueStr(type, format):
	strSpots = getPrimitiveStrSpots(type, format)
	if False and random.random() < 0.25: # there is a list to reduce from
		# reduce
		pass
	elif len(strSpots) > 0 and random.random() < 0.8:
		return random.choice(strSpots)
	else:
		if type == "float":
			x = random.random() * 35565 * random.random() * random.random() * random.random() # optimize?
			if random.random() < 0.2:
				return str(-x)
			return str(x)
		elif type == "int":
			x = int(random.random() * 35565 * random.random() * random.random() * random.random()) # optimize?
			if random.random() < 0.2:
				return str(-x)
			return str(x)
		elif type == "bool":
			return str(random.random() < 0.5)
		elif type == "str":
			return "\"very random generated string\""
		elif type == "any":
			return getRandomPrimitiveValueStr(random.choice(PRIMITIVE_TYPES), format)
		die("getRandomPrimitiveValueStr(" + type + ", " + format + "): unknown type")

def getPrimitiveStrSpots(type, format):
	i = 0
	while i < len(format): # remove lists
		if format[i] == "[":
			while format[i] != "]":
				format = format[:i] + format[i+1:]
		i += 1

	spots = list()
	counter = list()
	i = 0
	while i < len(format):
		if format[i] == "(":
			counter.append("0")
			i += 1
		elif format[i] == ")":
			counter = counter[:-1]
			i += 1
		elif format[i] == ",":
			tmp = counter[-1]
			counter = counter[:-1]
			counter.append(str(int(tmp)+1))
			i += 1
		else:
			f = format[i:]
			commaspot = f.find(",")
			if commaspot != -1:
				f = f[:commaspot]
			parenspot = f.find(")")
			if parenspot != -1:
				f = f[:parenspot]
			if typeContains(type, f):
				tmp = "args[" + ']['.join(counter) + "]"
				if tmp == "args[]":
					tmp = "args"
				spots.append(tmp)
			if commaspot == -1:
				break
			else:
				i += commaspot
	return spots

def getOperators(inputtype, outputtype):
	ops = [
		("($/$)", "float", "float"),
		("($+$)", "int", "int"),
		("($-$)", "int", "int"),
		("($*$)", "int", "int"),
		("min($,$)", "int", "int"),
		("max($,$)", "int", "int"),
		("($<$)", "int", "bool"),
		("($>$)", "int", "bool"),
		("($==$)", "any", "bool"),
		("(not($))", "bool", "bool"),
		("($)and($)", "bool", "bool"),
		("($)or($)", "bool", "bool"),
		("int($)", "float", "int")
	]
	result = list()
	for op in ops:
		if typeContains(inputtype, op[1]) and typeContains(outputtype, op[2]):
			result.append(op)
	return result

def typeContains(a, b):
	return (a == "any" or a == b or (a == "float" and b == "int"))
