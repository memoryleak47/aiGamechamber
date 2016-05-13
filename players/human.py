#!/usr/bin/python3 -B

class Human:
	def __init__(self, noInput, noOutput):
		self.data = list()

	def act(self, gameinfo):
		return eval(input(">> "))

	def assess(self, value):
		pass
