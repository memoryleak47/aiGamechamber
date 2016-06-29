#!/usr/bin/python3 -B

import random
from player import *

class Kingofrandom(Player):
	def __init__(self, game, id):
		Player.__init__(self, game, id)

	def act(self):
		print("Kingofrandom::act: TODO")

	def evaluate(self, value):
		pass
