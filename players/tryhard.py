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
	def __init__(self, game):
		self.__game = game
		self.__ideas = list()
		self.__addRandomIdea()

	def act(self):
		while True:
			result = self.__ideas[0].func.call(self.__game.getData())
			if not None in result: # if call didnt fail -> go on
				break
			self.__throwAwayActiveIdea() # if it failed remove the func & try it with a new one
		return result

	def evaluate(self, value):
		self.__ideas[0].evaluate(value)
		#   if your ideas dont change anything        or if you surrender
		if (value < 0 and self.__nothingHasChangedFor(3)) or (self.__ideas[0].success < SURRENDERSUCCESS):
			self.__throwAwayActiveIdea()

	def __addRandomIdea(self):
		self.__ideas.append(Idea.getRandomIdea(self.__game.getNoInput(), self.__game.getNoOutput()))

	def __updateIdeas(self):
		if self.__ideas[0].success < MIN: # the idea was pretty bad
			self.__throwAwayActiveIdea()
		else: # it was ok
			self.__cloneActiveIdea()

	def __throwAwayActiveIdea(self):
		self.__ideas.pop(0)
		if len(self.__ideas) < NOIDEAS:
			self.__addRandomIdea()

	def __cloneActiveIdea(self):
		self.__ideas.insert(0, sorted(self.__ideas, key=lambda idea: idea.success)[0].pseudoClone()) # clone it

	def __nothingHasChangedFor(self, i):
		hlen = len(self.__game.getHistory())
		for j in range(hlen-i, hlen-1):
			if self.__game.getHistory()[j] != self.__game.getHistory()[j+1]:
				return False
		return True


class Idea:
	def __init__(self, func):
		self.func = func
		self.success = 0

	def evaluate(self, value):
		self.success += value

	def pseudoClone(self):
		print("TODO pseudoClone")
		return self # TODO

	@staticmethod
	def getRandomIdea(noInput, noOutput):
		return Idea(MultiFunc.getRandom(noInput, noOutput))

