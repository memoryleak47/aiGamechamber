#!/usr/bin/python3

import random

width=30
height=30

CATCH=1
RUN=0

class Rectgame:
	def __init__(self, players):
		self.__players=players

		job = CATCH
		for player in self.__players:
			player.data.append(job)
			player.data.append(random.randint(1,width-1))
			player.data.append(random.randint(1,height-1))
			job = 1-job
	def render(self):
		field=list()

		field.append(list("#"*width))
		for i in range(height-2):
			field.append(list("#" + " " * (width-2) + "#"))
		field.append(list("#"*width))

		for player in self.__players:
			if player.data[0] == CATCH:
				field[player.data[1]][player.data[2]] = "C"
			elif player.data[0] == RUN:
				field[player.data[1]][player.data[2]] = "R"
		for line in field:
			print("".join(line))
	def run(self):
		self.render()
