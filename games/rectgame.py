#!/usr/bin/python3

import random
import sys
import time
from game import *

WIDTH=30
HEIGHT=30

class Rectgame(Game):
	def __init__(self, noPlayers):
		if noPlayers != 2:
			print("Invalid size")
			sys.exit()
		Game.__init__(self, noPlayers)

	def _restart(self):
		self.__repositionPlayers()

	def applyAction(self, action, playerID):
		if action[0] < 0 and self.getData()[2*playerID] > 1:
			self._incDataMember(2*playerID, -1)
		elif action[0] > 0 and self.getData()[2*playerID] < WIDTH-2:
			self._incDataMember(2*playerID, +1)

		if action[1] < 0 and self.getData()[1 + 2*playerID] > 1:
			self._incDataMember(1 + 2*playerID, -1)
		elif action[1] > 0 and self.getData()[1 + 2*playerID] < WIDTH-2:
			self._incDataMember(1 + 2*playerID, +1)
		if self.__areTheyCatching():
			self.__getCatcher().evaluate(100)
			self.__getRunner().evaluate(-100)
			self._gameOver()
		else:
			self.__getCatcher().evaluate(-1)
			self.__getRunner().evaluate(1)

	def render(self):
		field=list()

		field.append(list("#"*WIDTH))
		for i in range(HEIGHT-2):
			field.append(list("#" + " " * (WIDTH-2) + "#"))
		field.append(list("#"*WIDTH))

		char = "c"
		field[self.getData()[1]][self.getData()[0]] = char

		char = "r"
		field[self.getData()[3]][self.getData()[2]] = char

		for line in field:
			print("".join(line))

	def getNoInput(self):
		return self.getNoPlayers() * 2

	def getNoOutput(self):
		return 2

	def __getCatcher(self):
		return self._getPlayer(0)

	def __getRunner(self):
		return self._getPlayer(1)

	def __repositionPlayers(self):
		self._setData([random.randint(1, WIDTH-2), random.randint(1, HEIGHT-2), random.randint(1,WIDTH-2), random.randint(1,HEIGHT-2)])

	def __areTheyCatching(self):
		return (self.getData()[0] == self.getData()[2]) and (self.getData()[1]) == (self.getData()[3])

