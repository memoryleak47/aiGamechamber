#!/usr/bin/python3

import random

WIDTH=30
HEIGHT=30

CATCH=1
RUN=0

class Rectgame:
	def __init__(self, players):
		self.__players=players

		job = CATCH
		for player in self.__players:
			player.data.append(job)
			player.data.append(random.randint(1,WIDTH-1))
			player.data.append(random.randint(1,HEIGHT-1))
			job = 1-job
	def render(self):
		field=list()

		field.append(list("#"*WIDTH))
		for i in range(HEIGHT-2):
			field.append(list("#" + " " * (WIDTH-2) + "#"))
		field.append(list("#"*WIDTH))

		for player in self.__players:
			if player.data[0] == CATCH:
				field[player.data[2]][player.data[1]] = "C"
			elif player.data[0] == RUN:
				field[player.data[2]][player.data[1]] = "R"
		for line in field:
			print("".join(line))

	def run(self):
		while True:
			for player in self.__players:
				self.render()
				plan = player.act()
				if plan[0] == -1 and player.data[1] > 1:
					player.data[1] -= 1
				elif plan[0] == 1 and player.data[1] < WIDTH-1:
					player.data[1] += 1

				if plan[1] == -1 and player.data[2] > 1:
					player.data[2] -= 1
				elif plan[1] == 1 and player.data[2] < HEIGHT-1:
					player.data[2] += 1
			input("Press any key to continue")
