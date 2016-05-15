#!/usr/bin/python3 -B

import random
import sys
import os
sys.path.append(os.path.dirname(sys.path[0]))
from mathcore import *

MIN = -10
NOIDEAS = 3
SURRENDERSUCCESS = -50

class Tryhard:
	def __init__(self, noInput, noOutput):
		self.noInput = noInput
		self.noOutput = noOutput
		self.__ideas = list()

		self.addRandomIdea()

	def act(self, gameinfo):
		return self.__ideas[0].func.call(gameinfo)

	def assess(self, value):
		self.__ideas[0].assess(value)
		if self.__ideas[0].success < SURRENDERSUCCESS:
			self.throwAwayActiveIdea()

	def gameOver(self):
		self.updateIdeas()

	def addRandomIdea(self):
		self.__ideas.append(Idea.getRandomIdea(self.noInput, self.noOutput))

	def updateIdeas(self):
		if self.__ideas[0].success < MIN: # the idea was pretty bad
			self.throwAwayActiveIdea()
		else: # it was ok
			self.cloneActiveIdea()

	def throwAwayActiveIdea(self):
		self.__ideas.pop(0)
		if len(self.__ideas) < NOIDEAS:
			self.addRandomIdea()

	def cloneActiveIdea(self):
		self.__ideas.insert(0, sorted(self.__ideas, key=lambda idea: idea.success)[0].pseudoClone()) # clone it


class Idea:
	def __init__(self, func):
		self.func = func
		self.success = 0

	def assess(self, value):
		self.success += value

	def pseudoClone(self):
		print("TODO pseudoClone")
		return self # TODO

	@staticmethod
	def getRandomIdea(noInput, noOutput):
		return Idea(MultiFunc.getRandom(noInput, noOutput))

