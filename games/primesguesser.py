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
		self._setData(self.getData()+1)

		prime = self.__isPrime(self.getData())
		if prime == (action[0] == "prime"):
			self._evaluatePlayer(playerID, 3)
			print("prime guess " + str(self.getData()) + " was correct")
		else:
			self._evaluatePlayer(playerID, -1)
			print("prime guess " + str(self.getData()) + " was wrong")

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
