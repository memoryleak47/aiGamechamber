#!/usr/bin/python3

import random
import sys
import time
from game import *

class Primesguesser(Game):
	def __init__(self, noPlayers):
		if noPlayers != 2:
			print("Invalid size")
			sys.exit()
		Game.__init__(self, noPlayers)
		self._setData(1)

	def _restart(self): pass

	def applyAction(self, action, playerID):
		if playerID == 0:
			self._setData(random.randint(2, random.randint(2, random.randint(2, random.randint(2, random.randint(2, 200000000))))))

		if self.__isPrime(self.getData()):
			if action == "prime":
				print("NICE ONE, " + str(self.getData()) + " is a prime")
				self._evaluatePlayer(playerID, 100)
			else:
				print("NOPE!? " + str(self.getData()) + " is no prime")
				self._evaluatePlayer(playerID, -200)
		else:
			if action == "prime":
				print("nope " + str(self.getData()) + " is no prime")
				self._evaluatePlayer(playerID, -30)
			else:
				print("easy, " + str(self.getData()) + " is a prime")
				self._evaluatePlayer(playerID, 1)
		print("\n\n")

	def render(self):
		pass

	def getDataFormat(self):
		return "int"

	def getActionFormat(self):
		return "{'no prime','prime'}"

	@staticmethod
	def __isPrime(number):
		for i in range(2, number):
			if number % i == 0:
				return False
		return True
