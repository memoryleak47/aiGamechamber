#!/usr/bin/python3 -B

from player import *

class Human(Player):
	def __init__(self, game):
		pass

	def act(self):
		return eval(input(">> "))
