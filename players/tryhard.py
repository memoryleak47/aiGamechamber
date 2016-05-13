#!/usr/bin/python3 -B

import random

STARTVALUE = 0
MIN = -10
NOIDEAS = 3
MIN_COMPLEXITY = 0
MAX_COMPLEXITY = 3
SURRENDERSUCCESS = -400

operators = ["max($,$)", "min($,$)", "($+$)", "($-$)", "(float($)/float($))", "($*$)"]

class Idea:
	def __init__(self, func):
		self.func = func
		self.success = STARTVALUE

	def assess(self, value):
		self.success += value

	def pseudoClone(self):
		print("TODO pseudoClone")
		return self # TODO

	@staticmethod
	def getRandomIdea(noInput, noOutput):
		func = "$" + (",$" * (noOutput - 1))
		for i in range(random.randint(MIN_COMPLEXITY, MAX_COMPLEXITY)):

			# load spots
			spots=list()
			for spot in range(len(func)):
				if func[spot] == "$":
					spots.append(spot)

			# find chosenspot
			chosenspot = spots[random.randint(0, len(spots)-1)]

			# find chosenoperator
			chosenoperator = operators[random.randint(0,len(operators)-1)]

			# insert
			func = func[:chosenspot] + chosenoperator + func[chosenspot+1:]

		while "$" in func:
			spot = func.find("$")
			func = func[:spot] + "gameinfo[" + str(random.randint(0, noInput-1)) + "]" + func[spot+1:]

		return Idea(func)


class Tryhard:
	def __init__(self, noInput, noOutput):
		self.noInput = noInput
		self.noOutput = noOutput
		self.data = list() # TODO remove
		self.__ideas = list()
		self.__success = 0

		self.addRandomIdea()

	def act(self, gameinfo):
		print("func=" + self.__ideas[0].func)
		return eval(self.__ideas[0].func)

	def assess(self, value):
		self.__success += value
		self.__ideas[0].assess(value)
		if self.__success < SURRENDERSUCCESS:
			self.updateIdeas()

	def gameOver(self):
		self.updateIdeas()

	def addRandomIdea(self):
		self.__ideas.append(Idea.getRandomIdea(self.noInput, self.noOutput))

	def updateIdeas(self):
		print("ideas are now updated")
		self.__success = 0
		activeIdea = self.__ideas[0]
		if activeIdea.success < MIN: # the idea was pretty bad
			self.__ideas.remove(activeIdea) # try something completely new
			if len(self.__ideas) < NOIDEAS:
				self.addRandomIdea()
		else: # it was ok
			self.__ideas.insert(0, sorted(self.__ideas, key=lambda idea: idea.success)[0].pseudoClone()) # clone it
