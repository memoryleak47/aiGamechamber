#!/usr/bin/python3

import random
import sys

WIDTH=30
HEIGHT=30

class Rectgame:
	def __init__(self, noplayers):
		if noplayers != 2:
			print("Invalid size")
			sys.exit()
		self.noplayers = noplayers
		self.__players=list()

	def run(self, players):
		self.__players = players

		self.__players[0].data.append(random.randint(1,WIDTH-2))
		self.__players[0].data.append(random.randint(1,HEIGHT-2))
		self.__players[1].data.append(random.randint(1,WIDTH-2))
		self.__players[1].data.append(random.randint(1,HEIGHT-2))
		while True:
			for player in self.__players:
				self.render(player)
				plan = player.act(self.__players[0].data + self.__players[1].data)
				if plan[0] == -1 and player.data[0] > 1:
					player.data[0] -= 1
				elif plan[0] == 1 and player.data[0] < WIDTH-2:
					player.data[0] += 1

				if plan[1] == -1 and player.data[1] > 1:
					player.data[1] -= 1
				elif plan[1] == 1 and player.data[1] < HEIGHT-2:
					player.data[1] += 1

				if (self.__players[0].data[0] == self.__players[1].data[0]) and (self.__players[0].data[1]) == (self.__players[1].data[1]):
					self.__players[0].assess(100)
					self.__players[1].assess(-100)
					self.__players[0].gameOver()
					self.__players[1].gameOver()
					print("Game Over")
					return
			self.__players[1].assess(1)
			self.__players[0].assess(-1)
			input("Press any key to continue")

	def render(self, activePlayer):
		field=list()

		field.append(list("#"*WIDTH))
		for i in range(HEIGHT-2):
			field.append(list("#" + " " * (WIDTH-2) + "#"))
		field.append(list("#"*WIDTH))

		char = "c"
		if self.__players[0] == activePlayer:
			char = char.upper()
		field[self.__players[0].data[1]][self.__players[0].data[0]] = char

		char = "r"
		if self.__players[1] == activePlayer:
			char = char.upper()
		field[self.__players[1].data[1]][self.__players[1].data[0]] = char

		for line in field:
			print("".join(line))

	def getNoInfos(self):
		return self.noplayers * 2
