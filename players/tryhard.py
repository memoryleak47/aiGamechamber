#!/usr/bin/python3 -B

import random
import sys
import os
sys.path.append(os.path.dirname(sys.path[0]))
from mathcore import *
from player import *
import time

SURRENDERSUCCESS = -800
MUTATESUCCESS = 300
MUTATESTOP = 100
LAZINESS_PUNISHMENT = 50

class Tryhard(Player):
	def __init__(self, game, id):
		Player.__init__(self, game, id)
		self.__ideas = list()
		self.__appendRandomIdea()
		self.__ideaStartTime = 0

	def act(self):
		return self.__ideas[0].call(self._game.getData())

	def gameOver(self):
		self.__updateIdeas()

	def evaluate(self, value):
		self.__ideas[0].evaluate(value)
		#   if you surrender OR you get bad evals and don't do anything
		if (self.__ideas[0].success <= SURRENDERSUCCESS):
			self.__throwAwayActiveIdea()
		elif (value <= 0 and self.__isStuck()):
			self.__ideas[0].success -= LAZINESS_PUNISHMENT
			self.__switchIdeas()
		elif (self.__ideas[0].success >= MUTATESUCCESS):
			self.__ideas[0].success -= MUTATESTOP
			self.__insertActiveIdeaMutation()

	def __throwAwayActiveIdea(self):
		# print(str(self.getID()) + ": - " + str(len(self.__ideas)))
		self.__ideas.pop(0)
		if len(self.__ideas) == 0:
			self.__appendRandomIdea()
		self.__ideaStartTime = self._game.getTime()

	def __switchIdeas(self):
		self.__ideas.append(self.__ideas.pop(0))

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

	def __updateIdeas(self):
		if self.__ideas[0].success < 0: # the idea was pretty bad
			self.__throwAwayActiveIdea()
		else: # it was ok
			self.__insertActiveIdeaMutation()

	def __insertRandomIdea(self):
		self.__ideaStartTime = self._game.getTime()
		self.__ideas.insert(0, Idea.getRandom(self._game.getNoInput(), self._game.getNoOutput()))
		# print(str(self.getID()) + ": + " + str(len(self.__ideas)))

	def __appendRandomIdea(self):
		self.__ideas.append(Idea.getRandom(self._game.getNoInput(), self._game.getNoOutput()))
		# print(str(self.getID()) + ": + " + str(len(self.__ideas)))

	def __insertActiveIdeaMutation(self):
		self.__ideaStartTime = self._game.getTime()
		self.__ideas.insert(0, self.__ideas[0].getMutation())
		# print(str(self.getID()) + ": mutate")
		# print(str(self.getID()) + ": + " + str(len(self.__ideas)))

	def __appendActiveIdeaMutation(self):
		self.__ideas.append(self.__ideas[0].getMutation())
		# print(str(self.getID()) + ": + " + str(len(self.__ideas)))




class Idea:
	def __init__(self, parts, noInput, noOutput):
		self.parts = parts
		self.noInput = noInput
		self.noOutput = noOutput
		self.success = 0

	@staticmethod
	def getRandom(noInput, noOutput):
		return Idea([IdeaPart.getRandom(noInput) for i in range(noOutput)], noInput, noOutput)

	def toString(self):
		return "{\n\tsuccess = " + str(self.success) + "\n" + "\n\n".join(["\tparts[" + str(i) + "] =\n\t\t" + self.parts[i].toString() for i in range(len(self.parts))]) + "\n}"

	def call(self, data):
		result = list()
		for part in self.parts:
			partresult = part.call(data)
			result.append(part.call(data))
		return result

	def evaluate(self, value):
		self.success += value

	def getMutation(self):
		parts = self.parts.copy()
		index = random.randint(0, len(parts)-1)
		parts[index] = parts[index].getMutation()
		return Idea(parts, self.noInput, self.noOutput)

class IdeaPart:
	def __init__(self, funcs, equations, noInput):
		self.funcs = funcs
		self.equations = equations
		self.noInput = noInput

	@staticmethod
	def getRandom(noInput):
		rand = random.randint(0, 4)
		return IdeaPart([UpdateOnCrashFunc.getRandom(noInput, FLOAT, FLOAT) for i in range(rand+1)], [UpdateOnCrashFunc.getRandom(noInput, FLOAT, BOOL) for i in range(rand)], noInput)

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
			equations.insert(rand, UpdateOnCrashFunc.getRandom(self.noInput, FLOAT, BOOL))
		elif rand == 2:
			# alter a func
			rand = random.randint(0, len(funcs)-1)
			funcs.pop(rand)
			funcs.insert(rand, UpdateOnCrashFunc.getRandom(self.noInput, FLOAT, FLOAT))
		elif rand == 3:
			# add a func + equation
			rand = random.randint(0, len(funcs))
			funcs.insert(rand, UpdateOnCrashFunc.getRandom(self.noInput, FLOAT, FLOAT))
			equations.insert(rand, UpdateOnCrashFunc.getRandom(self.noInput, FLOAT, BOOL))
		else:
			print("man. really...?")
		return IdeaPart(funcs, equations, self.noInput)

class UpdateOnCrashFunc:
	def __init__(self, arg, noInput, inputtype, outputtype):
		if isinstance(arg, str):
			self.func = Func(string)
		elif isinstance(arg, Func):
			self.func = arg
		else:
			die("UpdateOnCrashFunc: wrong arg type")
		self.noInput = noInput
		self.inputtype = inputtype
		self.outputtype = outputtype

	def toString(self):
		return self.func.toString()

	@staticmethod
	def getRandom(noInput, inputtype, outputtype):
		return UpdateOnCrashFunc(Func.getRandom(noInput, inputtype, outputtype), noInput, inputtype, outputtype)

	def call(self, args):
		while True:
			result = self.func.call(args, silent=True)
			if result != ERRORDATA:
				break
			# print("UpdateOnCrashFunc: update!")
			self.func = Func.getRandom(self.noInput, self.inputtype, self.outputtype)
		return result
