#!/usr/bin/python3 -B

import random
import sys
import os
sys.path.append(os.path.dirname(sys.path[0]))
from mathcore import *
from player import *
import time

MIN = -10
NOIDEAS = 3
SURRENDERSUCCESS = -500

class Tryhard(Player):
	def __init__(self, game):
		Player.__init__(self, game)
		self.__ideas = list()
		self.__ideas.append(self.__getRandomIdea())

	def act(self):
		while True:
			result = self.__ideas[0].func.call(self._game.getData())
			if not None in result: # if call didnt fail -> go on
				break
			self.__throwAwayActiveIdea() # if it failed remove the func & try it with a new one
		return result

	def gameOver(self):
		self.__updateIdeas()

	def evaluate(self, value):
		self.__ideas[0].evaluate(value)
		#   if you surrender OR you get bad evals and don't do anything
		if (self.__ideas[0].success < SURRENDERSUCCESS) or (value < 0 and self.__nothingHasChangedFor(3)):
			self.__throwAwayActiveIdea()

	def __getRandomIdea(self):
		return Idea.getRandomIdea(self._game.getNoInput(), self._game.getNoOutput())

	def __throwAwayActiveIdea(self):
		self.__ideas.pop(0)
		if len(self.__ideas) < NOIDEAS:
			self.__ideas.append(self.__getRandomIdea())

	def __addActiveIdeaMutation(self):
		self.__ideas.insert(0, self.__ideas[0].getMutation())

	def __nothingHasChangedFor(self, i):
		hlen = len(self._game.getHistory())

		for j in range(hlen-i, hlen-1):
			if self._game.getHistory()[j] != self._game.getHistory()[j+1]:
				return False
		return True

	def __updateIdeas(self):
		if self.__ideas[0].success < MIN: # the idea was pretty bad
			self.__throwAwayActiveIdea()
		else: # it was ok
			self.__addActiveIdeaMutation()



class Idea:
	def __init__(self, func):
		self.func = func
		self.success = 0

	def evaluate(self, value):
		self.success += value

	@staticmethod
	def getRandomIdea(noInput, noOutput):
		return Idea(MultiFunc.getRandom(noInput, noOutput, complexity=(0,10)))

	def getMutation(self):
		print("getMutation TODO")
		return self

