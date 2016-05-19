#!/usr/bin/python3

import random
import sys
import time
from game import *
import tkinter as tk

WIDTH=30
HEIGHT=30

class Rectgame(Game):
	def __init__(self, noPlayers, window):
		if noPlayers != 2:
			print("Invalid size")
			sys.exit()
		Game.__init__(self, noPlayers)
		self.__window = window
		self.__listbox = tk.Listbox(self.__window, width=800, height=600)
		self.__listbox.config(font=("Monospace", 12))
		self.__listbox.pack()

	def _restart(self):
		self.__repositionPlayers()

	def applyAction(self, action, playerID):
		data = self.getData()
		if action[0] < 0 and self.getData()[2*playerID] > 1:
			data[2*playerID] -= 1
		elif action[0] > 0 and self.getData()[2*playerID] < WIDTH-2:
			data[2*playerID] += 1

		if action[1] < 0 and self.getData()[1 + 2*playerID] > 1:
			data[1 + 2*playerID] -= 1
		elif action[1] > 0 and self.getData()[1 + 2*playerID] < WIDTH-2:
			data[1 + 2*playerID] += 1
		self._setData(data)
		if self.__areTheyCatching():
			self._evaluatePlayer(0, 100)
			self._evaluatePlayer(1, -100)
			self._gameOver()
		else:
			self._evaluatePlayer(0, -1)
			self._evaluatePlayer(1, 1)

	def render(self):
		field=list()

		field.append(list("#"*WIDTH))
		for i in range(HEIGHT-2):
			field.append(list("#" + " " * (WIDTH-2) + "#"))
		field.append(list("#"*WIDTH))

		char = "0"
		field[self.getData()[1]][self.getData()[0]] = char

		char = "1"
		field[self.getData()[3]][self.getData()[2]] = char

		self.__listbox.delete(0, self.__listbox.size()-1)
		for line in field:
			self.__listbox.insert(tk.END, "".join(line))

	def getNoInput(self):
		return self.getNoPlayers() * 2

	def getNoOutput(self):
		return 2

	def __repositionPlayers(self):
		self._setData([random.randint(1, WIDTH-2), random.randint(1, HEIGHT-2), random.randint(1,WIDTH-2), random.randint(1,HEIGHT-2)])

	def __areTheyCatching(self):
		return (self.getData()[0] == self.getData()[2]) and (self.getData()[1]) == (self.getData()[3])

