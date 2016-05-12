#!/usr/bin/python3

import random
import sys

WIDTH=30
HEIGHT=30

CATCH=1
RUN=0

class Rectgame:
	def __init__(self, players):
		if len(players) != 2:
			print("Invalid size")
			sys.exit()

		self.__players=players

		self.__players[0].data.append(CATCH)
		self.__players[1].data.append(RUN)

		self.__players[0].data.append(random.randint(1,WIDTH-2))
		self.__players[0].data.append(random.randint(1,HEIGHT-2))
		self.__players[1].data.append(random.randint(1,WIDTH-2))
		self.__players[1].data.append(random.randint(1,HEIGHT-2))
	def render(self, activePlayer):
		field=list()

		field.append(list("#"*WIDTH))
		for i in range(HEIGHT-2):
			field.append(list("#" + " " * (WIDTH-2) + "#"))
		field.append(list("#"*WIDTH))

		for player in self.__players:
			
			if player.data[0] == CATCH:
				char = "c"
			elif player.data[0] == RUN:
				char = "r"
			if player == activePlayer:
				char = char.upper()
			field[player.data[2]][player.data[1]] = char

		for line in field:
			print("".join(line))

	def run(self):
		while True:
			for player in self.__players:
				self.render(player)
				plan = player.act()
				if plan[0] == -1 and player.data[1] > 1:
					player.data[1] -= 1
				elif plan[0] == 1 and player.data[1] < WIDTH-2:
					player.data[1] += 1

				if plan[1] == -1 and player.data[2] > 1:
					player.data[2] -= 1
				elif plan[1] == 1 and player.data[2] < HEIGHT-2:
					player.data[2] += 1

				if (self.__players[0].data[1] == self.__players[1].data[1]) and (self.__players[0].data[2]) == (self.__players[1].data[2]):
					self.__players[0].assess(100)
					self.__players[1].assess(-100)
					print("The game is over")
					return
			self.__players[1].assess(1)
			self.__players[0].assess(-1)
			input("Press any key to continue")
