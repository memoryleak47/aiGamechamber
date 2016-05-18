#!/usr/bin/python3 -B

import random
import sys

# <types>
FLOAT=0
BOOL=1
# </types>

def getOperators(type):
	if type == FLOAT:
		return ["(-$)", "max($,$)", "min($,$)", "($+$)", "($-$)", "(float($)/float($))", "($*$)"]
	elif type == BOOL:
		return ["not($)", "($)and($)", "($)or($)"]

def die(string):
	print(string)
	1/0 # FOR THE STACK TRACE!

class Func:
	def __init__(self, string):
		if not isinstance(string, str):
			die("Func(string): (" + str(string) + ")is not a string")
		self.string = string

	def toString(self):
		return self.string

	def call(self, args):
		result = None
		try:
			result = eval(self.string)
		except:
			print("func call failed: " + self.string)
		return result

	@staticmethod
	def getRandom(noInput, type=FLOAT, complexity=(0,4)):
		operators = getOperators(type)
		string = "$"
		for i in range(random.randint(complexity[0], complexity[1])):

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

		return Func(string)
