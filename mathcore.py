#!/usr/bin/python3 -B

import random
import sys

operators = ["(-$)", "max($,$)", "min($,$)", "($+$)", "($-$)", "(float($)/float($))", "($*$)"]

def die(string):
	print(string)
	1/0 # FOR THE STACK TRACE!

class Func:
	pass

class MultiFunc(Func):
	def __init__(self, funcs):
		self.funcs = funcs

	def toString(self):
		s = ""
		for func in self.funcs:
			s += func.toString() + ", "
		return s.strip(", ")

	@staticmethod
	def getByStrings(strings):
		funcs = list()
		for string in strings:
			funcs.append(SingleFunc(string))
		return MultiFunc(funcs)

	def call(self, args):
		results = list()
		for func in self.funcs:
			results.append(func.call(args))
		return results

	@staticmethod
	def getRandom(noInput, noOutput):
		funcs = list()
		for i in range(noOutput):
			funcs.append(SingleFunc.getRandom(noInput))
		return MultiFunc(funcs)

class SingleFunc(Func):
	def __init__(self, string):
		if not isinstance(string, str):
			die("SingleFunc(string): (" + str(string) + ")is not a string")
		self.string = string

	def toString(self):
		return self.string

	def call(self, args):
		result = -1
		try:
			result = eval(self.string)
		except:
			print("func call failed: " + self.string)
		return result

	@staticmethod
	def getRandom(noInput):
		string = "$"
		for i in range(random.randint(0, 4)):

			# load spots
			spots=list()
			for spot in range(len(string)):
				if string[spot] == "$":
					spots.append(spot)

			# find chosenspot
			chosenspot = spots[random.randint(0, len(spots)-1)]

			# find chosenoperator
			chosenoperator = operators[random.randint(0,len(operators)-1)]

			# insert
			string = string[:chosenspot] + chosenoperator + string[chosenspot+1:]

		while "$" in string:
			spot = string.find("$")
			string = string[:spot] + "args[" + str(random.randint(0, noInput-1)) + "]" + string[spot+1:]

		return SingleFunc(string)
