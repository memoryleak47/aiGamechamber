#!/usr/bin/python3 -B

import random

STARTVALUE = 0
MIN = -10
NOIDEAS = 3

operators = ["max($,$)", "min($,$)", "($+$)", "($-$)", "(float($)/float($))", "($*$)"]

class Idea:
	def __init__(self, func, noinfos):
		self.func = func
		self.success = STARTVALUE

	def assess(self, value):
		self.success += value

	def pseudoClone(self):
		pass

	@staticmethod
	def getRandomIdea(noinfos):
		pass


class Tryhard:
	def __init__(self, noinfos):
		self.noinfos = noinfos # number of infos
		self.data = list() # TODO remove
		self.__ideas = list()

		self.__ideas.append(Idea.getRandomIdea())

	def act(gameinfo):
		return eval(self.__ideas[0].func)

	def assess(self, value):
		self.__ideas[0].assess(value)

	def gameOver(self):
		activeIdea = self.__ideas[0]
		if activeIdea.success < MIN: # the idea was pretty bad
			self.__ideas.remove(activeIdea) # try something completely new
			if len(self.__ideas) < NOIDEAS:
				self.__ideas.append(Idea.getRandomIdea())
		else: # it was ok
			self.__ideas.insert(0, sorted(self.__ideas, key=success)[0].pseudoClone()) # clone it
