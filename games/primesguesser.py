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
			self._setData(self.getData()+1)

		prime = self.__isPrime(self.getData())
		print(str(prime) + " == " + str(action))
		if prime == (action == "prime"):
			print("prime guess " + str(self.getData()) + " was correct:")
			self._evaluatePlayer(playerID, 10)
		else:
			print("prime guess " + str(self.getData()) + " was wrong:")
			self._evaluatePlayer(playerID, -60)
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
