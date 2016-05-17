#!/usr/bin/python3

import random
import sys
import time

WIDTH=30
HEIGHT=30

class Rectgame:
	def __init__(self, noplayers):
		if noplayers != 2:
			print("Invalid size")
			sys.exit()
		self.noplayers = noplayers
		self.__players = list()
		self.__data = list() # [p0.x, p0.y, p1.x, p1.y]
		self.__history = list()

	def start(self, players):
		self.__players = players
		self.__repositionPlayers()

	def applyAction(self, action, playerID):
		if action[0] < 0 and self.__data[2*playerID] > 1:
			self.__data[2*playerID] -= 1
		elif action[0] > 0 and self.__data[2*playerID] < WIDTH-2:
			self.__data[2*playerID] += 1

		if action[1] < 0 and self.__data[1 + 2*playerID] > 1:
			self.__data[1 + 2*playerID] -= 1
		elif action[1] > 0 and self.__data[1 + 2*playerID] < WIDTH-2:
			self.__data[1 + 2*playerID] += 1
		self.__updateData()
		if self.__areTheyCatching():
			self.__getCatcher().evaluate(100)
			self.__getRunner().evaluate(-100)
			self.__repositionPlayers()
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
		field[self.__data[1]][self.__data[0]] = char

		char = "r"
		field[self.__data[3]][self.__data[2]] = char

		for line in field:
			print("".join(line))

	def getHistory(self):
		return self.__history.copy()

	def getData(self):
		return self.__data.copy()

	def getNoInput(self):
		return self.noplayers * 2

	def getNoOutput(self):
		return 2

	def __getCatcher(self):
		return self.__players[0]

	def __getRunner(self):
		return self.__players[1]

	def __updateData(self):
		self.__history.append(self.__data.copy())

	def __repositionPlayers(self):
		self.__data = [random.randint(1, WIDTH-2), random.randint(1, HEIGHT-2), random.randint(1,WIDTH-2), random.randint(1,HEIGHT-2)]
		self.__updateData()

	def __areTheyCatching(self):
		return (self.__data[0] == self.__data[2]) and (self.__data[1]) == (self.__data[3])

