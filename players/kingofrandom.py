#!/usr/bin/python3 -B

import random
from player import *

class Kingofrandom(Player):
	def __init__(self, game, id):
		Player.__init__(self, game, id)

	def act(self):
		l = list()
		for i in range(self._game.getNoOutput()):
			l.append(random.randint(-1000, 1000))
		return l

	def evaluate(self, value):
		pass
