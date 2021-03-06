#!/usr/bin/python3

import random
import sys
import time
from game import *
import tkinter as tk

WIDTH=30
HEIGHT=30

class Together(Game):
	def __init__(self, noPlayers, window):
		if noPlayers != 2:
			print("Invalid size")
			sys.exit()
		Game.__init__(self, noPlayers)
		self.__window = window
		self._setData()

	def _restart(self):
		pass

	def applyAction(self, action, playerID):
		if action[0] < 0:
			self._evaluatePlayer(playerID, 10)
			self._evaluatePlayer(1-playerID, 10)
		else:
			self._evaluatePlayer(playerID, 100)
			self._evaluatePlayer(1-playerID, -100)
		self._setData()

	def render(self):
		self.__window.wm_title("Together: " + str(self.getScore(0)) + "x" + str(self.getScore(1)))

	def getActionFormat(self):
		return "bool"

	def getDataFormat(self):
		return ""
