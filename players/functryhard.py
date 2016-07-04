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
		return "success= " + str(self.success)

	def call(self, data):
		return self.func.call(data)

	def evaluate(self, value):
		self.success += value
		if self.parent != None:
			self.parent.highestSuccess += value * PARENT_FACTOR
		self.highestSuccess = max(self.success, self.highestSuccess)

	def getMutation(self):
		die("TODO getMutation")

# func

ERRORDATA="_ERRORDATA_"

def getRandomFunc(inputformat, outputformat): # creates a Func, that converts data which matches inputdata to data which matches outputdata
		if inputformat.startswith("{"):
			return BraceFunc.getRandom(inputformat, outputformat)
		if outputformat.startswith("{"):
			return getRandomFunc(inputformat, random.choice(formatter.splitSections(outputformat)))
		if outputformat.startswith("("):
			return ParenFunc.getRandom(inputformat, outputformat)
		if outputformat.startswith("["):
			die("no lists yet")
			return ERRORDATA
		if outputformat == "int":
			return EvalFunc(getRandomPrimitiveFuncStr(inputformat, "int"))
		if outputformat == "float":
			return EvalFunc(getRandomPrimitiveFuncStr(inputformat, "float"))
		if outputformat == "str":
			return EvalFunc(getRandomPrimitiveFuncStr(inputformat, "str"))
		if outputformat == "bool":
			return EvalFunc(getRandomPrimitiveFuncStr(inputformat, "bool"))
		if outputformat.startswith("'") or outputformat.startswith('"'):
			return EvalFunc("'" + outputformat[1:-1] + "'")
		die("getRandomFunc(). dunno, what todo with outputformat=" + outputformat)

class BraceFunc:
	def __init__(self, inputformats, funcs):
		self.inputformats = inputformats
		self.funcs = funcs

	def call(self, args):
		for i in range(len(self.inputformats)):
			if formatter.matches(arg, self.inputformats[i]):
				return funcs[i].call(args)
		die("BraceFunc::call(): no format is matched")
		return ERRORDATA

	@staticmethod
	def getRandom(inputformat, outputformat):
		inputformats = formatter.splitSections(inputformat)
		return BraceFunc(inputformats, [getRandomFunc(inputformats[i], outputformat) for i in range(len(inputformats))])

class ParenFunc:
	def __init__(self, parts):
		self.parts = parts

	def call(self, args):
		t = tuple()
		for part in self.parts:
			t += (part.call(args),) # to make it tuply anyhow
		return t

	@staticmethod
	def getRandom(inputformat, outputformat):
		parts = list()
		outputformats = formatter.splitSections(outputformat)
		for format in outputformats:
			parts.append(getRandomFunc(inputformat, format))
		return ParenFunc(parts)

class EvalFunc:
	def __init__(self, string):
		self.string = string

	def call(self, args):
		try:
			return eval(self.string)
		except:
			die("EvalFunc::call() failed func=" + self.string)

def getRandomPrimitiveFuncStr(inputformat, outputtype, recursion=0.95):
	outteroperator = random.choice(getOperators("any", outputtype))
	opstring = outteroperator[0]
	opin = outteroperator[1]
	opout = outteroperator[2]

	if random.random() < recursion: # another step
		while "$" in opstring:
			opstring = opstring.replace("$", getRandomPrimitiveFuncStr("any", opin, recursion/2), 1)
	else: # insert real values
		while "$" in opstring:
			opstring = opstring.replace("$", getRandomPrimitiveValueStr(opin), 1)
	return opstring

def getRandomPrimitiveValueStr(type, format):
	if False and random.random() < 0.25: # there is a list to reduce from
		# reduce
		pass
	elif random.random() < 0.5:
		return random.choice(getPrimitiveStrSpots(type, format))
	else:
		if type == "float":
			x = random.random() * 35565 # optimize?
			if random.random() < 0.2:
				return -x
			return x
		elif type == "int":
			x = int(random.random() * 35565 * random.random()) # optimize?
			if random.random() < 0.2:
				return -x
			return x
		elif type == "bool":
			return random.random() < 0.5
		elif type == "str":
			return "very random generated string"
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
	for i in range(len(format)):
		if format[i] == "(":
			counter.append("0")
		elif format[i] == ")":
			counter = counter[:-1]
		elif format[i] == ",":
			tmp = counter[-1]
			counter = counter[:-1]
			counter.append(str(int(tmp)+1))
		elif format[i:].startswith(type):
			tmp = "args[" + ']['.join(counter) + "]"
			if tmp == "args[]":
				tmp = "args"
			spots.append(tmp)
	return spots

def getOperators(inputtype, outputtype):
	ops = [
		("($+$)", "float", "float"),
		("($-$)", "float", "float"),
		("($*$)", "float", "float"),
		("($/$)", "float", "float"),
		("min($,$)", "float", "float"),
		("max($,$)", "float", "float"),
		("($<$)", "float", "bool"),
		("($>$)", "float", "bool"),
		("($==$)", "any", "bool"),
		("not($)", "bool", "bool"),
		("($)and($)", "bool", "bool"),
		("($)or($)", "bool", "bool")
	]
	result = list()
	for op in ops:
		if (op[1] == "any" or inputtype == "any" or op[1] == inputtype) and (op[2] == "any" or outputtype == "any" or op[2] == outputtype):
			result.append(op)
	return result
