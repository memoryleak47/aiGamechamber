#!/usr/bin/python3 -B

from player import *

class Human(Player):
	def __init__(self, game, id):
		Player.__init__(self, game, id)

	def act(self):
		return eval(input(">> "))
