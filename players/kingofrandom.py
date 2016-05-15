#!/usr/bin/python3 -B

import random

class Kingofrandom:
	def __init__(self, noInput, noOutput):
		self.noOutput = noOutput

	def act(self, gameinfo):
		l = list()
		for i in range(self.noOutput):
			l.append(random.randint(-1000, 1000))
		return l

	def assess(self, value):
		pass
