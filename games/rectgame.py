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
		self.__players=list()
		self.__data=list() # [p0.x, p0.y, p1.x, p1.y]

	def run(self, players):
		self.__players = players

		self.__data = []
		self.__data.append(random.randint(1,WIDTH-2))
		self.__data.append(random.randint(1,HEIGHT-2))
		self.__data.append(random.randint(1,WIDTH-2))
		self.__data.append(random.randint(1,HEIGHT-2))

		while True:
			for i in range(len(self.__players)):
				self.render(self.__players[i])
				plan = self.__players[i].act(self.__data)
				if plan[0] < 0 and self.__data[2*i] > 1:
					self.__data[2*i] -= 1
				elif plan[0] > 0 and self.__data[2*i] < WIDTH-2:
					self.__data[2*i] += 1

				if plan[1] < 0 and self.__data[1 + 2*i] > 1:
					self.__data[1 + 2*i] -= 1
				elif plan[1] > 0 and self.__data[1 + 2*i]< HEIGHT-2:
					self.__data[1 + 2*i] += 1

				if (self.__data[0] == self.__data[2]) and (self.__data[1]) == (self.__data[3]):
					self.__players[0].assess(100)
					self.__players[1].assess(-100)
					self.__players[0].gameOver()
					self.__players[1].gameOver()
					print("Game Over")
					return
			self.__players[0].assess(-1)
			self.__players[1].assess(1)
			time.sleep(0.05)

	def render(self, activePlayer):
		field=list()

		field.append(list("#"*WIDTH))
		for i in range(HEIGHT-2):
			field.append(list("#" + " " * (WIDTH-2) + "#"))
		field.append(list("#"*WIDTH))

		char = "c"
		if self.__players[0] == activePlayer:
			char = char.upper()
		field[self.__data[1]][self.__data[0]] = char

		char = "r"
		if self.__players[1] == activePlayer:
			char = char.upper()
		field[self.__data[3]][self.__data[2]] = char

		for line in field:
			print("".join(line))

	def getNoInput(self):
		return self.noplayers * 2

	def getNoOutput(self):
		return 2
