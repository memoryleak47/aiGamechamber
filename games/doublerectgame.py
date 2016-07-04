#!/usr/bin/python3

import random
import sys
import time
from game import *
import tkinter as tk

WIDTH=30
HEIGHT=30
TILESIZE = 10

# player0: a, c
# player1: B, D
# data = [xa, ya, xB, yB, xc, yc, xD, yD]

class Doublerectgame(Game):
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
		# x first
		if action[0] == "-1" and self.getData()[2*playerID] > 1:
			data[2*playerID] -= 1
		elif action[0] == "1" and self.getData()[2*playerID] < WIDTH-2:
			data[2*playerID] += 1

		# y first
		if action[1] == "-1" and self.getData()[1 + 2*playerID] > 1:
			data[1 + 2*playerID] -= 1
		elif action[1] == "1" and self.getData()[1 + 2*playerID] < WIDTH-2:
			data[1 + 2*playerID] += 1

		# x second
		if action[2] == "-1" and self.getData()[4 + 2*playerID] > 1:
			data[4 + 2*playerID] -= 1
		elif action[2] == "1" and self.getData()[4 + 2*playerID] < WIDTH-2:
			data[4 + 2*playerID] += 1

		# y second
		if action[3] == "-1" and self.getData()[5 + 2*playerID] > 1:
			data[5 + 2*playerID] -= 1
		elif action[3] == "1" and self.getData()[5 + 2*playerID] < WIDTH-2:
			data[5 + 2*playerID] += 1

		gameOver = False
		self._setData(data)
		evA = 0
		evB = 0
		if data[0] == data[2] and data[1] == data[3]:
			evA += 100
			evB -= 100
			gameOver = True
		if data[2] == data[4] and data[3] == data[5]:
			evA -= 100
			evB += 100
			gameOver = True
		if data[4] == data[6] and data[5] == data[7]:
			evA += 100
			evB -= 100
			gameOver = True
		if data[6] == data[0] and data[7] == data[1]:
			evA -= 100
			evB += 100
			gameOver = True
		self._evaluatePlayer(0, evA)
		self._evaluatePlayer(1, evB)
		if gameOver:
			self._gameOver()

	def render(self):
		self.__window.wm_title("Doublerectgame: " + str(self.getScore(0)) + "x" + str(self.getScore(1)))

		self.__canvas.create_rectangle(0, 0, WIDTH*TILESIZE, HEIGHT*TILESIZE, fill="black")
		self.__canvas.create_rectangle(TILESIZE, TILESIZE, (WIDTH-1)*TILESIZE, (HEIGHT-1)*TILESIZE, fill="white")

		x = self.getData()[0]*TILESIZE
		y = self.getData()[1]*TILESIZE
		self.__canvas.create_rectangle(x, y, x+TILESIZE, y+TILESIZE, fill="red")
		x = self.getData()[2]*TILESIZE
		y = self.getData()[3]*TILESIZE
		self.__canvas.create_rectangle(x, y, x+TILESIZE, y+TILESIZE, fill="blue")
		x = self.getData()[4]*TILESIZE
		y = self.getData()[5]*TILESIZE
		self.__canvas.create_rectangle(x, y, x+TILESIZE, y+TILESIZE, fill="yellow")
		x = self.getData()[6]*TILESIZE
		y = self.getData()[7]*TILESIZE
		self.__canvas.create_rectangle(x, y, x+TILESIZE, y+TILESIZE, fill="green")

	def getDataFormat(self):
		return "(int,int,int,int,int,int,int,int)"

	def getActionFormat(self):
		return "({'-1','0','1'},{'-1','0','1'},{'-1','0','1'},{'-1','0','1'})"

	def __repositionPlayers(self):
		self._setData([random.randint(1, WIDTH-2), random.randint(1, HEIGHT-2), random.randint(1,WIDTH-2), random.randint(1,HEIGHT-2), random.randint(1, WIDTH-2), random.randint(1, HEIGHT-2), random.randint(1,WIDTH-2), random.randint(1,HEIGHT-2)])

