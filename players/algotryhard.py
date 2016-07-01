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

class AlgoTryhard(Player):
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

class Idea:
	def __init__(self, parts, inputformat, outputformat):
		self.parts = parts
		self.inputformat = inputformat
		self.outputformat = outputformat
		self.success = 0
		self.highestSuccess = 0
		self.parent = None

	@staticmethod
	def getRandom(inputformat, outputformat):
		sections = formatter.splitSections(outputformat)
		return Idea([IdeaPart.getRandom(inputformat, sections[i]) for i in range(len(sections))], inputformat, outputformat)

	def toString(self):
		return "{\n\tsuccess = " + str(self.success) + "\n" + "\n\n".join(["\tparts[" + str(i) + "] =\n\t\t" + self.parts[i].toString() for i in range(len(self.parts))]) + "\n}"

	def call(self, data):
		return [part.call(data) for part in self.parts]

	def evaluate(self, value):
		self.success += value
		if self.parent != None:
			self.parent.highestSuccess += value * PARENT_FACTOR
		self.highestSuccess = max(self.success, self.highestSuccess)


	def getMutation(self):
		parts = self.parts.copy()
		index = random.randint(0, len(parts)-1)
		parts[index] = parts[index].getMutation()
		idea = Idea(parts, self.inputformat, self.outputformat)
		idea.parent = self
		return idea

class IdeaPart:
	def __init__(self, funcs, equations, inputformat):
		self.funcs = funcs
		self.equations = equations
		self.inputformat = inputformat

	@staticmethod
	def getRandom(inputformat, outputtype):
		rand = random.randint(0, 4)
		return IdeaPart([UpdateOnCrashFunc.getRandom(inputformat, outputtype) for i in range(rand+1)], [UpdateOnCrashFunc.getRandom(inputformat, "bool") for i in range(rand)], inputformat)

	def call(self, data):
		for i in range(len(self.equations)):
			if self.equations[i].call(data):
				return self.funcs[i].call(data)
		return self.funcs[-1].call(data)

	def toString(self):
		return "\n\t\t".join([self.equations[i].toString() + ":\n\t\t\t\t" + self.funcs[i].toString() for i in range(len(self.equations))]) + "\n\t\tdefault:\n\t\t\t\t" + self.funcs[-1].toString()

	def getMutation(self):
		funcs = self.funcs.copy()
		equations = self.equations.copy()
		if len(self.equations) == 0:
			rand = random.randint(2, 3) # 0 / 1 not possible when there is no equation
		else:
			rand = random.randint(0, 3)

		if rand == 0:
			# remove a func + equation
			rand = random.randint(0, len(equations)-1)
			funcs.pop(rand)
			equations.pop(rand)
		elif rand == 1:
			# alter an equation
			rand = random.randint(0, len(equations)-1)
			equations.pop(rand)
			equations.insert(rand, UpdateOnCrashFunc.getRandom(inputformat, "bool"))
		elif rand == 2:
			# alter a func
			rand = random.randint(0, len(funcs)-1)
			funcs.pop(rand)
			funcs.insert(rand, UpdateOnCrashFunc.getRandom(inputformat, formatter.splitSections(outputformat)[rand]))
		elif rand == 3:
			# add a func + equation
			rand = random.randint(0, len(funcs))
			funcs.insert(rand, UpdateOnCrashFunc.getRandom(inputformat, formatter.splitSections(outputformat)[rand]))
			equations.insert(rand, UpdateOnCrashFunc.getRandom(inputformat, "bool"))
		else:
			print("man. really...?")
		return IdeaPart(funcs, equations, self.inputformat)

class UpdateOnCrashFunc:
	def __init__(self, arg, inputformat, outputtype):
		if isinstance(arg, str):
			self.func = Func(string)
		elif isinstance(arg, Func):
			self.func = arg
		else:
			die("UpdateOnCrashFunc: wrong arg type")
		self.inputformat = inputformat
		self.outputtype = outputtype

	def toString(self):
		return self.func.toString()

	@staticmethod
	def getRandom(inputformat, outputtype):
		return UpdateOnCrashFunc(Func.getRandom(inputformat, outputtype), inputformat, outputtype)

	def call(self, args):
		while True:
			result = self.func.call(args, silent=True)
			if result != ERRORDATA:
				break
			# print("UpdateOnCrashFunc: update!")
			self.func = Func.getRandom(self.inputformat, self.outputtype)
		return result

# algorhithm

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

	@staticmethod
	def getRandom(inputformat, outputformat): pass
		# TODO
		# check with which inputdata, we can build the outputdata
		# ____________________________________
		# Input:  |(int)a   |(float)b | (int)c|
		# Output: |(float)d |(bool)e  |       |
		# *************************************

		# |
		# V

		# d = (b*a)
		# e = (a == c)
		#
		# and now insert ifgo's, which don't change the datatypes of the used variables

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
