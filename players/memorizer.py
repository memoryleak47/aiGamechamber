#!/usr/bin/python3 -B

import random
import sys
import os
sys.path.append(os.path.dirname(sys.path[0]))
import formatter
from player import *
import time

def die(string):
	print(string)
	1/0 # FOR THE STACK TRACE!

class Memorizer(Player):
	def __init__(self, game, id):
		Player.__init__(self, game, id)
		self.__knowledgebase = dict() # {datastr => {action1 => eval1, action2 => eval2}, datastr2 => ...}
		self.__lastDataStr = None
		self.__lastAction = None

	def act(self):
		self.__lastDataStr = str(self._game.getData())
		if str(self.__lastDataStr) in list(self.__knowledgebase.keys()):
			knowledge = self.__knowledgebase[self.__lastDataStr]
			bestKey = list(knowledge.keys())[0]
			for key, value in knowledge.items():
				if knowledge[bestKey] < knowledge[key]:
					bestKey = key
			if knowledge[bestKey] <= 0:
				self.__lastAction = self.__actRandom(self._game.getActionFormat())
			else:
				self.__lastAction = bestKey
		else:
			self.__lastAction = self.__actRandom(self._game.getActionFormat())
		return self.__lastAction

	def __actRandom(self, outputformat): # should not do stuff he already did
		if outputformat.startswith("{"):
			return self.__actRandom(random.choice(formatter.splitSections(outputformat)))
		if outputformat.startswith("("):
			t = tuple()
			sections = formatter.splitSections(outputformat)
			for section in sections:
				t += (self.__actRandom(section),)
			return t
		if outputformat.startswith("["):
			print("Memorizer: no lists yet")
			sys.exit()
		if outputformat.startswith("'") or outputformat.startswith('"'):
			return outputformat[1:-1]
		if outputformat == "float":
			return random.random() * 255666.4
		if outputformat == "int":
			return int(random.random() * 255666.4)
		if outputformat == "bool":
			return random.choice([False, True])
		print("Memorizer doesn't know outputformat=" + outputformat)

	def gameOver(self): pass

	def evaluate(self, value):
		if self.__lastDataStr not in list(self.__knowledgebase.keys()):
			self.__knowledgebase[self.__lastDataStr] = dict()
		self.__knowledgebase[self.__lastDataStr][self.__lastAction] = value
