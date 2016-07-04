#!/usr/bin/python3 -B

import random
import sys
import os
sys.path.append(os.path.dirname(sys.path[0]))
import formatter
from player import *

class KingOfRandom(Player):
	def __init__(self, game, id):
		Player.__init__(self, game, id)

	def act(self):
		return self.call(self._game.getActionFormat())

	def call(self, outputformat):
		if outputformat.startswith("{"):
			return self.call(random.choice(formatter.splitSections(outputformat)))
		if outputformat.startswith("("):
			t = tuple()
			sections = formatter.splitSections(outputformat)
			for section in sections:
				t += (self.call(section),)
			return t
		if outputformat.startswith("["):
			print("KingOfRandom: no lists yet")
			sys.exit()
		if outputformat.startswith("'") or outputformat.startswith('"'):
			return outputformat[1:-1]
		if outputformat == "float":
			return random.random() * 255666.4
		if outputformat == "int":
			return int(random.random() * 255666.4)
		if outputformat == "bool":
			return random.choice([False, True])
		print("KingOfRandom doesn't know outputformat=" + outputformat)

	def evaluate(self, value): pass
