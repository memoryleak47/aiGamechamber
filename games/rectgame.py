#!/usr/bin/python3

import random
import sys
import time
from game import *
import tkinter as tk

WIDTH=30
HEIGHT=30
TILESIZE=10

class Rectgame(Game):
	def __init__(self, noPlayers, window):
		if noPlayers != 2:
			print("Invalid size")
			sys.exit()
		Game.__init__(self, noPlayers)
		self.__window = window

		self.__canvas = tk.Canvas(self.__window, width=800, height=600)
		self.__canvas.pack()

	def _restart(self):
		self.__repositionPlayers()

	def applyAction(self, action, playerID):
		data = self.getData()
		if action[0] == "-1" and self.getData()[2*playerID] > 1:
			data[2*playerID] -= 1
		elif action[0] == "1" and self.getData()[2*playerID] < WIDTH-2:
			data[2*playerID] += 1

		if action[1] == "-1" and self.getData()[1 + 2*playerID] > 1:
			data[1 + 2*playerID] -= 1
		elif action[1] == "1" and self.getData()[1 + 2*playerID] < WIDTH-2:
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
		self.__window.wm_title("Rectgame: red=" + str(self.getScore(0)) + " green=" + str(self.getScore(1)))
		
		self.__canvas.delete("all")
		self.__canvas.create_rectangle(0, 0, WIDTH*TILESIZE, HEIGHT*TILESIZE, fill="black")
		self.__canvas.create_rectangle(TILESIZE, TILESIZE, (WIDTH-1)*TILESIZE, (HEIGHT-1)*TILESIZE, fill="white")

		x = self.getData()[0]*TILESIZE
		y = self.getData()[1]*TILESIZE
		self.__canvas.create_rectangle(x, y, x+TILESIZE, y+TILESIZE, fill="red")
		x = self.getData()[2]*TILESIZE
		y = self.getData()[3]*TILESIZE
		self.__canvas.create_rectangle(x, y, x+TILESIZE, y+TILESIZE, fill="green")

	def getDataFormat(self):
		return "(int,int,int,int)"

	def getActionFormat(self):
		return "({'-1','0','1'},{'-1','0','1'})"

	def __repositionPlayers(self):
		self._setData([random.randint(1, WIDTH-2), random.randint(1, HEIGHT-2), random.randint(1,WIDTH-2), random.randint(1,HEIGHT-2)])

	def __areTheyCatching(self):
		return (self.getData()[0] == self.getData()[2]) and (self.getData()[1]) == (self.getData()[3])

