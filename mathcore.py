#!/usr/bin/python3 -B

import random
import sys

ANY=-1
FLOAT = 0
BOOL = 1

ERRORDATA="_ERRORDATA_"

def die(string):
	print(string)
	1/0 # FOR THE STACK TRACE!

class Func:
	def __init__(self, string):
		if not isinstance(string, str):
			die("Func(string): (" + str(string) + ") is not a string")
		self.string = string

	def call(self, args, silent=False):
		try:
			result = eval(self.string)
		except:
			if not silent:
				print("func call failed: " + self.string)
			return ERRORDATA
		return result

	def toString(self):
		return self.string

	@staticmethod
	def getRandom(noInput, inputtype=FLOAT, outputtype=FLOAT):
		# outputlayer
		string = "$"
		for i in range(random.randint(0, 1)):
			spots=list()
			for spot in range(len(string)):
				if string[spot] == "$":
					spots.append(spot)
			chosenspot = spots[random.randint(0, len(spots)-1)]
			operators = Func.getOperators(outputtype, outputtype)
			chosenoperator = operators[random.randint(0,len(operators)-1)]
			string = string[:chosenspot] + chosenoperator + string[chosenspot+1:]
		# exchangelayer
		spots=list()
		for spot in range(len(string)):
			if string[spot] == "$":
				spots.append(spot)
		for chosenspot in reversed(spots):
			operators = Func.getOperators(inputtype, outputtype)
			chosenoperator = operators[random.randint(0,len(operators)-1)]
			string = string[:chosenspot] + chosenoperator + string[chosenspot+1:]
		# inputlayer
		for i in range(random.randint(0, 1)):
			spots=list()
			for spot in range(len(string)):
				if string[spot] == "$":
					spots.append(spot)
			chosenspot = spots[random.randint(0, len(spots)-1)]
			operators = Func.getOperators(inputtype, inputtype)
			chosenoperator = operators[random.randint(0,len(operators)-1)]
			string = string[:chosenspot] + chosenoperator + string[chosenspot+1:]
		while "$" in string:
			spot = string.find("$")
			string = string[:spot] + "args[" + str(random.randint(0, noInput-1)) + "]" + string[spot+1:]

		return Func(string)

	@staticmethod
	def getOperators(inputtype, outputtype):
		ops = [
			("($+$)", FLOAT, FLOAT),
			("($-$)", FLOAT, FLOAT),
			("($*$)", FLOAT, FLOAT),
			("($/$)", FLOAT, FLOAT),
			("min($,$)", FLOAT, FLOAT),
			("max($,$)", FLOAT, FLOAT),
			("($<$)", FLOAT, BOOL),
			("($>$)", FLOAT, BOOL),
			("($==$)", ANY, BOOL),
			("not($)", BOOL, BOOL),
			("($)and($)", BOOL, BOOL),
			("($)or($)", BOOL, BOOL)
		]
		result = list()
		for op in ops:
			if (op[1] == ANY or inputtype == ANY or op[1] == inputtype) and (op[2] == ANY or outputtype == ANY or op[2] == outputtype):
				result.append(op[0])
		return result
