#!/usr/bin/python3 -B

import random

class Kingofrandom:
	def __init__(self, game):
		self.__game = game

	def act(self):
		l = list()
		for i in range(self.__game.getNoOutput()):
			l.append(random.randint(-1000, 1000))
		return l

	def evaluate(self, value):
		pass
